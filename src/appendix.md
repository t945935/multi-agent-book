# 附錄：全書命令速查與發布檢查

本附錄整理本書專案常用命令、Agent 分工與 v1.0 發布檢查清單，方便讀者在實作時快速查閱。

## A.1 常用命令速查

檢查 Python 與 pytest：

```bash
python3 --version
python3 -m pytest --version
```

執行全書範例測試：

```bash
bash scripts/test_all.sh
```

只執行單章測試，例如第 6 章：

```bash
cd examples/ch06_sandbox_runner
PYTHONPATH=. python3 -m pytest -v
```

建置封面與內文 PDF：

```bash
PATH="$PWD/bin:$PATH" python3 scripts/build.py
```

打包 release artifacts：

```bash
python3 scripts/package_release.py
```

檢查產物：

```bash
ls -lh dist/
```

## A.2 Agent 分工速查

| Agent | 主要責任 | 主要目錄 | 驗收方式 |
|---|---|---|---|
| Herdr | 終端多工、狀態監管、人工接管提示 | 外部監管層 / dashboard | 狀態正確、阻塞可見 |
| Pi | 微修、標點、Markdown / Typst 精修 | `src/`, `templates/` | diff 小、build 通過 |
| OpenCode | Plan / Build、章節主筆、任務合約 | `src/` | 章節符合規格 |
| Hermes | 技術主編、長程記憶、QA 審稿 | `docs/`, `qa/reports/` | QA 報告通過 |
| Codex | 範例程式碼、測試、沙盒驗證 | `examples/`, `scripts/test_all.sh` | pytest 通過 |
| Antigravity | 總編排、發布、封面與 CI/CD | `scripts/`, `dist/`, `assets/` | release artifacts 完整 |

## A.3 v1.0 發布檢查清單

內容面：

- [x] 8 章正文已完成。
- [x] 前言與附錄已建立。
- [x] 每章都有對應 examples 目錄。
- [x] 每章 QA 報告已更新。
- [x] 術語已依 `docs/style_guide.md` 統一。

程式面：

- [x] `scripts/test_all.sh` 全部通過。
- [x] 每章 pytest 可獨立執行。
- [x] 範例使用 Python 標準庫為主，降低安裝負擔。

排版面：

- [x] `scripts/build.py` 可產出 `dist/cover.pdf`。
- [x] `scripts/build.py` 可產出 `dist/book_interior.pdf`。
- [x] Typst 字型警告已修正。
- [x] 封面 JPG 已產出，可作為上架素材。

發布面：

- [x] `scripts/package_release.py` 可產生 release manifest。
- [x] release zip 包含 PDF、封面、README、QA 與規格文件。
- [x] checksum 可用於確認 artifacts 未被竄改。
- [ ] 正式公開上架前，仍需人工最終核准。

## A.4 常見問題排除

若 pytest 找不到模組，請確認在章節 examples 目錄中執行，並設定：

```bash
PYTHONPATH=.
```

若 Typst 找不到，請確認 `typst` 已安裝，或使用專案內 `bin/typst`：

```bash
PATH="$PWD/bin:$PATH" python3 scripts/build.py
```

若 PDF build 失敗，請先查看 `dist/book_interior.typ` 附近錯誤行，再回到對應 `src/chXX.md` 修正 Markdown 或特殊符號。

若 release zip 缺少檔案，請先重新執行測試與 build，再執行：

```bash
python3 scripts/package_release.py
```

## A.5 建議學習路線

不同讀者可以用不同順序閱讀：

| 讀者類型 | 建議順序 | 重點 |
|---|---|---|
| 初學者 | 第 1 章 → 第 2 章 → 第 3 章 → 第 6 章 → 第 7 章 → 第 8 章 | 先建立多 Agent、監管、微修與測試觀念，再看整合與發布。 |
| 專案管理者 | 第 1 章 → 第 4 章 → 第 5 章 → 第 7 章 → 第 8 章 | 聚焦任務合約、品質管理、流程與發布。 |
| 工程實作者 | 第 3 章 → 第 4 章 → 第 6 章 → 第 8 章 | 聚焦微修、Plan / Build、沙盒測試與打包。 |
| 技術主編 | 第 5 章 → `docs/style_guide.md` → `qa/reports/` → 第 7 章 | 聚焦術語、審稿、記憶規則與品質閘門。 |

## A.6 下一步延伸

v1.0 完成後，可以考慮：

1. 增加 EPUB 輸出。
2. 加入 GitHub Actions。
3. 將 QA 報告轉成 JSON metadata。
4. 為 Herdr 與 OpenCode 補真實操作截圖。
5. 將每章擴充到正式技術書篇幅。
