import os
import signal
import subprocess
import sys
import time


def run_command(command):
    try:
        ret = subprocess.run(command, shell=True, capture_output=True, text=True)
        if ret.returncode == 0:
            return ret
        return None
    except Exception as e:
        print(f"コマンド実行エラー: {e}")
        return None


def start_process(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE, encoding='utf-8',
                          preexec_fn=os.setsid)  # プロセスグループを作成


def signal_handler(signum, frame):
    print("\n終了します...")
    sys.exit(0)


def start():
    manage_py = find_manage_py()
    if not manage_py:
        print("manage.pyが見つかりませんでした")
        return
    
    print(f"Found manage.py at: {manage_py}")
    
    # シグナルハンドラを設定
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 開発サーバーを起動
    server_command = f"python3 {manage_py} runserver"
    print("開発サーバーを起動します...")
    server_process = start_process(server_command)
    
    # タスク処理を起動
    task_command = f"python3 {manage_py} process_tasks"
    print("タスクを起動します...")
    task_process = start_process(task_command)
    
    try:
        while True:
            # 各プロセスの出力を表示
            server_output = server_process.stdout.readline()
            if server_output:
                print("Server:", server_output.strip())
            
            task_output = task_process.stdout.readline()
            if task_output:
                print("Task:", task_output.strip())
            
            # プロセスが終了していないか確認
            if server_process.poll() is not None or task_process.poll() is not None:
                print("プロセスが予期せず終了しました")
                break
                
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n終了します...")
    finally:
        # プロセスグループごと終了
        try:
            os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
            os.killpg(os.getpgid(task_process.pid), signal.SIGTERM)
        except:
            pass


def find_manage_py():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # カレントディレクトリとその配下からmanage.pyを探す
    for root, dirs, files in os.walk(current_dir):
        if 'manage.py' in files:
            return os.path.join(root, 'manage.py')
    
    return None


if __name__ == '__main__':
    start()
