#!/usr/bin/env python3
"""
Gemini Vision MCP Server for DeepSeek TUI
Connects DeepSeek TUI to Google Gemini Flash for image understanding.

Usage:
  1. Install deps: pip install google-generativeai mcp
  2. Set env: export GEMINI_API_KEY="your-key"
  3. Run: python3 gemini_vision_mcp.py
  4. Configure in DeepSeek TUI: ~/.config/deepseek/mcp.json

Author: frank kimi
License: MIT
"""

import os
import sys
import json
import base64
from typing import Any

try:
    import google.generativeai as genai
except ImportError:
    print("ERROR: google-generativeai not installed. Run: pip install google-generativeai")
    sys.exit(1)

try:
    from mcp.server import Server
    from mcp.types import TextContent, Tool
except ImportError:
    print("ERROR: mcp package not installed. Run: pip install mcp")
    sys.exit(1)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable not set")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

app = Server("gemini-vision")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="describe_image",
            description="Analyze an image (screenshot, design mockup, UI) and return a detailed structured description suitable for coding. Includes layout, colors, typography, components, and spacing.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Absolute or relative path to the image file (PNG, JPG, WEBP)"
                    },
                    "detail_level": {
                        "type": "string",
                        "enum": ["brief", "standard", "detailed"],
                        "description": "How thorough the analysis should be",
                        "default": "detailed"
                    }
                },
                "required": ["image_path"]
            }
        ),
        Tool(
            name="extract_text",
            description="Extract all visible text from an image (OCR). Useful for scraping UI labels, error messages, or documentation screenshots.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Absolute or relative path to the image file"
                    }
                },
                "required": ["image_path"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name not in ("describe_image", "extract_text"):
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    image_path = arguments.get("image_path", "")
    if not image_path or not os.path.exists(image_path):
        return [TextContent(type="text", text=f"Image not found: {image_path}")]

    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    model = genai.GenerativeModel("gemini-2.0-flash")

    if name == "describe_image":
        detail = arguments.get("detail_level", "detailed")
        prompts = {
            "brief": "Describe this UI/website screenshot briefly in 3-4 sentences.",
            "standard": "Describe this UI screenshot. Include: layout structure, main colors, typography style, key components.",
            "detailed": (
                "You are a frontend developer analyzing a UI design screenshot. "
                "Provide a DETAILED structured description including:\n"
                "1. LAYOUT: Overall structure (header, hero, sections, footer)\n"
                "2. COLORS: Primary, secondary, background, text colors with approximate hex values\n"
                "3. TYPOGRAPHY: Font sizes, weights, hierarchy (H1, H2, body)\n"
                "4. COMPONENTS: Buttons, cards, forms, navigation elements with their styles\n"
                "5. SPACING: Padding, margins, gaps between elements\n"
                "6. RESPONSIVE HINTS: If mobile/desktop layout is visible\n"
                "Format as clean markdown. Be precise enough that a developer can reconstruct this UI from your description alone."
            )
        }
        prompt = prompts.get(detail, prompts["detailed"])

    else:  # extract_text
        prompt = "Extract ALL visible text from this image. Preserve the layout/structure as much as possible. Output as markdown."

    try:
        response = model.generate_content(
            [
                prompt,
                {"mime_type": "image/png", "data": image_b64}
            ]
        )
        return [TextContent(type="text", text=response.text)]
    except Exception as e:
        return [TextContent(type="text", text=f"Gemini API error: {str(e)}")]


if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )

    asyncio.run(main())
