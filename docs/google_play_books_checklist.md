# Google Play Books 上架檢查清單

本清單用於 Google Play Books Partner Center 上架前檢查。自動化流程只應協助產生草稿與填表，公開送審前必須人工核准。

## 1. 檔案檢查

- [x] 內文 PDF 存在：`dist/book_interior.pdf`
- [x] 封面 PDF 存在：`dist/cover.pdf`
- [x] 封面 JPG 存在：`dist/cover_1600x2400.jpg`
- [x] Release manifest 存在：`dist/release_manifest.json`
- [x] Release ZIP 存在：`dist/multi-agent-book-v1.0.0.zip`
- [x] ZIP 包含 README、LICENSE、CHANGELOG、QA 報告與文件

## 2. Metadata 檢查

- [x] 書名：多 Agent 系統架構與實戰
- [x] 副標題：用 AI Agent 團隊完成寫作、測試、排版與發布
- [x] 作者：Happy eBook Authors
- [x] 作者簡介已準備
- [x] 短書介已準備
- [x] 長書介已準備
- [x] 分類建議已準備
- [x] 關鍵字已準備
- [x] 授權摘要已準備

## 3. 分類檢查

建議分類：

- [x] Computers / Artificial Intelligence
- [x] Computers / Software Development & Engineering / General
- [x] Computers / Programming / General
- [x] Computers / Electronic Publishing

Google Play Books 後台若分類名稱不同，應選擇最接近的「人工智慧」、「軟體開發」、「程式設計」、「電子出版」類別。

## 4. 定價檢查

正式建議價：

- [x] TWD 199
- [x] USD 5.99
- [x] JPY 900
- [x] HKD 48
- [x] SGD 7.99

首發促銷價，可選：

- [ ] TWD 149
- [ ] USD 4.99
- [ ] JPY 700
- [ ] HKD 38
- [ ] SGD 6.99

## 5. 人工核准項目

以下項目不得全自動提交：

- [ ] 最終 Publish / Submit 按鈕
- [ ] 價格與幣別
- [ ] 銷售國家 / 地區
- [ ] DRM 設定
- [ ] ISBN 或書籍 ID
- [ ] 稅務、付款或帳戶資訊
- [ ] 刪除或覆蓋既有書籍版本

## 6. 建議半自動流程

1. 執行全書測試。
2. 建置 PDF。
3. 產生 release manifest 與 ZIP。
4. 執行 Google Play package validation。
5. 匯出 Google Play metadata JSON。
6. 使用 Browser Agent / OpenCLI 登入 Partner Center。
7. 建立新書草稿。
8. 上傳 PDF 與封面。
9. 填入 metadata、分類與定價。
10. 儲存草稿。
11. 人工檢查預覽、價格、區域、DRM。
12. 人工按下提交。

## 7. 建議命令

```bash
bash scripts/test_all.sh
PATH="$PWD/bin:$PATH" python3 scripts/build.py
python3 scripts/package_release.py --version 1.0.0
python3 scripts/validate_google_play_package.py
python3 scripts/export_google_play_metadata.py
```
