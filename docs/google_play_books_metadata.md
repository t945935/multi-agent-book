# Google Play Books 上架 Metadata

本文件整理《多 Agent 系統架構與實戰》在 Google Play Books 上架時建議使用的欄位。公開送審前仍需人工最終確認。

## 基本資訊

| 欄位 | 建議值 |
|---|---|
| 書名 | 多 Agent 系統架構與實戰 |
| 副標題 | 用 AI Agent 團隊完成寫作、測試、排版與發布 |
| 作者 | Happy eBook Authors |
| 語言 | 繁體中文（zh-TW） |
| 版本 | v1.0.0 |
| 格式 | PDF |
| 是否含程式碼 | 是，附配套 examples 與 release package |
| 是否需要 ISBN | v1.0 可先不填；若正式商業出版建議申請 |
| DRM 建議 | 視銷售策略決定；若啟用 DRM，需在上架前人工確認 |

## 作者簡介

Happy eBook Authors 是一個專注於 AI 輔助寫作、技術出版自動化與數位學習內容製作的創作團隊。團隊致力於把 AI 工具落地為可驗證、可重跑、可維護的出版流程，涵蓋選題、規格、範例程式碼、審稿、排版、封面與上架素材。

## 短書介

一本以真實出版流水線為案例的多 Agent 實戰電子書。從 Herdr 監管中樞、Pi 微修、OpenCode Plan / Build、Hermes 反思審稿、Codex 測試沙盒，到 Typst 排版與 release manifest，帶你把 AI Agent 從單次問答推進到可驗證、可建置、可發布的工程流程。

## 長書介

AI Agent 不應只是更會聊天的工具。當任務變成寫一本書、開發一組範例、執行測試、審稿、排版與上架時，單一 Chatbot 很快會遇到上下文膨脹、角色衝突、驗證不足與修改範圍失控等問題。

《多 Agent 系統架構與實戰》以一個自我指涉的專案為主軸：用多 Agent 團隊製作一本介紹多 Agent 系統的科技書。全書不只談概念，也提供可執行的 Python 範例、pytest 測試、Typst 排版模板、QA 報告與 release 打包流程。

你將學到：

- 為什麼單一 Agent 會在長程工程任務中失效。
- 如何使用 Herdr 型監管中樞觀察多個代理狀態。
- 如何用 Pi 的微修哲學降低大範圍修改風險。
- 如何用 OpenCode 的 Plan / Build 模式管理大型任務。
- 如何用 Hermes 的長程記憶與審稿報告維持品質。
- 如何用 Codex 的測試沙盒確保範例程式碼可執行。
- 如何把規格、範例、正文、審稿、排版與發布串成出版流水線。
- 如何產生 PDF、release manifest 與發布包。

本書適合已經使用過 AI coding 工具，並希望把 AI Agent 用在長程專案、技術寫作、自動化出版或工程流程管理的讀者。

## 分類建議

### 主分類

- Computers / Artificial Intelligence

### 次分類

- Computers / Software Development & Engineering / General
- Computers / Programming / General
- Computers / Electronic Publishing

## 關鍵字

AI Agent, Multi-Agent, 多 Agent, AI coding, Herdr, Pi, OpenCode, Hermes, Codex, Antigravity, Typst, CI/CD, 技術寫作, 自動化出版, Python, pytest, release manifest, 電子書出版

## 定價建議

### 正式定價

| 市場 | 建議價格 |
|---|---:|
| 台灣 | NT$199 |
| 美國 / 國際 | US$5.99 |
| 日本 | ¥900 |
| 香港 | HK$48 |
| 新加坡 | S$7.99 |

### 首發促銷價

| 市場 | 建議價格 |
|---|---:|
| 台灣 | NT$149 |
| 美國 / 國際 | US$4.99 |
| 日本 | ¥700 |
| 香港 | HK$38 |
| 新加坡 | S$6.99 |

## 上架檔案

| 用途 | 檔案 |
|---|---|
| 內文 PDF | `dist/book_interior.pdf` |
| 封面 PDF | `dist/cover.pdf` |
| 封面 JPG | `dist/cover_1600x2400.jpg` |
| Release manifest | `dist/release_manifest.json` |
| 發布包 | `dist/multi-agent-book-v1.0.0.zip` |

## 風險提醒

- 不建議自動按下 Publish；應先建立草稿並人工確認。
- 價格、銷售區域、DRM 與 ISBN 欄位應人工核准。
- 若平台要求 EPUB，目前 v1.0 尚未提供，需列為後續工作。
