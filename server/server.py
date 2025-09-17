import asyncio
import websockets
import json
import time

# 接続中のクライアントを管理するためのセット
connected_clients = set()

async def notify_clients(message):
    """接続中の全クライアントにメッセージを送信します。"""
    if connected_clients:
        # 非同期で全てのクライアントにメッセージを送信
        await asyncio.wait([client.send(message) for client in connected_clients])

async def handler(websocket, path):
    """新しいクライアントが接続したときに実行されます。"""
    print(f"新しいクライアントが接続しました。Path: {path}")
    # 新しいクライアントをセットに追加
    connected_clients.add(websocket)
    try:
        # クライアントからのメッセージを処理（ここでは何もしない）
        await websocket.wait_closed()
    finally:
        # クライアントが切断したらセットから削除
        print("クライアントが切断しました。")
        connected_clients.remove(websocket)

async def main():
    """WebSocketサーバーを起動し、通知ループを開始します。"""
    # WebSocketサーバーをlocalhostの8765ポートで起動
    server = await websockets.serve(handler, "localhost", 8765)
    print("WebSocketサーバーを起動しました。ポート8765で待機中...")

    # 通知を送信するメインループ
    notification_count = 0
    while True:
        # 5秒ごとに通知を送信するシミュレーション
        await asyncio.sleep(5)
        notification_count += 1
        
        # JSON形式の通知メッセージを作成
        message = {
            "type": "notification",
            "title": "新しいタスク",
            "body": f"タスクAが割り当てられました。（通知番号：{notification_count}）"
        }
        
        # 接続中のクライアントにメッセージを送信
        await notify_clients(json.dumps(message))
        print(f"通知を送信しました: {message['body']}")

if __name__ == "__main__":
    asyncio.run(main())