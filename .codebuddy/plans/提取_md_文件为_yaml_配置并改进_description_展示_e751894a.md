---
name: 提取 md 文件为 yaml 配置并改进 description 展示
overview: 将项目中的 md 文件（图论、数论、串论、概率论、离散数学、数学分析、组合数学）提取成 yaml 配置文件，添加到 chapters/ 目录下；同时改进 index.html，在网页界面上展示 description 字段，让用户在练习 LaTeX 的同时学习数学概念。
design:
  architecture:
    framework: html
  fontSystem:
    fontFamily: Inter, 'Segoe UI', system-ui, sans-serif
    heading:
      size: 1.1rem
      weight: 600
    subheading:
      size: 0.95rem
      weight: 500
    body:
      size: 0.95rem
      weight: 400
  colorSystem:
    primary:
      - "#6c8ef5"
    background:
      - "#1a1d27"
    text:
      - "#e2e8f0"
    functional:
      - "#8892b0"
todos:
  - id: analyze-md-structure
    content: 分析所有 md 文件结构，确定提取规则，包括识别 LaTeX 公式、概念描述和输入提示
    status: completed
  - id: create-yaml-configs
    content: 为 7 个 md 文件创建对应的 yaml 配置文件，遵循现有格式并确保字段完整
    status: completed
    dependencies:
      - analyze-md-structure
  - id: update-chapters-index
    content: 修改 chapters/index.yaml，添加新章节索引，确保网页能加载新配置文件
    status: completed
    dependencies:
      - create-yaml-configs
  - id: modify-html-description
    content: 修改 index.html，添加 description 展示区域，并修改 loadKoan 函数以渲染 description 字段
    status: completed
    dependencies:
      - analyze-md-structure
  - id: test-webpage
    content: 测试网页功能，确保新章节能正确加载，description 能正确显示且 LaTeX 公式能正确渲染
    status: completed
    dependencies:
      - update-chapters-index
      - modify-html-description
---

## 用户需求

将项目中的 md 文件（图论.md、数论.md、串论.md、概率论.md、离散数学.md、数学分析.md、组合数学.md）提取成 yaml 配置文件，并改进网页上 description 的展示方式。

## 功能描述

1. **提取 md 文件为 yaml 配置**：按需要输入的 LaTeX 公式来提取，每个公式作为一个独立的 koan。如果一个概念有 2 个不同的大公式，可以重复描述，创建两个 koan。如果两个公式中间文字很少，可以合并成一个 koan，中间加点英文。description 可以完整描述数学概念，必要时可多展示 LaTeX 公式。
2. **改进网页展示**：在 index.html 中改进 description 的展示方式，当前 loadKoan 函数没有渲染 description 字段，需要在网页界面上展示 description。

## 技术栈

- 前端：HTML, CSS, JavaScript
- 配置文件：YAML
- LaTeX 渲染：MathJax 3
- YAML 解析：js-yaml

## 实现方法

1. **提取 md 文件**：分析 md 文件结构，识别需要用户输入的 LaTeX 公式，按照用户指定的规则提取成 yaml 配置文件。每个 koan 包含字段：id, chapter, title, tag, difficulty, latex, description, hint。

- `latex` 字段：用户需要输入的 LaTeX 公式（用于练习）
- `description` 字段：完整描述数学概念，可包含 LaTeX 公式（用于学习）
- `hint` 字段：用户输入提示

2. **修改 index.html**：

- 在 HTML 中的 `.content` 部分，在 compare preview 卡片之后、editor 卡片之前，添加 description 展示区域（`<div class="description card" id="description">`）
- 修改 `loadKoan` 函数，在渲染目标公式后，渲染 description 字段到新添加的元素
- 确保 MathJax 渲染 description 中的 LaTeX 公式

3. **修改 chapters/index.yaml**：添加新的章节索引，指向新创建的 yaml 配置文件。

在网页上添加一个区域来展示 description，位置在 "图形对比" 卡片之后，"LaTeX 输入" 卡片之前。使用卡片样式（class="card"）以保持与现有设计一致。description 内容应美观、易读，支持 LaTeX 公式渲染。

设计要点：

- 创建一个独立的卡片来展示 description
- 卡片标题为 "概念说明"
- 内容区域使用现有的 .description CSS 类，并确保 MathJax 渲染其中的 LaTeX 公式
- 在 loadKoan 函数中，每次加载新题目时更新 description 内容

## Agent Extensions

### SubAgent

- **code-explorer**
- Purpose: 探索代码库，分析 md 文件结构，提取内容到 yaml 配置文件
- Expected outcome: 生成所有 md 文件对应的 yaml 配置文件，确保每个 koan 包含正确的字段和格式