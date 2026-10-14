# 第 6 章 Codex 驗證沙盒

本範例示範如何用沙盒包裝命令執行，捕捉 stdout/stderr、return code 與 timeout，並摘要為 PASS、FAIL 或 TIMEOUT。

## 學習目標

- 理解可測試範例與文件範例的差異。
- 學會保留 stdout、stderr、return code 與 timeout 狀態。
- 理解為什麼多 Agent 系統不能盲目執行任意命令。

## 主要檔案

- `sandbox.py`：SandboxResult、validate_command、run_command 與 summarize。
- `test_baseline.py`：驗證成功命令、失敗命令、危險命令拒絕與 timeout 摘要。

## 執行測試

```bash
PYTHONPATH=. python3 -m pytest -v
```

## 觀察重點

- return code 0 會摘要為 PASS。
- return code 非 0 會摘要為 FAIL。
- timeout 應被視為獨立狀態，而不是普通失敗。
- `validate_command()` 會拒絕 `sudo`、`rm`、`mkfs`、`shutdown` 等高風險命令。
- stdout/stderr 應保留給後續診斷。

## 延伸練習

1. 為 `run_command` 增加 `cwd` 參數。
2. 擴充 denylist，支援 `rm -rf` 這類組合規則。
3. 將 stdout/stderr 截斷到固定長度，避免 log 過大。
4. 將測試結果輸出成 JSON 摘要。
