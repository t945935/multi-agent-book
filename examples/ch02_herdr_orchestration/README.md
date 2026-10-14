# 第 2 章 Herdr 監管中樞

本範例不是 Herdr 本體，而是用 Python 模擬 Herdr 型監管中樞的核心邏輯：將終端 pane 的文字輸出轉換成狀態快照，並產生 dashboard 統計。

## 學習目標

- 理解 `IDLE`、`RUNNING`、`BLOCKED`、`DONE` 四種狀態。
- 學會把非結構化終端輸出轉成 `PaneSnapshot`。
- 理解 dashboard 如何幫助監管者快速找出阻塞任務。

## 主要檔案

- `herdr.py`：PaneState、PaneSnapshot 與 HerdrSupervisor。
- `test_baseline.py`：驗證狀態判斷、告警與 dashboard 統計。

## 執行測試

```bash
PYTHONPATH=. python3 -m pytest -v
```

## 互動觀察

可在 Python REPL 中嘗試：

```python
from herdr import HerdrSupervisor

h = HerdrSupervisor()
h.ingest("pane-1", "Codex", "tests passed")
h.ingest("pane-2", "OpenCode", "waiting for input")
print(h.dashboard())
```

你應該會看到 DONE 與 BLOCKED 的統計。

## 觀察重點

- `waiting for input` 與 `blocked` 會被判定為 `BLOCKED`。
- `done` 與 `passed` 會被判定為 `DONE`。
- `error` 與 `failed` 會增加 `needs_attention` 告警。

## 延伸練習

1. 新增 `FAILED` 狀態。
2. 為 `PaneSnapshot` 增加 `updated_at`。
3. 新增 `needs_attention()` 方法，列出所有需要人工檢查的 pane。
