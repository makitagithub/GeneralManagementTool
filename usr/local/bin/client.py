import requests
import json
# 以下のGUI関連のimportは不要
# import tkinter as tk
# from tkinter import ttk, messagebox
# from pathlib import Path
# import resource_monitor
# import command_log
# import endpoint_log
# import network_status
# import setting

# アプリケーションのバージョン情報
APPLICATION_VERSION = "1.6.0"

def get_application_version():
    """現在のアプリケーションのバージョンを取得する"""
    return APPLICATION_VERSION

def get_notification_message():
    """通知メッセージを読み込む"""
    # notification.jsonを直接指定
    notification_url = "http://10.10.5.2/update/notification.json"

    try:
        response = requests.get(notification_url, timeout=5)
        response.raise_for_status()
        notification_data = response.json()
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"サーバーへの接続に失敗しました: {e}"}
    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"通知情報の解析に失敗しました。サーバーの応答が不正です: {e}"}

    notification_title = notification_data.get("title", "")
    notification_message = notification_data.get("message", "通知メッセージはありません。")
    
    # シンプルにタイトルとメッセージを結合して返す
    message = f"[{notification_title}]\n{notification_message}"
    return {"status": "success", "message": message}

# client.pyの残りのGUI関連関数やmainブロックはすべて削除します。
# GeneralManagementTool.py が get_notification_message のみを使用します。