# 第 3 章 Pi 微修代理

本範例示範 Pi 的微修哲學：只在修改目標唯一時才套用 patch，避免模糊替換與大範圍重寫。

## 學習目標

- 理解 exact text replacement 的安全價值。
- 學會拒絕 0 次或多次匹配的修改。
- 觀察標點正規化如何用小函式穩定處理。

## 主要檔案

- `micro_patch.py`：`replace_once`、PatchResult 與標點正規化。
- `test_baseline.py`：驗證唯一替換、拒絕模糊替換與標點轉換。

## 執行測試

```bash
PYTHONPATH=. python3 -m pytest -v
```

## 互動觀察

```python
from micro_patch import replace_once

content = "Agent 修改檔案。Agent 也可能覆蓋別人。"
result = replace_once(content, "Agent", "Pi")
print(result.changed)      # False
print(result.occurrences)  # 2
```

這個範例故意讓 `Agent` 出現兩次，因此修改會被拒絕。

## 觀察重點

- `replace_once` 不是為了方便替換，而是為了避免不確定修改。
- `PatchResult.occurrences` 可讓上層代理判斷失敗原因。
- 小型、可測試的修補比全檔重寫更適合多 Agent 協作。

## 延伸練習

1. 增加 preview 模式，只顯示將修改的內容。
2. 實作 `replace_many_exact`，要求所有目標都唯一。
3. 實作術語正規化，把「多代理」統一為「多 Agent」。
