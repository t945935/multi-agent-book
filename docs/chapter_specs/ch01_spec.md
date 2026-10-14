# 第 1 章技術規格書 (Chapter 1 Specification)

## 章節標題
**多 Agent 協同新範式：從單一 Chatbot 到自主工程團隊**

---

## 1. 章節學習目標
讀者閱讀本章後，應能夠：
1. 理解「單一 LLM 上下文膨脹（Context Bloat）」與「認知過載」的底層限制。
2. 掌握多 Agent 協同的三種主流通訊拓撲（Star / Pipeline / Peer-to-Peer）。
3. 實作一個不依賴笨重第三方龐大框架、僅使用 Python 標準庫與輕量 HTTP 的最簡多 Agent 消息總線（Message Bus）。

---

## 2. 正文大綱結構

* **1.1 單一 Agent 的黃金極限與崩塌點**
  * 1.1.1 上下文視窗（Context Window）的真實成本與注意力衰減（Lost in the Middle）。
  * 1.1.2 角色衝突難題：為什麼同一個 Agent 不能既是狂熱的「功能實現者」，又是挑剔的「安全審查員」？
* **1.2 多 Agent 協同的架構模式**
  * 1.2.1 集中式編排（Orchestrator-Worker Pattern）
  * 1.2.2 流水線式傳遞（Linear Pipeline Pattern）
  * 1.2.3 去中心化消息總線（Decentralized Message Bus）
* **1.3 核心合約設計：Agent 如何對話**
  * 1.3.1 結構化事件契約（Event Envelope）：Sender、Receiver、Topic、Payload。
  * 1.3.2 狀態轉換定義：PENDING -> RUNNING -> WAITING_INPUT -> COMPLETED / FAILED。
* **1.4 實戰項目：50 行程式碼打造第一個多 Agent 協同最小原型**
  * 1.4.1 架構設計：Planner Agent、Coder Agent 與 Reviewer Agent。
  * 1.4.2 程式碼實作與除錯。
  * 1.4.3 實機運行與觀察輸出。
* **1.5 本章小結與實務陷阱**
  * 死迴圈對話的熔斷機制（Circuit Breaker）設計。

---

## 3. 配套範例專案規格 (`examples/ch01_multi_agent_baseline/`)

* **專案目錄**：
  ```text
  examples/ch01_multi_agent_baseline/
  ├── README.md
  ├── pyproject.toml
  ├── agent_bus.py        # 輕量 Event/Message Bus 核心
  ├── agents.py           # Planner, Coder, Reviewer 具體 Agent 類別
  ├── main.py             # 協同流程演練入口
  └── test_baseline.py    # 自動化單元測試
  ```
* **技術棧**：Python 3.10+，僅使用標準庫 `dataclasses`、`asyncio`、`enum` 等模組。
* **驗收標準**：
  * `pytest test_baseline.py` 通過率 100%。
  * 具備防止 Agent 無限循環的 `max_turns` 熔斷機制。
