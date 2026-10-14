#!/usr/bin/env python3
"""Build an EPUB 3 ebook and render Mermaid blocks as image assets.

This script intentionally has no Python package dependency. It extracts the
book Markdown, converts each Mermaid diagram into a Graphviz-rendered PNG, then
emits a minimal EPUB 3 package under dist/.
"""

from __future__ import annotations

import hashlib
import html
import re
import shutil
import subprocess
import uuid
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, List, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
DIST_DIR = ROOT_DIR / "dist"
EPUB_WORK_DIR = DIST_DIR / "epub_build"
OEBPS_DIR = EPUB_WORK_DIR / "OEBPS"
CHAPTERS_DIR = OEBPS_DIR / "chapters"
IMAGES_DIR = OEBPS_DIR / "images"
MERMAID_DIR = IMAGES_DIR / "mermaid"
META_INF_DIR = EPUB_WORK_DIR / "META-INF"

TITLE = "多 Agent 系統架構與實戰"
SUBTITLE = "用 AI Agent 團隊完成寫作、測試、排版與發布"
AUTHOR = "Happy eBook Authors"
LANGUAGE = "zh-Hant"
VERSION = "1.0.0"
BOOK_ID = "urn:uuid:9cce66ba-159f-4c67-bf06-8958f4d47de2"


@dataclass(frozen=True)
class Chapter:
    source: Path
    filename: str
    title: str
    xhtml: str


@dataclass(frozen=True)
class ImageAsset:
    href: str
    media_type: str


def source_files() -> List[Path]:
    files: List[Path] = []
    preface = SRC_DIR / "preface.md"
    appendix = SRC_DIR / "appendix.md"
    if preface.exists():
        files.append(preface)
    files.extend(sorted(SRC_DIR.glob("ch*.md")))
    if appendix.exists():
        files.append(appendix)
    return files


def slugify(path: Path) -> str:
    return path.stem.replace("_", "-")


