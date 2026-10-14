# 第 5 章 Hermes 反思記憶

本範例示範 Hermes 如何從審稿觀察中萃取規則，並在後續任務中用記憶評估風險。

## 學習目標

- 理解 observation 到 rule 的轉換。
- 學會用 `prompt_hints()` 取得可重用規則。
- 理解過去失敗如何影響新任務風險評估。

## 主要檔案

- `memory.py`：ReflectionMemory 與 `review_risk`。
- `test_baseline.py`：驗證 timeout / overwrite 規則與 network 任務風險。

## 執行測試

```bash
PYTHONPATH=. python3 -m pytest -v
```

## 觀察範例

```text
觀察：第 8 章 build 失敗，原因是 Typst 字型不存在。
萃取規則：新增或修改 Typst 字型時，必須先檢查系統可用字型。
```

真實系統可分三層記憶：

1. 關鍵字規則。
2. 結構化審稿報告。
3. 向量資料庫或長程記憶服務。

## 觀察重點

- `observe()` 保存原始觀察，也萃取簡化規則。
- `prompt_hints()` 會去重並排序規則。
- `review_risk()` 展示記憶如何影響新任務判斷。

## 延伸練習

1. 增加 `severity`，區分 warning 與 blocker。
2. 新增 `check_available_fonts` 規則。
3. 將 QA 報告轉成記憶規則清單。
