import asyncio
import websockets
import json
import PySimpleGUI as sg
import threading

# GUIのイベントキューにメッセージを送信するためのキー
MESSAGE_KEY = '-MESSAGE-'

def run_websocket_client(window):
    """GUIの別スレッドでWebSocketクライアントを実行します。"""
    async def connect():
        uri = "ws://localhost:8765"
        try:
            # WebSocketサーバーに接続
            async with websockets.connect(uri) as websocket:
                print("サーバーに接続しました。通知を待機中...")
                window.write_event_value(MESSAGE_KEY, "サーバーに接続しました。通知を待機中...")
                
                # サーバーからのメッセージを待機
                async for message_str in websocket:
                    message_data = json.loads(message_str)
                    print(f"サーバーからメッセージを受信: {message_data}")
                    window.write_event_value(MESSAGE_KEY, message_data)

        except ConnectionRefusedError:
            error_msg = "サーバーへの接続に失敗しました。サーバーが起動しているか確認してください。"
            print(error_msg)
            window.write_event_value(MESSAGE_KEY, {"type": "error", "body": error_msg})
        except Exception as e:
            error_msg = f"接続中にエラーが発生しました: {e}"
            print(error_msg)
            window.write_event_value(MESSAGE_KEY, {"type": "error", "body": error_msg})

    # asyncioのイベントループをスレッド内で実行
    asyncio.run(connect())

# GUIのレイアウト
layout = [
    [sg.Text("GeneralManagementTool", font=("Helvetica", 20))],
    [sg.Text("サーバーからの通知を待機中...", key='-STATUS-')],
    [sg.HorizontalSeparator()],
    [sg.Output(size=(60, 10), key='-OUTPUT-')],
    [sg.Button("終了")]
]

# ウィンドウの作成
window = sg.Window("GeneralManagementTool", layout, finalize=True)

# WebSocketクライアントを別スレッドで起動
thread = threading.Thread(target=run_websocket_client, args=(window,), daemon=True)
thread.start()

# GUIのイベントループ
while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED or event == "終了":
        break
    
    # WebSocketスレッドからのメッセージを受信
    if event == MESSAGE_KEY:
        message = values[MESSAGE_KEY]
        if isinstance(message, str):
            window['-STATUS-'].update(message)
            window['-OUTPUT-'].print(message)
        elif isinstance(message, dict) and message.get("type") == "notification":
            title = message.get("title", "通知")
            body = message.get("body", "")
            sg.popup_ok(body, title=title)
            window['-OUTPUT-'].print(f"ポップアップ通知: {body}")
        elif isinstance(message, dict) and message.get("type") == "error":
            error_body = message.get("body", "不明なエラー")
            sg.popup_error(error_body, title="エラー")
            window['-OUTPUT-'].print(f"エラー: {error_body}")
            window['-STATUS-'].update("接続エラーが発生しました。")
            break

window.close()