import requests
import json

def check_for_updates_once():
    """一度だけアップデートを確認し、JSON形式の通知メッセージを読み込む"""
    # update_server_url = "http://203.0.113.5/update"
    # notification_url = "http://203.0.113.5/update/notification.json"
    update_server_url = "http://10.0.2.15/update"
    notification_url = "http://10.0.2.15/update/notification.json"

    try:
        # 1. アップデート情報を取得
        update_response = requests.get(update_server_url, timeout=5)
        update_response.raise_for_status()  # 4xx/5xxエラーをキャッチ
        
        # 応答内容をデバッグ用に表示
        print(f"Update server response: {update_response.text}")

        update_data = update_response.json()
    except requests.exceptions.RequestException as e:
        # アップデートサーバーへの接続・通信エラー
        return {"status": "error", "message": f"アップデートサーバーへの接続に失敗しました: {e}"}
    except json.JSONDecodeError as e:
        # アップデート情報のJSON解析エラー
        return {"status": "error", "message": f"アップデート情報の解析に失敗しました。サーバーの応答が不正です: {e}"}

    try:
        # 2. 通知メッセージを取得
        notification_response = requests.get(notification_url, timeout=5)
        notification_response.raise_for_status() # 4xx/5xxエラーをキャッチ
        
        # 応答内容をデバッグ用に表示
        print(f"Notification server response: {notification_response.text}")
        
        notification_data = notification_response.json()
    except requests.exceptions.RequestException as e:
        # 通知サーバーへの接続・通信エラー
        return {"status": "error", "message": f"通知サーバーへの接続に失敗しました: {e}"}
    except json.JSONDecodeError as e:
        # 通知メッセージのJSON解析エラー
        return {"status": "error", "message": f"通知メッセージの解析に失敗しました。サーバーの応答が不正です: {e}"}

    # 正常な処理（ここから以下は前回と同じです）
    notification_title = notification_data.get("title", "")
    notification_message = notification_data.get("message", "通知メッセージはありません。")

    if update_data.get("has_update"):
        version = update_data.get("version")
        download_url = update_data.get("download_url")
        message = f"[{notification_title}]\n{notification_message}\n\n新しいバージョンが見つかりました: {version}\nダウンロード: {download_url}"
        return {"status": "found", "message": message}
    else:
        message = f"[{notification_title}]\n{notification_message}\n\n新しいアップデートはありません。"
        return {"status": "not_found", "message": message}

if __name__ == "__main__":
    result = check_for_updates_once()
    print(json.dumps(result, ensure_ascii=False, indent=2))