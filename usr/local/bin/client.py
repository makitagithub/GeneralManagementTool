import requests
import PySimpleGUI as sg
import threading
import time

def check_for_updates_polling(window):
    """アップデートを定期的に確認するポーリングスレッド"""
    update_check_interval = 30  # 確認間隔を30秒に設定
    update_server_url = "http://localhost:5000/check_for_updates"

    while True:
        try:
            response = requests.get(update_server_url)
            update_data = response.json()
            
            if update_data.get("has_update"):
                version = update_data.get("version")
                download_url = update_data.get("download_url")
                
                message = f"新しいバージョンが見つかりました: {version}\nダウンロード: {download_url}"
                window.write_event_value('-UPDATE_FOUND-', message)
                # アップデートが見つかったらポーリングを停止することもできます
                break 
            
            print("アップデートはありませんでした。")

        except requests.exceptions.RequestException as e:
            print(f"アップデートサーバーへの接続に失敗しました: {e}")
        
        # 次の確認まで待機
        time.sleep(update_check_interval)

# GUIのレイアウトとイベントループは、WebSocketの時とほぼ同じ
layout = [
    [sg.Text("GeneralManagementTool", font=("Helvetica", 20))],
    [sg.Output(size=(60, 10))],
    [sg.Button("終了")]
]

window = sg.Window("GeneralManagementTool", layout, finalize=True)

# アップデート確認スレッドを起動
update_thread = threading.Thread(target=check_for_updates_polling, args=(window,), daemon=True)
update_thread.start()

# GUIのイベントループ
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "終了":
        break
    
    # ポーリングスレッドからのアップデート通知を受信
    if event == '-UPDATE_FOUND-':
        sg.popup_ok(values['-UPDATE_FOUND-'], title="アップデート通知")

window.close()