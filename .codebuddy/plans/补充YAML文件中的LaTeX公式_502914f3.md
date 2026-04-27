---
name: 补充YAML文件中的LaTeX公式
overview: 检查所有 chapters/ 下的 YAML 文件，将 description 中包含的 LaTeX 公式（用 $...$ 或 $$...$$ 包裹）补充到对应的 latex 字段中，确保 latex 字段尽可能完整地包含该条目的所有公式。
todos:
  - id: create-script
    content: 创建 Python 脚本用于提取和补充 LaTeX 公式
    status: completed
  - id: process-files
    content: 使用脚本处理所有 12 个 YAML 文件，补充缺失的 LaTeX 公式到 latex 字段
    status: completed
    dependencies:
      - create-script
  - id: verify-changes
    content: 验证修改后的 YAML 文件格式正确且内容完整
    status: completed
    dependencies:
      - process-files
---

## 产品概述

检查并补充 YAML 文件中的 LaTeX 公式。当前项目中，每个 koan 条目包含 `latex` 和 `description` 两个字段，其中 `description` 中可能包含用 `$... 或 `$... 包裹的 LaTeX 公式，但这些公式可能没有完整地出现在 `latex` 字段中。

## 核心功能

- 扫描所有 12 个 YAML 文件（位于 chapters/ 目录下）
- 识别每个 koan 条目中 `description` 字段包含的 LaTeX 公式
- 将 `description` 中存在但 `latex` 字段中缺失的公式补充到 `latex` 字段
- 保持 YAML 文件格式的一致性和正确性

## 技术栈选择

- **编程语言**: Python 3
- **YAML 处理**: PyYAML 库（或使用标准库手动解析以保留格式）
- **正则表达式**: 用于从 description 中提取 LaTeX 公式

## 实现方案

### 策略

采用 Python 脚本批量处理所有 YAML 文件，具体步骤：

1. **文件遍历**: 遍历 `chapters/` 目录下的所有 `.yaml` 文件
2. **内容解析**: 读取每个 YAML 文件，解析 koans 列表
3. **公式提取**: 对每个 koan 的 `description` 字段，使用正则表达式提取所有 LaTeX 公式：

- 匹配模式：`\$((?:[^\$]|\\[^\$])+)\ (行内公式 `$...)
- 匹配模式：`\$\$((?:[^\$]|\\[^\$])+)\$\ (块级公式 `$...)

4. **公式比较**: 将提取的公式与 `latex` 字段中的公式进行比较
5. **字段更新**: 将缺失的公式追加到 `latex` 字段中
6. **文件写回**: 保持 YAML 格式写回文件

### 关键技术方案

#### 公式提取逻辑

```python
import re

def extract_latex_from_description(description):
    """从 description 中提取所有 LaTeX 公式"""
    patterns = [
        r'\$\$(.+?)\$\$',  # 块级公式 $$...$$
        r'(?<!\$)\$(?!\$)(.+?)\$(?!\$)'  # 行内公式 $...$
    ]
    formulas = []
    for pattern in patterns:
        matches = re.findall(pattern, description, re.DOTALL)
        formulas.extend(matches)
    return formulas
```

#### 公式去重与合并

- 将 `latex` 字段按 `, ` 或换行分割为公式列表
- 将 `description` 提取的公式与现有公式对比
- 使用规范化比较（去除空格、换行等差异）
- 将新公式追加到 `latex` 字段

#### YAML 格式保持

- 使用 `ruamel.yaml` 库代替 `PyYAML`，以保留注释和格式
- 或者采用逐行读取、手动更新特定字段的方式

### 实现注意事项

1. **性能优化**:

- 批量处理文件，避免重复 I/O
- 使用正则表达式预编译提高匹配效率

2. **日志记录**:

- 记录每个文件的处理结果
- 记录更新的 koan 条目及具体变更

3. **回滚机制**:

- 处理前备份原文件
- 提供 dry-run 模式（仅打印变更，不实际修改）

4. **错误处理**:

- YAML 解析错误处理
- 正则表达式匹配异常处理
- 文件读写权限检查

## 架构设计

### 系统架构

采用脚本式架构，单文件处理流程：

```
YAML 文件 → 读取解析 → 提取公式 → 比较合并 → 写回文件
```

### 数据流

1. 读取 YAML 文件内容
2. 解析为结构化数据（koans 列表）
3. 遍历每个 koan 条目：

- 提取 description 中的 LaTeX 公式
- 与 latex 字段比较
- 更新 latex 字段

4. 写回 YAML 文件

## 目录结构

本任务主要涉及对现有文件的修改，不需要创建新的目录结构。

涉及的文件：

```
/Users/darrenhp/github.com/darrenhp/latex-koans/chapters/
├── 01-基础语法.yaml  [MODIFY]
├── 02-常用运算符.yaml  [MODIFY]
├── 03-进阶表达.yaml  [MODIFY]
├── 04-经典公式.yaml  [MODIFY]
├── 05-图论.yaml  [MODIFY]
├── 06-数论.yaml  [MODIFY]
├── 07-串论.yaml  [MODIFY]
├── 08-概率论.yaml  [MODIFY]
├── 09-离散数学.yaml  [MODIFY]
├── 10-数学分析.yaml  [MODIFY]
├── 11-组合数学.yaml  [MODIFY]
└── 12-物理学.yaml  [MODIFY]
```

## 关键代码结构

### 主处理函数

```python
def process_yaml_file(file_path: str, dry_run: bool = False) -> dict:
    """
    处理单个 YAML 文件，补充 latex 字段
    
    Args:
        file_path: YAML 文件路径
        dry_run: 是否为试运行模式
        
    Returns:
        处理结果统计
    """
    pass

def extract_latex_formulas(text: str) -> list:
    """
    从文本中提取所有 LaTeX 公式
    
    Args:
        text: 包含 LaTeX 公式的文本
        
    Returns:
        提取的公式列表
    """
    pass

def normalize_formula(formula: str) -> str:
    """
    规范化公式（去除多余空格、换行等）
    
    Args:
        formula: 原始公式
        
    Returns:
        规范化后的公式
    """
    pass

def merge_latex_field(existing: str, new_formulas: list) -> str:
    """
    合并 latex 字段，去重
    
    Args:
        existing: 现有 latex 字段内容
        new_formulas: 新提取的公式列表
        
    Returns:
        合并后的 latex 字段内容
    """
    pass
```

## Agent Extensions

### SubAgent

- **code-explorer**
- 用途: 在需要跨多个文件、目录或模式进行搜索时使用，或者当代码探索范围太大而无法单次调用 read_file 或 search_file 时。对于本任务，可用于验证 YAML 文件的结构一致性。
- 预期结果: 确认所有 YAML 文件的koans结构一致性，确保脚本能正确处理所有文件。