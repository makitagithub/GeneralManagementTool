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

    # --- 🔔アイコンと通知メッセージの変更点 ---
    
    # 1. 通知状態を管理する変数（初期値: True = 通知あり）
    notification_available = tk.BooleanVar(value=True) 

    # 2. 通知メッセージ Label の作成
    notification_label = tk.Label(
        header_frame, 
        text="一件の通知があります", 
        fg="red", # 目立たせる
        font=("Arial", 12, "bold")
    )

    # 3. 🔔アイコンボタンの作成
    # textをシンプルにし、通知ありを示す色を設定
    bell_icon = tk.Button(
        header_frame, 
        text="🚨🔔", # 通知ありを示すアイコンに変更 (例: 🚨🔔)
        # lambdaを使ってnotify_updateに関数とラベルとボタン自身を渡す
        command=lambda: notify_update(notification_available, notification_label, bell_icon), 
        bd=0, 
        font=("Arial", 16),
        fg="red" # 通知があることを示すために赤くする
    )
    
    # 4. ラベルとボタンを配置 (packの順序が重要: ラベル → ボタンで左から右に並ぶ)
    # 初期状態で通知がある場合のみメッセージを表示
    if notification_available.get():
        # bell_iconよりも先にpackすることで、左隣に配置される
        notification_label.pack(side="right", padx=5, pady=5) 
        
    bell_icon.pack(side="right", padx=15, pady=5) # 🔔アイコンを右端に配置

    # ----------------------------------------
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # ... (タブの作成と追加は変更なし) ...
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