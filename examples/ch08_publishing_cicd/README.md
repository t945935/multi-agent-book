# 第 8 章 發行 CI/CD

本範例示範 release manifest 與 checksum 的最小模型。實際專案中的完整打包流程位於 `scripts/package_release.py`。

## 學習目標

- 理解 artifacts 為什麼需要 checksum。
- 學會建立包含版本、檔案雜湊與檢查項目的 ReleaseManifest。
- 理解 publishable 不等於已公開上架，公開上架仍需人工核准。

## 主要檔案

- `release.py`：ReleaseManifest、checksum、create_manifest、is_publishable。
- `test_baseline.py`：驗證 checksum 穩定性與 manifest 可發布條件。

## 執行測試

```bash
PYTHONPATH=. python3 -m pytest -v
```

## 執行全書打包

回到專案根目錄後執行：

```bash
PATH="$PWD/bin:$PATH" python3 scripts/build.py
python3 scripts/package_release.py --version 1.0.0
```

會產出：

- `dist/release_manifest.json`
- `dist/multi-agent-book-v1.0.0.zip`

## 觀察重點

- 同一份內容應產生相同 checksum。
- manifest 至少需要 version、artifacts 與 checks。
- release package 可以自動產生，但公開上架仍需人工確認。

## 延伸練習

1. 將範例 checksum 改為完整 SHA-256。
2. 為 ReleaseManifest 增加 `created_at`。
3. 檢查 `dist/release_manifest.json` 是否包含 PDF 與 QA 報告。
