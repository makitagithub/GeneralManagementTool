import asyncio
import websockets
import json

# 接続中のクライアントを管理するためのセット
CONNECTED_CLIENTS = set()

async def notify_clients(message):
    """接続中の全クライアントにメッセージを送信します。"""
    # 接続が切れたクライアントは除外する
    if CONNECTED_CLIENTS:
        await asyncio.wait([client.send(message) for client in CONNECTED_CLIENTS])

async def register(websocket):
    """クライアントが接続したときに実行されます。"""
    CONNECTED_CLIENTS.add(websocket)
    try:
        # クライアントが切断するまで待機
        await websocket.wait_closed()
    finally:
        # クライアントが切断したらリストから削除
        CONNECTED_CLIENTS.remove(websocket)

async def server_main():
    """WebSocketサーバーを起動します。"""
    async with websockets.serve(register, "localhost", 8765):
        print("WebSocketサーバーを起動しました。ポート8765で待機中...")
        
        # 通知を送るためのシミュレーションループ
        count = 0
        while True:
            # 5秒ごとに通知を送信
            await asyncio.sleep(5)
            count += 1
            notification_message = {
                "type": "notification",
                "title": "新しい通知",
                "body": f"これはサーバーからのテスト通知です。（通知番号：{count}）"
            }
            print(f"クライアントに通知を送信: {notification_message['body']}")
            await notify_clients(json.dumps(notification_message))

if __name__ == "__main__":
    asyncio.run(server_main())