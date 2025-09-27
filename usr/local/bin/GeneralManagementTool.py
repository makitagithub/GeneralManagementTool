#!/usr/bin/env python3

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import resource_monitor 
import command_log
import endpoint_log
import network_status
import setting
# import client as update_client # client.pyをインポート

# clientモジュールから直接必要な関数をインポート
from client import get_notification_message

ICON_PATH = "/usr/share/icons/hicolor/scalable/apps/icon_picture.png"

def notify_update():
    """ベルマークボタンを押したときに通知を表示する"""
    # client.pyからget_notification_message関数を呼び出す
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
    
    if Path(ICON_PATH).exists():
        root.iconphoto(True, tk.PhotoImage(file=ICON_PATH))

    header_frame = tk.Frame(root, height=50)
    header_frame.pack(fill="x", side="top")

    # 1. 通知状態変数 (BooleanVar) の定義（初期状態: True、通知あり）
    notification_available = tk.BooleanVar(value=True) 

    # 2. 🔔アイコンボタンの作成
    # command に引数を渡すため lambda 式を使用
    bell_icon = tk.Button(
        header_frame, 
        text="🔔", 
        command=lambda: notify_update(notification_available, notification_label), 
        bd=0, 
        font=("Arial", 16),
        fg="red" # 通知があることを示すために赤くする
    )
    bell_icon.pack(side="right", padx=5, pady=5) # 🔔アイコンを右端に配置

    # 3. 通知メッセージ Label の作成
    notification_label = tk.Label(
        header_frame, 
        text="一件の通知があります", 
        fg="red", # メッセージも赤くして目立たせる
        font=("Arial", 12, "bold")
    )
    
    # 4. 初期状態で通知がある場合のみメッセージを表示
    # 🔔アイコンの左隣に配置するため、🔔よりも先に pack する必要がある
    if notification_available.get():
        notification_label.pack(side="right", padx=5, pady=5)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # resource_monitor, network_status などがないため仮のフレームで代替
    resource_tab = tk.Frame(notebook); network_status_tab = tk.Frame(notebook)
    endpoint_tab = tk.Frame(notebook); log_tab = tk.Frame(notebook)
    settings_tab = tk.Frame(notebook)

    notebook.add(resource_tab, text="🏠 resource monitor")
    notebook.add(network_status_tab, text="🌐 network status")
    notebook.add(endpoint_tab, text="🖧 endpoint management")
    notebook.add(log_tab, text="👨‍💼 log management")
    notebook.add(settings_tab, text="⚙️ settings")

    root.mainloop()

if __name__ == "__main__":
    create_gui()