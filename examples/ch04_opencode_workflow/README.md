# 第 4 章 OpenCode Plan / Build 工作流

本範例示範先規劃、再建置的雙模式工作流。未核准的 Plan 不能進入 Build，避免代理在目標與範圍不清楚時直接改檔案。

## 學習目標

- 理解 Plan 與 Build 為什麼要分離。
- 學會用 approval gate 控制大型修改。
- 理解 BuildArtifact 應回報修改檔案與摘要。

## 主要檔案

- `workflow.py`：Plan、approve、build 與 BuildArtifact。
- `test_baseline.py`：驗證未核准不得 build，以及核准後可產生 artifact。

## 執行測試

```bash
PYTHONPATH=. python3 -m pytest -v
```

## Plan 範例

```text
目標：擴充第 5 章 Hermes 記憶章節
修改範圍：只修改 src/ch05.md
步驟：
1. 讀取現有章節
2. 對照 examples/ch05_hermes_self_learning/
3. 補充記憶污染與審稿報告格式
4. 執行測試與 build
驗證：
- bash scripts/test_all.sh
- PATH="$PWD/bin:$PATH" python3 scripts/build.py
```

## 觀察重點

- `build()` 會拒絕 `approved=False` 的 Plan。
- approval gate 是工作流中的硬性條件，不只是文字建議。
- Build 完成後應留下可交接摘要。

## 延伸練習

1. 為 Plan 增加 `risks` 與 `verification` 欄位。
2. 要求缺少驗證命令的 Plan 不可 approve。
3. 讓 BuildArtifact 記錄測試結果。
