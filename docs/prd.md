# 書籍產品需求文件 (Product Requirement Document, PRD)

## 一、基本資訊
* **專案代號**：`book-multi-agent-system`
* **書名**：《多 Agent 系統架構與實戰：用 AI Agent 團隊完成寫作、測試、排版與發布》
* **發行格式**：v1.0 以 PDF (Typst 出版排版) 與配套範例程式碼為主；EPUB 作為後續版本規劃。
* **v1.0 字數目標**：25,000 ~ 35,000 字短版實戰電子書。
* **正式技術書版字數目標**：80,000 ~ 100,000 字。
* **章節總數**：8 章，另含前言與附錄

---

## 二、讀者設定與文風指南 (Voice & Tone)

1. **讀者定位**：
   * 具備中等以上 Python/TypeScript 基礎的軟體工程師。
   * 希望超越單一「Chat Prompting」，構建能夠自主運行、工具調度、監管並行的多 Agent 系統者。
2. **寫作文風與原則**：
   * **拒絕空洞理論**：每一章的核心概念必須有架構圖、時序圖，並緊隨真實可執行的程式碼。
   * **防禦性教學（Defensive Teaching）**：主動提示 Agent 在生產環境中的常見陷阱（如 Context 爆炸、死迴圈、互相覆寫檔案、Prompt 飄移）。
   * **語調嚴謹、接地氣、富工程美感**：繁體中文技術專業術語為主，英文專有名詞於首次出現時附上括弧對照（例：終端多工器（Terminal Multiplexer））。

---

## 三、程式碼規範契約 (Code Contract)

1. **可執行性保證（100% Executable Guarantee）**：
   * 書中出現的任何程式碼段落，必須直接來源於 `examples/` 對應專案檔案，嚴禁手動捏造。
2. **結構隔離**：
   * 每個章節的範例為獨立專案，包含自己的 `README.md`、依賴清單（`pyproject.toml` 或 `package.json`）及單元測試檔案。
3. **程式碼塊引用格式**：
   ```markdown
   ```python title="examples/ch01_multi_agent_baseline/agent.py"
   # 程式碼本體
   ```
   ```

---

## 四、全書章節進度追蹤表

| 章節 | 章名 | 範例程式碼目錄 | 狀態 | 主責 Agent |
| :--- | :--- | :--- | :--- | :--- |
| **Ch 01** | 多 Agent 協同新範式：從 Chatbot 到自主工程團隊 | `examples/ch01_multi_agent_baseline/` | 完成 (PASSED) | OpenCode / Codex |
| **Ch 02** | 終端多工與監管中樞：Herdr 架構與 Agent 狀態感知 | `examples/ch02_herdr_orchestration/` | 完成 (PASSED) | OpenCode / Codex |
| **Ch 03** | 極簡純粹的工程代理：Pi 的極簡哲學與微修實戰 | `examples/ch03_pi_agent_extension/` | 完成 (PASSED) | Pi / Codex |
| **Ch 04** | 雙模式架構實戰：OpenCode 的 Plan 與 Build 拆解 | `examples/ch04_opencode_workflow/` | 完成 (PASSED) | OpenCode / Hermes |
| **Ch 05** | 長程推理與反思中樞：Hermes Agent 的自主學習 | `examples/ch05_hermes_self_learning/` | 完成 (PASSED) | Hermes / Codex |
| **Ch 06** | 程式碼驗證沙盒：Codex 自動化測試與安全隔離 | `examples/ch06_sandbox_runner/` | 完成 (PASSED) | Codex / Hermes |
| **Ch 07** | 全流程編排實戰：用多 Agent 自動化產出科技書 | `examples/ch07_book_pipeline/` | 完成 (PASSED) | Antigravity / 全體 |
| **Ch 08** | 排版、封面生成與發布 CI/CD | `examples/ch08_publishing_cicd/` | 完成 (PASSED) | Codex / Pi / Antigravity |
