# 第 7 章 出版流水線

本範例示範如何用 Stage 與依賴關係描述書籍出版流程，並用品質閘門決定是否能發布。

## 學習目標

- 理解 spec、example、draft、review、build、release 的階段關係。
- 學會根據已完成階段計算下一個 ready stage。
- 理解 tests、review、build 必須同時通過才可進入發布。

## 主要檔案

- `pipeline.py`：Stage、default_stages、ready_stages 與 quality_gate。
- `test_baseline.py`：驗證階段依賴與品質閘門。

## 執行測試

```bash
PYTHONPATH=. python3 -m pytest -v
```

## 狀態表示例

| 階段 | 狀態 | 負責 Agent | 驗收 |
|---|---|---|---|
| spec | done | Hermes | PRD / 章節規格存在 |
| example | done | Codex | pytest 通過 |
| draft | done | OpenCode | 章節正文完成 |
| review | done | Hermes | QA 報告通過 |
| build | done | Pi / Antigravity | PDF 產出 |
| release | pending | Antigravity | manifest + zip |

## 觀察重點

- `ready_stages([], stages)` 只會回傳 `spec`。
- 完成 `build` 後才會出現 `release`。
- `quality_gate()` 不應在 review 或 build 失敗時通過。

## 延伸練習

1. 為 Stage 增加 `owner` 欄位。
2. 加入 `package` 階段，放在 build 與 release 中間。
3. 將 pipeline 狀態輸出成 Markdown 表格。
