# 风格分析：用户参考图

## 核心视觉特征

### 配色
- **背景**: 暖米色/奶油色 (#F4F0E7 / #F5F0E6)
- **主文字**: 纯黑粗体 (#211F1B)
- **强调色**: 铜色/赤陶色 (#B87333) 用于 italic 文字
- **卡片底色**: 柔和 pastel（蜜桃、鼠尾草绿、粉蓝、薄荷、淡紫）
- **描边**: 黑色粗线，手绘不完美感

### 字体
- **标题**: 粗衬线体 (Playfair Display / Fraunces 风格)，全大写或首字母大写
- **Italic**: 用于副标题或强调词，铜色
- **标签**: 小号无衬线，全大写，带手绘边框
- **编号**: 01/02/03 双位数，细线分隔

### 元素
1. **手绘边框**: 粗黑线，略有抖动感，不是精密 CSS border
2. **分类卡片**: 左侧竖线 + 编号 + 标题 + 描述，右侧箭头
3. **小标签 pill**: "100 REPOS", "10 SECTIONS", "HONEST" 带框
4. **角落装饰**: 四个角的括号/方框角标
5. **Credit**: 右下角手写体风格 @username

### 整体氛围
Editorial + Indie + Hand-crafted + Print Magazine

## 应用到 DeepSeek × Gemini 封面的方案

### 构图
**左右分栏**（跟参考图一致）
- **左侧 40%**: 大标题 + 副标题 + 标签
- **右侧 60%**: 两个 pipeline 卡片，用箭头连接

### 左侧内容
- **主标题**: DEEPSEEK + GEMINI
- **副标题 (italic copper)**: A Multi-Model Coding Pipeline
- **三个标签**: VISION | REASONING | MCP

### 右侧内容
- **Card 1 (蜜桃底色)**: 01 | Gemini Flash — image analysis & OCR
- **Card 2 (鼠尾草绿底色)**: 02 | DeepSeek V4 — code generation
- **连接箭头**: 细黑线箭头从 Card 1 指向 Card 2

### 装饰
- 四角括号
- 右下角: @hwan50
- 底部小字: "Built with MCP Protocol"

## Pollinations Prompt

```
Editorial illustration in warm cream paper style with hand-drawn black ink borders. Left side: large bold serif headline "DEEPSEEK + GEMINI" with italic copper-colored subtitle "A Multi-Model Coding Pipeline". Three small hand-drawn pill tags below: "VISION", "REASONING", "MCP". Right side: two connected workflow cards — Card 1 (soft peach background, black hand-drawn border) labeled "01 | Gemini Flash" with subtitle "image analysis + OCR", Card 2 (soft sage green background, black hand-drawn border) labeled "02 | DeepSeek V4" with subtitle "code generation". Thin arrow connecting the two cards. Corner bracket decorations in all four corners. Hand-lettered credit "@hwan50" in bottom right. Warm beige background #F4F0E7, minimalist editorial layout, flat illustration, no gradients, no shadows, print magazine aesthetic, indie zine style.
```
