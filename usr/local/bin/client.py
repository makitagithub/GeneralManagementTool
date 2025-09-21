import requests
import json
import subprocess
import os
import resource_monitor
import command_log
import endpoint_log
import network_status
import setting
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

# アプリケーションのバージョン情報
# このバージョン番号は、.debパッケージのcontrolファイルと一致させる必要があります
APPLICATION_VERSION = "1.0.0"

# --- アップデート機能の追加 ---

def get_application_version():
    """現在のアプリケーションのバージョンを取得する"""
    return APPLICATION_VERSION

def check_for_updates_once():
    """通知を確認し、アップデート情報を読み込む"""
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

    if notification_data.get("has_update"):
        version = notification_data.get("version")
        download_url = notification_data.get("download_url")
        message = f"[{notification_title}]\n{notification_message}\n\n新しいバージョンが見つかりました: {version}\nダウンロード: {download_url}"
        
        # 現在のバージョンと比較
        if version > get_application_version():
            return {"status": "found", "message": message, "download_url": download_url}
        else:
            return {"status": "not_found", "message": "新しいアップデートはありません。"}
    else:
        message = f"[{notification_title}]\n{notification_message}\n\n新しいアップデートはありません。"
        return {"status": "not_found", "message": message, "download_url": None}


def update_application_auto(download_url):
    """アプリケーションを自動でアップデートする"""
    if not download_url:
        return {"status": "error", "message": "ダウンロードURLが指定されていません。"}
    
    try:
        # ダウンロード
        messagebox.showinfo("アップデート", "アップデートファイルをダウンロード中...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        deb_filename = os.path.basename(download_url)
        temp_file_path = f"/tmp/{deb_filename}"

        with open(temp_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # インストールコマンドを実行 (管理者権限が必要)
        messagebox.showinfo("アップデート", "アップデートをインストール中...パスワードが求められます。")
        install_command = ["sudo", "dpkg", "-i", temp_file_path]
        subprocess.run(install_command, check=True)

        messagebox.showinfo("アップデート完了", "アプリケーションは最新版にアップデートされました。再起動してください。")
        return {"status": "success", "message": "アップデートが完了しました。"}

    except requests.exceptions.RequestException as e:
        messagebox.showerror("エラー", f"ダウンロードに失敗しました: {e}")
        return {"status": "error", "message": f"ダウンロードに失敗しました: {e}"}
    except subprocess.CalledProcessError as e:
        messagebox.showerror("エラー", f"インストールの実行に失敗しました: {e}")
        return {"status": "error", "message": f"インストールの実行に失敗しました: {e}"}

# --- GUIの修正 ---

ICON_PATH = "/usr/share/icons/hicolor/scalable/apps/icon_picture.png"

def notify_update():
    """ベルマークボタンを押したときにアップデートを確認し、通知を表示する"""
    result = check_for_updates_once()
    status = result.get("status")
    message = result.get("message")
    download_url = result.get("download_url")
    
    if status == "found":
        response = messagebox.askyesno("アップデート通知", f"{message}\n\n今すぐアップデートしますか？")
        if response:
            update_application_auto(download_url)
    elif status == "not_found":
        messagebox.showinfo("アップデート通知", message)
    elif status == "error":
        messagebox.showerror("エラー", message)

def create_gui():
    root = tk.Tk(className="GeneralManagementTool")
    root.title("General Management Tool")
    root.geometry("1600x900")
    
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