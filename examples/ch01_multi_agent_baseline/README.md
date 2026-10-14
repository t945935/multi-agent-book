# 第 1 章 多 Agent 協同最小原型

本範例示範如何用 Python 標準庫建立最小多 Agent 協作流程：Planner 產生計劃，Coder 根據計劃產生程式碼，Reviewer 進行審查，MessageBus 負責事件傳遞。

## 學習目標

- 理解 Message Bus 如何用 topic 串接不同 Agent。
- 觀察 Planner、Coder、Reviewer 的最小分工。
- 理解為什麼需要 `max_turns` 熔斷機制避免無限對話。

## 主要檔案

- `agent_bus.py`：訊息信封與非同步 Message Bus。
- `agents.py`：PlannerAgent、CoderAgent、ReviewerAgent。
- `main.py`：串起三個 Agent 的示範入口。
- `test_baseline.py`：驗證訊息路由、協作流程與熔斷器。

## 執行示範

```bash
PYTHONPATH=. python3 main.py
```

## 執行測試

```bash
PYTHONPATH=. python3 -m pytest -v
```

## 觀察重點

- `MessageBus.subscribe()` 如何建立 topic 與 handler 的關係。
- `PlannerAgent` 如何產生 `task.plan`。
- `CoderAgent` 如何接收計劃並產生 `task.code`。
- `ReviewerAgent` 如何審查程式碼並產生決策。
- `test_circuit_breaker` 如何避免 Agent 反覆互相要求修改。

## 延伸練習

1. 新增 `SecurityAuditorAgent`，讓它也訂閱 `task.code`。
2. 為 `MessageEnvelope` 增加 `priority` 欄位。
3. 嘗試讓 Reviewer 在第一次審查時拒絕，第二次才通過。
