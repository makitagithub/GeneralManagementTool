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

notification_available = None 

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

    global notification_available
    notification_available = tk.BooleanVar(value=True)
    initial_text = "重要なお知らせが来ています🔔" if notification_available.get() else "🔔"
    bell_text = tk.StringVar(value=initial_text) 

    bell_icon = tk.Button(header_frame, text=bell_text, command=notify_update, bd=0, font=("Arial", 16), fg="red" if notification_available.get() else "black")
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