#!/usr/bin/env python3
"""
書籍自動化排版建置腳本 (Automated Book Typesetting & Build Pipeline)
讀取 src/ 目錄下的 Markdown 章節，轉換為 Typst 語法並編譯為印刷級 PDF。
"""

import os
import re
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
DIST_DIR = ROOT_DIR / "dist"
TEMPLATES_DIR = ROOT_DIR / "templates"


def md_to_typst(md_content: str) -> str:
    """輕量且穩健的 Markdown 轉 Typst 轉換器"""
    lines = md_content.splitlines()
    typst_lines = []
    in_code_block = False
    code_lang = ""

    for line in lines:
        # 處理代碼塊
        if line.startswith("```"):
            if not in_code_block:
                in_code_block = True
                lang_match = re.match(r"```(\w+)?", line)
                code_lang = lang_match.group(1) if lang_match and lang_match.group(1) else ""
                typst_lines.append(f"```{code_lang}")
            else:
                in_code_block = False
                typst_lines.append("```\n")
            continue

        if in_code_block:
            typst_lines.append(line)
            continue

        # 處理 Mermaid 圖表區塊 (轉為註記提示)
        if "graph LR" in line or "flowchart" in line or "stateDiagram" in line:
            typst_lines.append("// [架構圖表略縮區塊]")
            continue

        # 處理水平分隔線
        if line.strip() in ("---", "***", "___"):
            typst_lines.append("#v(0.5em)\n#line(length: 100%, stroke: 0.5pt + luma(200))\n#v(0.5em)")
            continue

        # 處理標題
        if line.startswith("# "):
            typst_lines.append(f"= {line[2:].strip()}\n")
            continue
        elif line.startswith("## "):
            typst_lines.append(f"== {line[3:].strip()}\n")
            continue
        elif line.startswith("### "):
            typst_lines.append(f"=== {line[4:].strip()}\n")
            continue

        # 處理引用塊
        if line.startswith("> "):
            quote_text = line[2:].strip().replace('"', '\\"')
            typst_lines.append(f'#quote[\n{quote_text}\n]\n')
            continue

        # 處理無序列表
        if re.match(r"^\s*[\*\-]\s+", line):
            indent_level = len(line) - len(line.lstrip())
            cleaned = re.sub(r"^\s*[\*\-]\s+", "", line)
            # 轉換行內粗體
            cleaned = re.sub(r"\*\*([^\*]+)\*\*", r"*\1*", cleaned)
            typst_lines.append("  " * (indent_level // 2) + f"- {cleaned}")
            continue

        # 處理有序列表
        if re.match(r"^\s*\d+\.\s+", line):
            cleaned = re.sub(r"^\s*\d+\.\s+", "", line)
            cleaned = re.sub(r"\*\*([^\*]+)\*\*", r"*\1*", cleaned)
            typst_lines.append(f"+ {cleaned}")
            continue

        # 處理行內粗體
        processed_line = re.sub(r"\*\*([^\*]+)\*\*", r"*\1*", line)
        typst_lines.append(processed_line)

    return "\n".join(typst_lines)


def build_book():
    DIST_DIR.mkdir(exist_ok=True)
    print("==================================================")
    print("📚 開始編譯全書 Typst 印刷級出版物")
    print("==================================================")

    # 1. 編譯封面
    print("▶ 1. 編譯書籍封面...")
    cover_cmd = ["typst", "compile", str(TEMPLATES_DIR / "cover.typ"), str(DIST_DIR / "cover.pdf")]
    subprocess.run(cover_cmd, check=True)
    print("   ✅ 封面生成完畢: dist/cover.pdf")

    # 2. 合併前言、章節與附錄並生成主內文
    print("▶ 2. 轉換 Markdown 章節為 Typst 格式...")
    chapters = sorted(list(SRC_DIR.glob("ch*.md")))
    source_files = []
    preface_path = SRC_DIR / "preface.md"
    appendix_path = SRC_DIR / "appendix.md"
    if preface_path.exists():
        source_files.append(preface_path)
    source_files.extend(chapters)
    if appendix_path.exists():
        source_files.append(appendix_path)
    if not source_files:
        print("❌ 未在 src/ 找到任何書籍 Markdown！")
        return

    full_typst_content = [
        '#import "../templates/book.typ": project',
        '',
        '#show: project.with(',
        '  title: "多 Agent 系統架構與實戰",',
        '  subtitle: "用 AI Agent 團隊完成寫作、測試、排版與發布",',
        '  author: "Happy eBook Authors",',
        '  version: "1.0.0"',
        ')',
        ''
    ]

    for source_path in source_files:
        print(f"   處理: {source_path.name} ...")
        with open(source_path, "r", encoding="utf-8") as f:
            md_text = f.read()
        full_typst_content.append(md_to_typst(md_text))
        full_typst_content.append("\n#pagebreak()\n")

    book_typ_path = DIST_DIR / "book_interior.typ"
    with open(book_typ_path, "w", encoding="utf-8") as f:
        f.write("\n".join(full_typst_content))

    # 3. 編譯內文 PDF
    print("▶ 3. 呼叫 Typst 編譯內文 PDF...")
    interior_pdf_path = DIST_DIR / "book_interior.pdf"
    typst_cmd = ["typst", "compile", "--root", str(ROOT_DIR), str(book_typ_path), str(interior_pdf_path)]
    subprocess.run(typst_cmd, check=True)
    print(f"   ✅ 內文排版完成: dist/{interior_pdf_path.name}")

    print("\n==================================================")
    print("🎉 書籍構建全流程完畢！輸出檔案如下：")
    print(f"   - 封面: {DIST_DIR / 'cover.pdf'}")
    print(f"   - 內文: {DIST_DIR / 'book_interior.pdf'}")
    print("==================================================")


if __name__ == "__main__":
    build_book()