def first_heading(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def normalize_mermaid_label(text: str) -> str:
    return text.strip().strip('"').strip("'")


def graphviz_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def extract_node(expr: str) -> Tuple[str, str]:
    expr = expr.strip().rstrip(";")
    match = re.match(r"([A-Za-z0-9_*\[\]]+)(?:\[(?:\"?)(.*?)(?:\"?)\])?$", expr)
    if not match:
        node_id = re.sub(r"\W+", "_", expr) or "node"
        return node_id, expr
    node_id = match.group(1)
    if node_id == "[*]":
        return "START", "開始"
    label = match.group(2) or node_id
    return node_id, normalize_mermaid_label(label)


def mermaid_to_dot(mermaid: str, title: str) -> str:
    lines = [line.strip() for line in mermaid.splitlines() if line.strip()]
    diagram_type = lines[0] if lines else "flowchart LR"
    rankdir = "LR" if "LR" in diagram_type or "stateDiagram" in diagram_type else "TB"
    nodes: dict[str, str] = {}
    edges: list[tuple[str, str, str]] = []

    for line in lines[1:]:
        line = line.strip().rstrip(";")
        if not line or line.startswith("%%"):
            continue

        # Mermaid edge with optional label: A -->|label| B, or A --> B: label
        edge_label = ""
        if "-->|" in line:
            left, rest = line.split("-->|", 1)
            edge_label, right = rest.split("|", 1)
        elif "-->" in line:
            left, right = line.split("-->", 1)
            if ":" in right and "[" not in right:
                right, edge_label = right.split(":", 1)
        else:
            continue

        src_id, src_label = extract_node(left)
        dst_id, dst_label = extract_node(right)
        nodes[src_id] = src_label
        nodes[dst_id] = dst_label
        edges.append((src_id, dst_id, normalize_mermaid_label(edge_label)))

    dot_lines = [
        "digraph G {",
        f"  graph [rankdir={rankdir}, bgcolor=\"transparent\", pad=0.2, nodesep=0.55, ranksep=0.65];",
        "  node [shape=box, style=\"rounded,filled\", color=\"#2563eb\", fillcolor=\"#eff6ff\", penwidth=1.6, fontname=\"Noto Sans CJK TC\", fontsize=18, margin=0.12];",
        "  edge [color=\"#64748b\", penwidth=1.4, fontname=\"Noto Sans CJK TC\", fontsize=13];",
        f"  labelloc=\"t\"; label={graphviz_quote(title)}; fontsize=20; fontname=\"Noto Sans CJK TC\";",
    ]
    for node_id, label in nodes.items():
        shape = "circle" if node_id == "START" else "box"
        dot_lines.append(f"  {graphviz_quote(node_id)} [label={graphviz_quote(label)}, shape={shape}];")
    for src, dst, label in edges:
        label_attr = f" [label={graphviz_quote(label)}]" if label else ""
        dot_lines.append(f"  {graphviz_quote(src)} -> {graphviz_quote(dst)}{label_attr};")
    dot_lines.append("}")
    return "\n".join(dot_lines) + "\n"


def render_mermaid_png(mermaid: str, asset_stem: str, title: str) -> str:
    MERMAID_DIR.mkdir(parents=True, exist_ok=True)
    dot_path = MERMAID_DIR / f"{asset_stem}.dot"
    png_path = MERMAID_DIR / f"{asset_stem}.png"
    dot_path.write_text(mermaid_to_dot(mermaid, title), encoding="utf-8")
    subprocess.run(["dot", "-Tpng", str(dot_path), "-o", str(png_path)], check=True)
    return f"../images/mermaid/{png_path.name}"


def replace_mermaid_blocks(markdown: str, chapter_stem: str) -> str:
    counter = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        mermaid = match.group(1).strip()
        title = f"{chapter_stem} architecture diagram {counter}"
        image_href = render_mermaid_png(mermaid, f"{chapter_stem}-{counter:02d}", title)
        return f'![架構圖 {counter}]({image_href})'

    return re.sub(r"```mermaid\n(.*?)\n```", repl, markdown, flags=re.S)


def parse_inline(text: str) -> str:
    placeholders: list[str] = []

    def stash(match: re.Match[str]) -> str:
        placeholders.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\u0000{len(placeholders)-1}\u0000"

    escaped = re.sub(r"`([^`]+)`", stash, html.escape(text, quote=False))
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>', escaped)
    for i, value in enumerate(placeholders):
        escaped = escaped.replace(f"\u0000{i}\u0000", value)
    return escaped


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def split_table_row(line: str) -> List[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def close_lists(out: List[str], list_stack: List[str]) -> None:
    while list_stack:
        out.append(f"</{list_stack.pop()}>")


def markdown_to_body(markdown: str) -> str:
    lines = markdown.splitlines()
    out: List[str] = []
    list_stack: List[str] = []
    paragraph: List[str] = []
    in_code = False
    code_lang = ""
    code_lines: List[str] = []
    i = 0

    def flush_para() -> None:
        nonlocal paragraph
        if paragraph:
            close_lists(out, list_stack)
            out.append(f"<p>{parse_inline(' '.join(paragraph).strip())}</p>")
            paragraph = []

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            if not in_code:
                flush_para()
                close_lists(out, list_stack)
                in_code = True
                code_lang = line[3:].strip().split()[0] if line[3:].strip() else ""
                code_lines = []
            else:
                in_code = False
                class_attr = f' class="language-{html.escape(code_lang)}"' if code_lang else ""
                out.append(f"<pre><code{class_attr}>{html.escape(chr(10).join(code_lines))}</code></pre>")
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not line.strip():
            flush_para()
            i += 1
            continue

        if line.strip() in {"---", "***", "___"}:
            flush_para()
            close_lists(out, list_stack)
            out.append("<hr/>")
            i += 1
            continue

        if i + 1 < len(lines) and "|" in line and is_table_separator(lines[i + 1]):
            flush_para()
            close_lists(out, list_stack)
            headers = split_table_row(line)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append(split_table_row(lines[i]))
                i += 1
            out.append("<table><thead><tr>" + "".join(f"<th>{parse_inline(h)}</th>" for h in headers) + "</tr></thead><tbody>")
            for row in rows:
                out.append("<tr>" + "".join(f"<td>{parse_inline(c)}</td>" for c in row) + "</tr>")
            out.append("</tbody></table>")
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            flush_para()
            close_lists(out, list_stack)
            level = len(heading.group(1))
            out.append(f"<h{level}>{parse_inline(heading.group(2).strip())}</h{level}>")
            i += 1
            continue

        image = re.match(r"^!\[([^\]]*)\]\(([^\)]+)\)$", line.strip())
        if image:
            flush_para()
            close_lists(out, list_stack)
            alt = html.escape(image.group(1), quote=True)
            src = html.escape(image.group(2), quote=True)
            out.append(f'<figure><img src="{src}" alt="{alt}"/><figcaption>{alt}</figcaption></figure>')
            i += 1
            continue

        if line.startswith("> "):
            flush_para()
            close_lists(out, list_stack)
            quote_lines = []
            while i < len(lines) and lines[i].startswith("> "):
                quote_lines.append(lines[i][2:].strip())
                i += 1
            out.append(f"<blockquote><p>{parse_inline(' '.join(quote_lines))}</p></blockquote>")
            continue

        ul = re.match(r"^\s*[-*]\s+(.*)$", line)
        ol = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if ul or ol:
            flush_para()
            kind = "ul" if ul else "ol"
            if not list_stack or list_stack[-1] != kind:
                close_lists(out, list_stack)
                out.append(f"<{kind}>")
                list_stack.append(kind)
            item = (ul or ol).group(1)
            out.append(f"<li>{parse_inline(item)}</li>")
            i += 1
            continue

        paragraph.append(line.strip())
        i += 1

    flush_para()
    close_lists(out, list_stack)
    if in_code:
        out.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
    return "\n".join(out)


def wrap_xhtml(title: str, body: str) -> str:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-Hant" lang="zh-Hant">
<head>
  <meta charset="utf-8"/>
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="../styles/book.css"/>
</head>
<body>
{body}
</body>
</html>
'''


def build_chapters() -> List[Chapter]:
    chapters: List[Chapter] = []
    for idx, path in enumerate(source_files(), start=1):
        raw = path.read_text(encoding="utf-8")
        title = first_heading(raw, path.stem)
        stem = f"{idx:02d}-{slugify(path)}"
        processed = replace_mermaid_blocks(raw, stem)
        body = markdown_to_body(processed)
        filename = f"{stem}.xhtml"
        chapters.append(Chapter(path, filename, title, wrap_xhtml(title, body)))
    return chapters


def write_static_files(chapters: Iterable[Chapter]) -> None:
    EPUB_WORK_DIR.mkdir(parents=True, exist_ok=True)
    OEBPS_DIR.mkdir(parents=True, exist_ok=True)
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    META_INF_DIR.mkdir(parents=True, exist_ok=True)

    (EPUB_WORK_DIR / "mimetype").write_text("application/epub+zip", encoding="ascii")
    (META_INF_DIR / "container.xml").write_text('''<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
''', encoding="utf-8")

    (OEBPS_DIR / "styles").mkdir(exist_ok=True)
    (OEBPS_DIR / "styles" / "book.css").write_text('''body { font-family: serif; line-height: 1.75; margin: 0 5%; color: #111827; }
h1, h2, h3 { line-height: 1.3; margin-top: 1.6em; }
h1 { font-size: 1.7em; border-bottom: 1px solid #d1d5db; padding-bottom: .35em; }
h2 { font-size: 1.35em; }
h3 { font-size: 1.15em; }
blockquote { border-left: 4px solid #93c5fd; margin-left: 0; padding-left: 1em; color: #374151; }
pre { background: #f3f4f6; padding: .9em; overflow-x: auto; white-space: pre-wrap; }
code { font-family: monospace; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: .9em; }
th, td { border: 1px solid #d1d5db; padding: .45em; vertical-align: top; }
th { background: #f3f4f6; }
figure { margin: 1.2em auto; text-align: center; page-break-inside: avoid; }
figcaption { font-size: .85em; color: #6b7280; margin-top: .35em; }
img { max-width: 100%; height: auto; }
''', encoding="utf-8")

    cover_src = DIST_DIR / "cover_1600x2400.jpg"
    if cover_src.exists():
        shutil.copy2(cover_src, IMAGES_DIR / "cover_1600x2400.jpg")

    for chapter in chapters:
        (CHAPTERS_DIR / chapter.filename).write_text(chapter.xhtml, encoding="utf-8")


def collect_image_assets() -> List[ImageAsset]:
    assets: List[ImageAsset] = []
    for path in sorted(IMAGES_DIR.rglob("*")):
        if path.is_file():
            rel = path.relative_to(OEBPS_DIR).as_posix()
            suffix = path.suffix.lower()
            if suffix in {".jpg", ".jpeg"}:
                media = "image/jpeg"
            elif suffix == ".png":
                media = "image/png"
            elif suffix == ".svg":
                media = "image/svg+xml"
            else:
                continue
            assets.append(ImageAsset(rel, media))
    return assets


def write_nav(chapters: List[Chapter]) -> None:
    toc = "\n".join(
        f'      <li><a href="chapters/{html.escape(ch.filename)}">{html.escape(ch.title)}</a></li>'
        for ch in chapters
    )
    (OEBPS_DIR / "nav.xhtml").write_text(f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-Hant" lang="zh-Hant">
<head>
  <meta charset="utf-8"/>
  <title>目錄</title>
  <link rel="stylesheet" type="text/css" href="styles/book.css"/>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>目錄</h1>
    <ol>
{toc}
    </ol>
  </nav>
</body>
</html>
''', encoding="utf-8")


def write_opf(chapters: List[Chapter]) -> None:
    image_assets = collect_image_assets()
    manifest_items = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '<item id="css" href="styles/book.css" media-type="text/css"/>',
    ]
    for i, chapter in enumerate(chapters, start=1):
        manifest_items.append(f'<item id="chap{i}" href="chapters/{html.escape(chapter.filename)}" media-type="application/xhtml+xml"/>')
    for i, asset in enumerate(image_assets, start=1):
        props = ' properties="cover-image"' if asset.href == "images/cover_1600x2400.jpg" else ""
        manifest_items.append(f'<item id="img{i}" href="{html.escape(asset.href)}" media-type="{asset.media_type}"{props}/>')

    spine_items = "\n".join(f'    <itemref idref="chap{i}"/>' for i, _ in enumerate(chapters, start=1))
    manifest_xml = "\n".join(f"    {item}" for item in manifest_items)
    modified = date.today().isoformat() + "T00:00:00Z"
    (OEBPS_DIR / "content.opf").write_text(f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{BOOK_ID}</dc:identifier>
    <dc:title>{html.escape(TITLE)}</dc:title>
    <dc:creator>{html.escape(AUTHOR)}</dc:creator>
    <dc:language>{LANGUAGE}</dc:language>
    <dc:publisher>{html.escape(AUTHOR)}</dc:publisher>
    <dc:description>{html.escape(SUBTITLE)}</dc:description>
    <meta property="dcterms:modified">{modified}</meta>
    <meta property="schema:version">{VERSION}</meta>
  </metadata>
  <manifest>
{manifest_xml}
  </manifest>
  <spine>
{spine_items}
  </spine>
</package>
''', encoding="utf-8")


def write_epub() -> Path:
    epub_path = DIST_DIR / "multi-agent-book-v1.0.0.epub"
    if epub_path.exists():
        epub_path.unlink()
    with zipfile.ZipFile(epub_path, "w") as zf:
        zf.write(EPUB_WORK_DIR / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(EPUB_WORK_DIR.rglob("*")):
            if path.name == "mimetype" or path.is_dir() or path.suffix == ".dot":
                continue
            rel = path.relative_to(EPUB_WORK_DIR).as_posix()
            zf.write(path, rel, compress_type=zipfile.ZIP_DEFLATED)
    return epub_path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if EPUB_WORK_DIR.exists():
        shutil.rmtree(EPUB_WORK_DIR)
    DIST_DIR.mkdir(exist_ok=True)

    print("==================================================")
    print("📚 開始建立 EPUB，並將 Mermaid 轉為 PNG 圖形")
    print("==================================================")
    chapters = build_chapters()
    write_static_files(chapters)
    write_nav(chapters)
    write_opf(chapters)
    epub_path = write_epub()
    mermaid_count = len(list(MERMAID_DIR.glob("*.png"))) if MERMAID_DIR.exists() else 0

    print(f"✅ EPUB 完成: {epub_path.relative_to(ROOT_DIR)}")
    print(f"✅ Mermaid 圖形: {mermaid_count} 張 PNG")
    print(f"✅ SHA256: {sha256_file(epub_path)}")


if __name__ == "__main__":
    main()
