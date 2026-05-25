# DeepSeek TUI × Gemini Flash Pipeline

## Quick Start

### 1. Install Dependencies

```bash
pip install google-generativeai mcp
```

### 2. Get Gemini API Key

- Go to https://aistudio.google.com/app/apikey
- Create a new key
- Set environment variable: `export GEMINI_API_KEY="your-key"`

### 3. Configure MCP Server

Edit `~/.config/deepseek/mcp.json` (create if missing):

```json
{
  "mcpServers": {
    "gemini-vision": {
      "command": "python3",
      "args": ["/path/to/gemini_vision_mcp.py"],
      "env": {
        "GEMINI_API_KEY": "your-key"
      }
    }
  }
}
```

### 4. Start DeepSeek TUI with Vision

```bash
cd your-project
deepseek --enable mcp
```

### 5. Example Prompts

```
"Look at ./design/mockup.png and describe the layout in detail, then implement it in React + Tailwind"

"Extract all text from ./screenshots/error-message.png and help me debug this"

"Compare these two screenshots (./v1.png and ./v2.png) and tell me what visual differences exist"
```

## Architecture

```
User Prompt + Image
       |
       v
[DeepSeek TUI] ----MCP Call----> [Gemini Vision MCP Server]
       |                                    |
       |<----- Structured Image Desc -------|
       v
[DeepSeek V4]  writes code based on description
       |
       v
   Files written, shell exec, LSP check
```

## Cost Estimation (per workflow)

| Step | Model | Input | Output | Cost |
|------|-------|-------|--------|------|
| Image analysis | Gemini 2.0 Flash | 1 image (~1MB) | ~500 tokens text | ~$0.0003 |
| Code generation | DeepSeek V4-Flash | 2K tokens (desc + prompt) | 3K tokens code | ~$0.001 |
| LSP + iteration | DeepSeek V4-Flash | 5K tokens | 1K tokens | ~$0.0008 |
| **Total** | | | | **~$0.002** |

Compare: Single Claude Code session for similar task ≈ $0.30-1.50

## Troubleshooting

**"MCP server not found"**
- Check that `python3` is in your PATH
- Use absolute path for the `.py` file
- Verify `GEMINI_API_KEY` is set

**"Gemini API error"**
- Check your API key quota at https://aistudio.google.com/
- Gemini Flash has generous free tier (1500 requests/day)

**Image too large**
- Resize to < 4MB before sending
- Or add resize logic to MCP server

## Advanced: Custom Prompts

Edit the `prompts` dict in `gemini_vision_mcp.py` to add your own analysis styles:

```python
"accessibility": "Analyze this UI for accessibility issues. Check color contrast, alt text, keyboard navigation, ARIA labels...",
"mobile-first": "Describe this UI optimized for mobile breakpoints. Identify what should stack, what should hide..."
```

## License

MIT — use freely, modify for your workflow.
