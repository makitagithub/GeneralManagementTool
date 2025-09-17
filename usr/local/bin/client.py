import requests
import json

def check_for_updates_once():
    """一度だけアップデートを確認する"""
    update_server_url = "http://localhost:5000/check_for_updates"

    try:
        response = requests.get(update_server_url)
        update_data = response.json()
        
        if update_data.get("has_update"):
            version = update_data.get("version")
            download_url = update_data.get("download_url")
            
            message = f"新しいバージョンが見つかりました: {version}\nダウンロード: {download_url}"
            return {"status": "found", "message": message}
        else:
            return {"status": "not_found", "message": "新しいアップデートはありません。"}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"アップデートサーバーへの接続に失敗しました: {e}"}

if __name__ == "__main__":
    # このスクリプトを単独で実行した場合のテスト
    result = check_for_updates_once()
    print(json.dumps(result))