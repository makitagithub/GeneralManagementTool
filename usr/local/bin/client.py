import requests
import json

def check_for_updates_once():
    """一度だけ通知を確認し、アップデート情報を読み込む"""
    notification_url = "http://10.0.2.15/update/notification.json"

    try:
        # 通知とアップデート情報を含むJSONを取得
        response = requests.get(notification_url, timeout=5)
        response.raise_for_status()
        
        # デバッグ用に出力
        print(f"Server response text: {response.text}")
        
        notification_data = response.json()
        
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"サーバーへの接続に失敗しました: {e}"}
    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"通知情報の解析に失敗しました。サーバーの応答が不正です: {e}"}

    # JSONデータから必要な情報を抽出
    notification_title = notification_data.get("title", "")
    notification_message = notification_data.get("message", "通知メッセージはありません。")

    if notification_data.get("has_update"):
        version = notification_data.get("version")
        download_url = notification_data.get("download_url")
        message = f"[{notification_title}]\n{notification_message}\n\n新しいバージョンが見つかりました: {version}\nダウンロード: {download_url}"
        return {"status": "found", "message": message}
    else:
        message = f"[{notification_title}]\n{notification_message}\n\n新しいアップデートはありません。"
        return {"status": "not_found", "message": message}

if __name__ == "__main__":
    result = check_for_updates_once()
    print(json.dumps(result, ensure_ascii=False, indent=2))