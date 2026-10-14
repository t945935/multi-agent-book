#!/usr/bin/env bash
set -e

echo "=================================================="
echo "🧪 執行全書所有章節程式碼範例自動化驗證"
echo "=================================================="

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for chapter_dir in "$BASE_DIR"/examples/*; do
  if [ -d "$chapter_dir" ]; then
    ch_name=$(basename "$chapter_dir")
    echo ""
    echo "▶ 正在檢驗章節: $ch_name ..."
    if [ -f "$chapter_dir/test_baseline.py" ] || [ -d "$chapter_dir/tests" ]; then
      (
        cd "$chapter_dir"
        PYTHONPATH=. python3 -m pytest -v
      )
      echo "✅ $ch_name 測試全數通過！"
    else
      echo "ℹ️  $ch_name 尚無測試腳本，略過。"
    fi
  fi
done

echo ""
echo "=================================================="
echo "🎉 全書所有範例測試完成，品質檢驗無誤！"
echo "=================================================="
