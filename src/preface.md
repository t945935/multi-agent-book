# 前言：為什麼用多 Agent 寫一本多 Agent 書

生成式 AI 已經從問答工具，逐步變成能讀檔、改程式、執行命令、產出文件的工程協作者。可是，當任務從「回答一個問題」變成「完成一個長程專案」時，單一 Chatbot 很快會遇到限制：上下文太大、角色衝突、驗證不足、修改範圍失控，以及缺少可追蹤交付物。

本書選擇一個自我指涉的實戰題目：用多 Agent 團隊，製作一本介紹多 Agent 系統的科技書。這個題目同時包含規格制定、程式範例、正文寫作、技術審稿、排版建置、封面與發布流程，剛好能展示多 Agent 協作的完整生命週期。

本書不追求一次介紹所有 AI Agent 框架，也不把模型能力神化。相反地，本書關注工程化問題：如何分工、如何限制權限、如何驗證結果、如何記錄決策、如何在出錯時停止，以及如何把產物做成可重跑的發布流程。

## 作者簡介

**Happy eBook Authors** 是一個專注於 AI 輔助寫作、技術出版自動化與數位學習內容製作的創作團隊。團隊關注如何把 AI 工具真正落地到可交付的出版流程中：從選題、規格、範例程式碼、審稿、排版、封面到上架素材，皆以可驗證、可重跑、可維護為核心原則。

在本書中，Happy eBook Authors 以「用多 Agent 團隊製作一本多 Agent 書」作為實驗場，示範如何把 AI Agent 從單次問答工具，組織成能協作、能審查、能測試、能發布的工程化團隊。這也代表團隊的出版理念：電子書不只是靜態內容，而可以是一個包含程式碼、測試、排版與 release artifacts 的可持續產品。

## 本書適合誰

本書適合以下讀者：

- 已經使用過 ChatGPT、Claude、Codex、OpenCode 或其他 AI coding 工具的工程師。
- 想把 AI Agent 用於長程專案，而不只是單次問答的人。
- 想自動化科技寫作、審稿、排版與發布流程的作者。
- 想理解 Herdr、Pi、OpenCode、Hermes、Codex 與 Antigravity 如何分工協作的人。
- 想把多 Agent 概念落地成可測試範例與可建置產物的實作者。

## 本書不適合誰

本書不適合以下需求：

- 完全沒有命令列與 Python 經驗的初學者。
- 只想閱讀 AI 概念，而不想執行範例程式碼的人。
- 期待完整 LLM 數學理論或模型訓練教材的人。
- 期待所有流程都能無人工審查、完全自動上架的人。

## 如何閱讀本書

建議閱讀方式如下：

1. 先讀第 1 章，理解為什麼需要多 Agent 分工。
2. 讀第 2 章，建立監管中樞與狀態觀念。
3. 讀第 3 至第 6 章，理解 Pi、OpenCode、Hermes、Codex 各自的角色。
4. 讀第 7 章，把前面角色串成出版流水線。
5. 讀第 8 章，完成排版、發布與 release manifest。
6. 回到 `examples/` 目錄，逐章執行測試。

如果你是專案負責人，可以優先閱讀第 1、2、7、8 章；如果你是工程實作者，可以優先閱讀第 3、4、6 章；如果你負責品質管理，可以優先閱讀第 5 章與 `qa/reports/`。

## 如何使用本書中的程式碼

本書中的程式碼不是要求讀者逐段複製貼上。閱讀時，請先把程式碼當作架構說明的一部分，用來理解 Agent 之間如何通訊、驗證與交付。

書中程式碼大致分成三類：

1. **概念片段**：出現在章節正文中，用來說明資料結構、狀態機、品質閘門或流程設計。這類程式碼以理解為主，不一定需要立即執行。
2. **完整範例專案**：放在 GitHub release zip 的 `examples/` 目錄。若你想實際執行，請下載範例專案包，進入對應的 `examples/chXX_*` 目錄執行。
3. **維護者腳本**：放在 `scripts/` 目錄，用於驗證全書範例、產生 PDF/EPUB、打包 release。這些命令適合進階讀者或專案維護者，不是第一次閱讀時的必要步驟。

簡單來說：一般讀者先看懂即可；想實作的讀者下載 GitHub 範例專案後跑 `examples/`；想重現出版流程的讀者再使用 `scripts/`。

## 最短上手路徑

如果你是第一次閱讀本書，不需要一開始就跑完整發布流程，也不需要立刻準備整個專案目錄。建議先閱讀第 1 章的程式片段，理解 `MessageEnvelope`、`MessageBus`、`PlannerAgent`、`CoderAgent` 與 `ReviewerAgent` 如何協作。

如果你想動手執行範例，請先到 GitHub 下載本書範例專案包：

- GitHub repository: `https://github.com/t945935/multi-agent-book`
- Release zip: `https://github.com/t945935/multi-agent-book/releases/tag/v1.0.0`

下載並解壓縮 release zip 後，再進入專案目錄執行最小範例：

```bash
cd multi-agent-book-v1.0.0/examples/ch01_multi_agent_baseline
python3 -m pytest
python3 main.py
```

這兩個命令會驗證第 1 章範例，並執行一個最小多 Agent 協同流程。若你只是透過電子書閱讀器閱讀，沒有下載範例專案包，可以先略過命令；每章會用文字說明核心設計，命令只是給想動手驗證的讀者使用。

如果你是專案維護者，或想確認整本書從範例、排版到發布打包都能重現，再回到範例專案根目錄執行完整驗證：

```bash
bash scripts/test_all.sh
PATH="$PWD/bin:$PATH" python3 scripts/build.py
python3 scripts/build_epub.py
python3 scripts/package_release.py --version 1.0.0
```

這組命令會分別驗證全書範例、建置 PDF、產生 EPUB，並建立 release manifest 與 ZIP 發布包。它不是讀者的第一個必要步驟，而是本書專案的端到端健康檢查。

## 執行環境

本書範例以 Python 3.12 與標準庫為主，盡量降低外部依賴。建議環境：

- Linux 或 macOS shell 環境。
- Python 3.12 以上。
- pytest。
- Typst，用於產生 PDF。

在本專案中，可使用下列命令驗證全書範例：

```bash
bash scripts/test_all.sh
```

產出 PDF：

```bash
PATH="$PWD/bin:$PATH" python3 scripts/build.py
```

打包發布檔：

```bash
python3 scripts/package_release.py
```

## 本書的限制

本書採取最小可執行範例，而不是完整商業平台實作。許多範例故意保持短小，目的是讓讀者看懂核心合約、狀態模型與品質閘門。若要投入生產環境，仍需補上更完整的權限控管、日誌保存、機密管理、CI/CD runner、錯誤追蹤與人工核准流程。

本書真正想傳達的不是某個單一工具，而是一種工程化思維：讓 AI Agent 在清楚角色、明確邊界、可驗證交付與可停止流程中協作。這也是後續所有章節的共同基礎。
