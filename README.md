# 《多 Agent 系統架構與實戰》

> **副標題**：用 AI Agent 團隊完成寫作、測試、排版與發布  
> **作者**：Happy eBook Authors  
> **出版模式**：多 Agent 自動化協同創作實戰專案

---

## 讀者下載與快速開始

- GitHub repository: <https://github.com/t945935/multi-agent-book>
- v1.0.0 Release: <https://github.com/t945935/multi-agent-book/releases/tag/v1.0.0>

如果你只是閱讀電子書，可直接閱讀各章，不必先執行命令。若你想動手跑範例，請下載 release zip，解壓縮後執行：

```bash
cd multi-agent-book-v1.0.0/examples/ch01_multi_agent_baseline
python3 -m pytest
python3 main.py
```

若要驗證完整專案流程，回到 `multi-agent-book-v1.0.0/` 根目錄執行：

```bash
bash scripts/test_all.sh
PATH="$PWD/bin:$PATH" python3 scripts/build.py
python3 scripts/build_epub.py
python3 scripts/package_release.py --version 1.0.0
```

---

## 專案結構 (Project Structure)

```text
multi-agent-book/
├── docs/                     # 規格文件 (由 Hermes / Antigravity 維護)
│   ├── prd.md                # 書籍總規格說明書 (PRD)
│   ├── style_guide.md        # 全書文風與術語指南
│   ├── release_checklist.md  # v1.0 發布檢查清單
│   ├── store_listing.md      # 上架文案草稿
│   ├── google_play_books_metadata.md   # Google Play Books metadata
│   ├── google_play_books_checklist.md  # Google Play Books 上架檢查清單
│   └── chapter_specs/        # 各章詳細技術規格 (ch01_spec.md ~ ch08_spec.md)
├── src/                      # 書籍正文 Markdown (由 OpenCode 撰寫、Pi 精校)
│   ├── preface.md
│   ├── ch01.md
│   ├── ...
│   ├── ch08.md
│   └── appendix.md
├── examples/                 # 獨立可運行的專案程式碼 (由 Codex 唯一維護)
│   ├── ch01_multi_agent_baseline/
│   ├── ...
│   └── ch08_publishing_cicd/
├── assets/                   # 圖表與封面 (由 Antigravity 維護)
│   ├── covers/
│   └── diagrams/
├── templates/                # Typst 排版樣式與模板
│   ├── book.typ
│   └── cover.typ
├── scripts/                  # 建置、驗證與發布腳本
│   ├── build.py
│   ├── test_all.sh
│   ├── make_cover.py
│   ├── package_release.py
│   ├── export_google_play_metadata.py
│   └── validate_google_play_package.py
├── CHANGELOG.md             # 版本歷史
├── LICENSE                  # 書籍內容與範例程式碼授權說明
├── qa/reports/               # 審稿報告與程式碼驗收紀錄
└── dist/                     # 編譯成品 (PDF、EPUB、Release ZIP)
```

---

## Agent 分工與權限規範 (Agent Roles & Access Control)

| Agent | 角色職責 | 專屬操作目錄 / 權限邊界 |
| :--- | :--- | :--- |
| **Antigravity** | 總編排協調、CI/CD、封面素材生成 | `assets/`, `scripts/`, `.github/` |
| **Hermes** | 技術主編、邏輯審查、章節規格 | `docs/`, `qa/reports/` |
| **OpenCode** | 章節主筆 (Plan & Build 撰寫) | `src/*.md` |
| **Codex** | 程式碼範例研發與自動化測試 | `examples/`, `tests/` |
| **Pi** | 格式精修、標點校對、Typst 排版執行 | `src/` (以 patch/diff 精修), `templates/` |

---

## 生產流程快速指引

1. **規格制定**：Hermes 建立章節規格 (`docs/chapter_specs/chXX_spec.md`)。
2. **範例研發**：Codex 在 `examples/chXX_*` 實作專案程式碼，並確保 `test_all.sh` 全部通過。
3. **篇章寫作**：OpenCode 根據規格與已通過的範例程式碼撰寫 `src/chXX.md`。
4. **審校微調**：Hermes 依 `docs/style_guide.md` 進行深度邏輯與術語審查，Pi 進行文字潤飾與標點修正。
5. **排版發行**：執行 `python3 scripts/build.py` 編譯 Typst 產出 `dist/cover.pdf` 與 `dist/book_interior.pdf`。
6. **發布打包**：執行 `python3 scripts/package_release.py` 產生 `dist/release_manifest.json` 與 v1.0 release zip。
7. **Google Play 上架準備**：執行 `python3 scripts/export_google_play_metadata.py` 與 `python3 scripts/validate_google_play_package.py` 產生並檢查上架 metadata。

---

## 目前完成狀態

- 前言、8 章正文與附錄均已建立於 `src/`。
- 8 章規格均已建立於 `docs/chapter_specs/`。
- 8 組章節範例均已建立於 `examples/`。
- QA 報告已建立於 `qa/reports/`。
- `scripts/test_all.sh` 全數通過；`scripts/build.py` 可成功產出 PDF。
- `scripts/package_release.py` 可產生 release manifest 與 ZIP 發布包。
- 已建立 Google Play Books metadata、checklist 與 package validation 腳本。
