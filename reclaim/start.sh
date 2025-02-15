#!/bin/bash

# プロセスIDを格納する配列
pids=()

# 終了時の処理
cleanup() {
    echo "全てのプロセスを終了します..."
    for pid in "${pids[@]}"; do
        kill $pid 2>/dev/null
    done
    exit 0
}

# SIGINTとSIGTERMのトラップを設定
trap cleanup SIGINT SIGTERM

conda activate reclaim

# cloudflaredをバックグラウンドで実行
cloudflared tunnel run reclaim &
pids+=($!)

# Django開発サーバーをバックグラウンドで実行
python manage.py runserver &
pids+=($!)

# Django background tasksをバックグラウンドで実行
python manage.py process_tasks &
pids+=($!)

echo "全てのサービスを開始しました"
echo "終了するにはCtrl+Cを押してください"
echo "終了するには’kill $$’を実行してください"

# メインプロセスを維持
wait