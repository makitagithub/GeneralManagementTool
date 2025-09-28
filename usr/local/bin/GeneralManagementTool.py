#!/usr/bin/env python3

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import resource_monitor 
import command_log
import endpoint_log
import network_status
import setting
# clientモジュールからget_notification_messageのみをインポート
from client import get_notification_message

ICON_PATH = "/usr/share/icons/hicolor/scalable/apps/icon_picture.png"

# ==========================================================
# 🔔 状態管理変数をモジュールレベルで定義 (create_gui内で初期化する)
# ==========================================================
# tk.BooleanVarとtk.StringVarはtk.Tk()初期化後に作成する必要があるため、Noneで初期化
notification_available = None 
bell_text = None
bell_icon_ref = None # ボタンの色変更のために、ボタン自身をグローバル参照する必要がある

def notify_update():
    """ベルマークボタンを押したときに通知を表示し、状態をリセットする"""
    # グローバル変数を使用するため宣言
    global notification_available
    global bell_text
    global bell_icon_ref
    
    # 1. 通知メッセージの取得
    result = get_notification_message()
    
    status = result.get("status")
    message = result.get("message")
    
    # 2. 通知の表示
    if status == "success":
        messagebox.showinfo("お知らせ", message)
    elif status == "error":
        messagebox.showerror("エラー", message)

    # 3. 通知を確認したので、状態をリセット
    if notification_available is not None:
        notification_available.set(False) 
    
    # 4. ボタンのテキストと色を「通知なし」に戻す
    if bell_text is not None:
        bell_text.set("🔔")
    if bell_icon_ref is not None:
        bell_icon_ref.config(fg="black") # 色を黒に戻す


def create_gui():
    root = tk.Tk(className="GeneralManagementTool")
    root.title("General Management Tool")
    root.geometry("1600x900")
    
    if Path(ICON_PATH).exists():
        root.iconphoto(True, tk.PhotoImage(file=ICON_PATH))

    header_frame = tk.Frame(root, height=50)
    header_frame.pack(fill="x", side="top")

    # ==========================================================
    # 🔔 状態変数の初期化とボタンの設定
    # ==========================================================
    global notification_available
    global bell_text
    global bell_icon_ref # 🔔ボタンの参照を保持
    
    # 1. 状態管理変数の初期化
    notification_available = tk.BooleanVar(value=True) # 初期状態: 通知あり
    initial_text = "重要なお知らせが来ています🔔" if notification_available.get() else "🔔"
    bell_text = tk.StringVar(value=initial_text) 
    
    # 2. 🔔アイコンボタンの作成
    bell_icon = tk.Button(
        header_frame, 
        textvariable=bell_text, # 👈 text ではなく textvariable を使用
        command=notify_update,  # グローバル変数を使うため引数なし
        bd=0, 
        font=("Arial", 16),
        fg="red" if notification_available.get() else "black" # 初期色を設定
    )
    bell_icon_ref = bell_icon # ボタンの参照をグローバル変数に保存
    # ==========================================================

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