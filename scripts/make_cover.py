#!/usr/bin/env python3
"""
專業出版級 1600x2400 書籍封面合成腳本 (Cover Generation Script)
負責人：Codex (代碼工程師)
版本：完美平衡版（取 V1 極簡自然流暢 與 V2 高對比清晰度 兩者的中間值）
- 移除生硬厚重的科技大框線與膠囊框，回歸大氣通透的封面設計
- 保留適度字重（Bold 750）與柔和環境暗影，確保主副標自然、清晰、不刺眼、不雜亂
- 底部「Happy eBook Authors」以經典大器排版呈現
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT_DIR = Path(__file__).resolve().parent.parent
BG_IMAGE_PATH = ROOT_DIR / "assets" / "covers" / "background_art.jpg"
OUTPUT_PNG = ROOT_DIR / "assets" / "covers" / "cover_1600x2400.png"
OUTPUT_DIST_JPG = ROOT_DIR / "dist" / "cover_1600x2400.jpg"

TARGET_WIDTH = 1600
TARGET_HEIGHT = 2400

FONT_VF_PATH = "/home/j5/.local/share/fonts/NotoSansTC-VF.ttf"
FONT_CJK_REGULAR = "/home/j5/.local/share/fonts/NotoSansCJKtc-Regular.otf"

FONT_EN_CANDIDATES = [
    "/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def get_cjk_font(size: int, weight: int = 750):
    """適中字重：750 (優雅平衡的 Bold，不顯單薄，也不會過度粗笨)"""
    if os.path.exists(FONT_VF_PATH):
        try:
            font = ImageFont.truetype(FONT_VF_PATH, size)
            if hasattr(font, "set_variation_by_axes"):
                font.set_variation_by_axes([weight])
            return font
        except Exception:
            pass
    if os.path.exists(FONT_CJK_REGULAR):
        return ImageFont.truetype(FONT_CJK_REGULAR, size)
    return ImageFont.load_default()


def get_en_font(size: int, weight: int = 600):
    for path in FONT_EN_CANDIDATES:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, size)
                if hasattr(font, "set_variation_by_axes"):
                    try:
                        font.set_variation_by_axes([weight])
                    except Exception:
                        pass
                return font
            except Exception:
                continue
    return ImageFont.load_default()


def create_balanced_gradient_mask(width, height, top_fade=900, bottom_fade=600):
    """自然柔和的暗角過渡，既保留底圖璀璨細節，又為文字提供足夠對比度"""
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # 頂部柔和漸層
    for y in range(top_fade):
        ratio = 1.0 - (y / top_fade)
        alpha = int(215 * (ratio ** 1.3))
        draw.line([(0, y), (width, y)], fill=alpha)

    # 底部柔和漸層
    for y in range(height - bottom_fade, height):
        ratio = (y - (height - bottom_fade)) / bottom_fade
        alpha = int(210 * (ratio ** 1.3))
        draw.line([(0, y), (width, y)], fill=alpha)

    return mask


def draw_glow_text(draw, position, text, font, fill_color, glow_color=(5, 12, 28, 220), radius=5):
    """繪製自然柔和的文字背部漫反射光暈，取代生硬外框線"""
    x, y = position
    # 多向微移形成自然陰影暈染
    for dx in range(-radius, radius + 1, 2):
        for dy in range(-radius, radius + 1, 2):
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=font, fill=glow_color)
    # 底部重陰影
    draw.text((x + 2, y + 4), text, font=font, fill=(0, 0, 0, 240))
    # 正文字體
    draw.text((x, y), text, font=font, fill=fill_color)


def main():
    print("==================================================")
    print("🎨 Codex 正在生成 1600x2400 平衡優雅版封面 (中間值)")
    print("==================================================")

    if not BG_IMAGE_PATH.exists():
        raise FileNotFoundError(f"未找到背景底圖: {BG_IMAGE_PATH}")

    # 1. 載入並高品質縮放背景
    bg = Image.open(BG_IMAGE_PATH).convert("RGBA")
    bg = bg.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)

    # 2. 疊加自然柔和的環境暗光（無生硬邊框，自然通透）
    dark_overlay = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (6, 12, 25, 255))
    mask = create_balanced_gradient_mask(TARGET_WIDTH, TARGET_HEIGHT, top_fade=920, bottom_fade=620)
    bg.paste(dark_overlay, (0, 0), mask)

    draw = ImageDraw.Draw(bg)

    # 3. 字型選定 (取適中字級與適中字重)
    font_tag = get_en_font(30, weight=600)
    font_title = get_cjk_font(114, weight=750)       # 兼顧清晰與優雅的 114 級 Bold 750
    font_subtitle = get_cjk_font(50, weight=600)    # 50 級 Medium-Bold
    font_badges = get_en_font(26, weight=500)
    font_authors = get_en_font(56, weight=700)      # 經典大器署名
    font_sub_authors = get_en_font(23, weight=400)

    # =========================================================
    # [頂部小標籤 - 輕盈優雅的雙點科技排版]
    # =========================================================
    tag_text = "•  AUTONOMOUS MULTI-AGENT SWARM  •"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
    tag_w = tag_bbox[2] - tag_bbox[0]
    tag_x = (TARGET_WIDTH - tag_w) // 2
    tag_y = 220
    draw.text((tag_x, tag_y), tag_text, font=font_tag, fill=(56, 189, 248, 230))

    # =========================================================
    # [主標題 - 自然通透、字體飽滿、不加生硬大外框]
    # =========================================================
    title_text = "多 Agent 系統架構與實戰"
    title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    title_x = (TARGET_WIDTH - title_w) // 2
    title_y = 350

    print("▶ 繪製平衡版主標題 (字號 114, Bold 750, 柔和暗影光暈)...")
    draw_glow_text(
        draw,
        position=(title_x, title_y),
        text=title_text,
        font=font_title,
        fill_color=(255, 255, 255, 255),
        glow_color=(4, 10, 22, 230),
        radius=4
    )

    # =========================================================
    # [副標題 - 簡約細膩的冰青白，不加厚重膠囊]
    # =========================================================
    subtitle_text = "用 AI Agent 團隊完成寫作、測試、排版與發布"
    sub_bbox = draw.textbbox((0, 0), subtitle_text, font=font_subtitle)
    sub_w = sub_bbox[2] - sub_bbox[0]
    sub_x = (TARGET_WIDTH - sub_w) // 2
    sub_y = title_y + 175

    print("▶ 繪製平衡版副標題 (字號 50, 冰青白, 優雅居中)...")
    draw_glow_text(
        draw,
        position=(sub_x, sub_y),
        text=subtitle_text,
        font=font_subtitle,
        fill_color=(205, 235, 255, 250),
        glow_color=(4, 10, 22, 220),
        radius=3
    )

    # =========================================================
    # [中央科技裝飾纖細分割線 (極致纖細 1.5px，輕巧點綴)]
    # =========================================================
    line_y = sub_y + 110
    line_w = 460
    line_x1 = (TARGET_WIDTH - line_w) // 2
    line_x2 = line_x1 + line_w
    draw.line([(line_x1, line_y), (line_x2, line_y)], fill=(56, 189, 248, 160), width=2)
    # 中心發光小圓點
    dot_r = 4
    cx = TARGET_WIDTH // 2
    draw.ellipse([(cx - dot_r, line_y - dot_r), (cx + dot_r, line_y + dot_r)], fill=(129, 140, 248, 240))

    # [中下部輕量技術關鍵字]
    feature_text = "HERDR  •  OPENCODE  •  NOUS HERMES  •  CODEX  •  PI  •  CI/CD"
    feat_bbox = draw.textbbox((0, 0), feature_text, font=font_badges)
    feat_w = feat_bbox[2] - feat_bbox[0]
    feat_x = (TARGET_WIDTH - feat_w) // 2
    feat_y = line_y + 45
    draw.text((feat_x, feat_y), feature_text, font=font_badges, fill=(148, 163, 184, 210))

    # =========================================================
    # [下方作者署名區 - Happy eBook Authors (大器優雅、無多餘大卡片框)]
    # =========================================================
    print("▶ 繪製大器優雅版作者署名: Happy eBook Authors ...")
    author_text = "Happy eBook Authors"
    auth_bbox = draw.textbbox((0, 0), author_text, font=font_authors)
    auth_w = auth_bbox[2] - auth_bbox[0]
    auth_x = (TARGET_WIDTH - auth_w) // 2
    auth_y = TARGET_HEIGHT - 320

    # 輕盈柔和的底部分隔微光線
    top_author_line_y = auth_y - 35
    top_line_w = 300
    draw.line([((TARGET_WIDTH - top_line_w) // 2, top_author_line_y), ((TARGET_WIDTH + top_line_w) // 2, top_author_line_y)], fill=(56, 189, 248, 120), width=1)

    # 繪製主作者名 (純白立體投影，極簡經典)
    draw_glow_text(
        draw,
        position=(auth_x, auth_y),
        text=author_text,
        font=font_authors,
        fill_color=(255, 255, 255, 255),
        glow_color=(4, 10, 22, 230),
        radius=3
    )

    # 底部版本標註
    pub_text = "FIRST EDITION · FULLY AUTOMATED CI/CD PUBLICATION"
    pub_bbox = draw.textbbox((0, 0), pub_text, font=font_sub_authors)
    pub_w = pub_bbox[2] - pub_bbox[0]
    pub_x = (TARGET_WIDTH - pub_w) // 2
    pub_y = auth_y + 75
    draw.text((pub_x, pub_y), pub_text, font=font_sub_authors, fill=(148, 163, 184, 220))

    # =========================================================
    # 輸出成品
    # =========================================================
    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIST_JPG.parent.mkdir(parents=True, exist_ok=True)

    final_rgb = bg.convert("RGB")
    final_rgb.save(OUTPUT_PNG, format="PNG", optimize=True)
    final_rgb.save(OUTPUT_DIST_JPG, format="JPEG", quality=96, dpi=(300, 300))

    artifact_cover = Path("/home/j5/.gemini/antigravity-cli/brain/a195a1f7-b4e6-4dbd-b660-35525158b03e/cover_1600x2400.png")
    final_rgb.save(artifact_cover, format="PNG", optimize=True)

    print(f"✅ 平衡版封面生成完畢:")
    print(f"   - {OUTPUT_PNG}")
    print(f"   - {OUTPUT_DIST_JPG}")
    print(f"   - {artifact_cover}")
    print("==================================================")


if __name__ == "__main__":
    main()
