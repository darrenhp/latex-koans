#!/usr/bin/env python3
"""
补充 YAML 文件中的 LaTeX 公式
从 description 字段提取 LaTeX 公式，补充到 latex 字段中
"""

import re
import yaml
from pathlib import Path
from typing import List, Set

def extract_latex_from_description(description: str) -> List[str]:
    """从 description 中提取所有 LaTeX 公式"""
    formulas = []
    
    # 匹配块级公式 $$...$$
    block_pattern = r'\$\$(.+?)\$\$'
    block_matches = re.findall(block_pattern, description, re.DOTALL)
    formulas.extend([m.strip() for m in block_matches])
    
    # 匹配行内公式 $...$
    # 需要排除已经匹配过的块级公式
    inline_pattern = r'(?<!\$)\$(?!\$)(.+?)\$(?!\$)'
    inline_matches = re.findall(inline_pattern, description, re.DOTALL)
    
    for match in inline_matches:
        # 清理公式
        formula = match.strip()
        if formula and formula not in formulas:
            formulas.append(formula)
    
    return formulas

def normalize_formula(formula: str) -> str:
    """规范化公式（去除多余空格、换行等）"""
    # 去除前后空格
    normalized = formula.strip()
    # 将多个空格替换为单个空格
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized

def get_existing_formulas(latex_str: str) -> Set[str]:
    """从 latex 字段中获取现有公式的集合"""
    if not latex_str:
        return set()
    
    # 按行分割，每行可能是一个公式
    formulas = set()
    for line in latex_str.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            formulas.add(normalize_formula(line))
    
    return formulas

def merge_latex_field(existing: str, new_formulas: List[str]) -> str:
    """合并 latex 字段，去重"""
    if not existing:
        return '\n'.join(new_formulas)
    
    existing_formulas = get_existing_formulas(existing)
    existing_lines = existing.split('\n')
    
    # 添加新的公式
    for formula in new_formulas:
        normalized_new = normalize_formula(formula)
        if normalized_new not in existing_formulas:
            existing_lines.append(formula)
            existing_formulas.add(normalized_new)
    
    return '\n'.join(existing_lines)

def process_yaml_file(file_path: Path, dry_run: bool = False) -> dict:
    """处理单个 YAML 文件"""
    print(f"\n处理文件: {file_path.name}")
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析 YAML
    data = yaml.safe_load(content)
    
    if not data or 'koans' not in data:
        print(f"  跳过：没有找到 koans 字段")
        return {'file': file_path.name, 'updated': 0, 'skipped': 0}
    
    updated_count = 0
    skipped_count = 0
    
    for koan in data['koans']:
        if not isinstance(koan, dict):
            continue
        
        title = koan.get('title', 'Unknown')
        description = koan.get('description', '')
        latex = koan.get('latex', '')
        
        if not description:
            skipped_count += 1
            continue
        
        # 提取 description 中的公式
        formulas_in_desc = extract_latex_from_description(description)
        
        if not formulas_in_desc:
            skipped_count += 1
            continue
        
        # 获取现有公式
        existing_formulas = get_existing_formulas(latex)
        
        # 找出缺失的公式
        missing_formulas = []
        for formula in formulas_in_desc:
            normalized = normalize_formula(formula)
            if normalized not in existing_formulas:
                missing_formulas.append(formula)
        
        if missing_formulas:
            # 更新 latex 字段
            new_latex = merge_latex_field(latex, missing_formulas)
            koan['latex'] = new_latex
            updated_count += 1
            print(f"  更新: {title}")
            print(f"    添加 {len(missing_formulas)} 个公式")
            
            if dry_run:
                print(f"    [DRY RUN] 不会实际修改")
        else:
            skipped_count += 1
    
    # 写回文件
    if not dry_run and updated_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        print(f"  已写入文件")
    
    return {
        'file': file_path.name,
        'updated': updated_count,
        'skipped': skipped_count
    }

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='补充 YAML 文件中的 LaTeX 公式')
    parser.add_argument('--dry-run', action='store_true', help='试运行模式，不实际修改文件')
    parser.add_argument('--chapters-dir', type=str, default='chapters', help='chapters 目录路径')
    args = parser.parse_args()
    
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    chapters_dir = project_dir / args.chapters_dir
    
    if not chapters_dir.exists():
        print(f"错误：目录不存在 {chapters_dir}")
        return
    
    # 获取所有 YAML 文件
    yaml_files = sorted(chapters_dir.glob('*.yaml'))
    
    if not yaml_files:
        print(f"警告：没有找到 YAML 文件 in {chapters_dir}")
        return
    
    print(f"找到 {len(yaml_files)} 个 YAML 文件")
    print(f"试运行模式: {args.dry_run}")
    
    # 处理每个文件
    total_updated = 0
    total_skipped = 0
    
    for yaml_file in yaml_files:
        result = process_yaml_file(yaml_file, dry_run=args.dry_run)
        total_updated += result['updated']
        total_skipped += result['skipped']
    
    print(f"\n处理完成:")
    print(f"  总更新: {total_updated} 个 koan")
    print(f"  总跳过: {total_skipped} 个 koan")

if __name__ == '__main__':
    main()
