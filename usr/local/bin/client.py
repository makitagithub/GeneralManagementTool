import requests
import json

def check_for_updates_once():
    """一度だけアップデートを確認し、JSON形式の通知メッセージを読み込む"""
    update_server_url = "http://203.0.113.5/update"
    notification_url = "http://203.0.113.5/update/notification.json"

    try:
        # アップデート情報を確認
        response = requests.get(update_server_url, timeout=5)
        response.raise_for_status()
        update_data = response.json()

        # 通知メッセージをJSON形式で取得
        notification_response = requests.get(notification_url, timeout=5)
        notification_response.raise_for_status()
        notification_data = notification_response.json()
        
        # 通知メッセージから必要な情報を抽出
        notification_title = notification_data.get("title", "")
        notification_message = notification_data.get("message", "通知メッセージはありません。")

        if update_data.get("has_update"):
            version = update_data.get("version")
            download_url = update_data.get("download_url")
            
            # 通知メッセージとアップデート情報を組み合わせる
            message = f"[{notification_title}]\n{notification_message}\n\n新しいバージョンが見つかりました: {version}\nダウンロード: {download_url}"
            return {"status": "found", "message": message}
        else:
            message = f"[{notification_title}]\n{notification_message}\n\n新しいアップデートはありません。"
            return {"status": "not_found", "message": message}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"アップデートサーバーへの接続に失敗しました: {e}"}
    except json.JSONDecodeError:
        return {"status": "error", "message": "アップデート情報または通知の解析に失敗しました。サーバーの応答が不正です。"}

if __name__ == "__main__":
    # このスクリプトを単独で実行した場合のテスト
    result = check_for_updates_once()
    print(json.dumps(result, ensure_ascii=False, indent=2))