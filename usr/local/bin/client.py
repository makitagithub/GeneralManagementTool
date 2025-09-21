import requests
import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import resource_monitor
import command_log
import endpoint_log
import network_status
import setting

# アプリケーションのバージョン情報
APPLICATION_VERSION = "1.0.0"

def get_application_version():
    """現在のアプリケーションのバージョンを取得する"""
    return APPLICATION_VERSION

def get_notification_message():
    """通知メッセージを読み込む"""
    # notification.jsonを直接指定
    notification_url = "http://10.0.2.15/update/notification.json"

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

ICON_PATH = "/usr/share/icons/hicolor/scalable/apps/icon_picture.png"

def notify_update():
    """ベルマークボタンを押したときに通知を表示する"""
    result = get_notification_message()
    status = result.get("status")
    message = result.get("message")
    
    if status == "success":
        messagebox.showinfo("お知らせ", message)
    elif status == "error":
        messagebox.showerror("エラー", message)

def create_gui():
    root = tk.Tk(className="GeneralManagementTool")
    root.title("General Management Tool")
    root.geometry("1600x900")
    
    # アイコンパスが存在する場合のみ設定
    if Path(ICON_PATH).exists():
        root.iconphoto(True, tk.PhotoImage(file=ICON_PATH))

    header_frame = tk.Frame(root, height=50)
    header_frame.pack(fill="x", side="top")

    bell_icon = tk.Button(header_frame, text="🔔", command=notify_update, bd=0, font=("Arial", 16))
    bell_icon.pack(side="right", padx=20, pady=5)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    resource_tab = resource_monitor.create_frame(notebook)
    network_status_tab = network_status.create_frame(notebook)
    endpoint_tab = endpoint_log.create_frame(notebook)
    log_tab = command_log.create_frame(notebook)
    settings_tab = setting.create_frame(notebook)

    notebook.add(resource_tab, text="🏠 resource monitor")
    notebook.add(network_status_tab, text="🌐 network status")
    notebook.add(endpoint_tab, text="🖧 endpoint management")
    notebook.add(log_tab, text="👨‍💼 log management")
    notebook.add(settings_tab, text="⚙️ settings")

    root.mainloop()

if __name__ == "__main__":
    create_gui()