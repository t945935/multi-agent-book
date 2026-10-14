# v1.0 Release Checklist

本清單用於確認《多 Agent 系統架構與實戰》是否可以進入 v1.0 初版發布。公開上架仍需人工最終核准。

## 1. 內容檢查

- [x] 前言已建立：`src/preface.md`
- [x] 8 章正文已完成：`src/ch01.md` ~ `src/ch08.md`
- [x] 附錄已建立：`src/appendix.md`
- [x] 全書術語已依 `docs/style_guide.md` 統一
- [x] README 已說明專案結構與生產流程
- [x] 作者資訊已確認：Happy eBook Authors
- [x] 授權說明已建立：`LICENSE`
- [x] 版本歷史已建立：`CHANGELOG.md`
- [x] Google Play Books metadata 已建立：`docs/google_play_books_metadata.md`
- [x] Google Play Books 上架檢查清單已建立：`docs/google_play_books_checklist.md`
- [x] PRD 已建立：`docs/prd.md`
- [x] 章節規格已建立：`docs/chapter_specs/`

## 2. 範例與測試檢查

- [x] 每章皆有對應 examples 目錄
- [x] 每章 pytest 可獨立執行
- [x] 全書測試腳本存在：`scripts/test_all.sh`
- [x] `bash scripts/test_all.sh` 通過

## 3. QA 檢查

- [x] 8 份 QA 報告已更新：`qa/reports/ch*_review_report.md`
- [x] QA 報告包含正文完整度、測試、技術審查、文風審查與風險建議
- [x] QA 報告使用統一術語

## 4. 排版與產物檢查

- [x] Typst 模板存在：`templates/book.typ`、`templates/cover.typ`
- [x] 建置腳本存在：`scripts/build.py`
- [x] `dist/cover.pdf` 可產出
- [x] `dist/book_interior.pdf` 可產出
- [x] `dist/cover_1600x2400.jpg` 已存在，可作為上架封面素材

## 5. 發布包檢查

- [x] 打包腳本存在：`scripts/package_release.py`
- [x] release manifest 可產生：`dist/release_manifest.json`
- [x] release zip 可產生：`dist/multi-agent-book-v1.0.0.zip`
- [x] manifest 包含 artifacts、size、sha256、checks 與 notes

## 6. 人工核准檢查

公開上架前，仍需人工確認：

- [ ] PDF 版面逐頁抽查
- [ ] 封面視覺確認
- [ ] 上架文案確認
- [ ] 價格與平台欄位確認
- [x] 授權與作者資訊確認
- [ ] 最終公開上傳核准

## 7. 建議發布命令

```bash
bash scripts/test_all.sh
PATH="$PWD/bin:$PATH" python3 scripts/build.py
python3 scripts/package_release.py --version 1.0.0
python3 scripts/export_google_play_metadata.py
python3 scripts/validate_google_play_package.py
```
