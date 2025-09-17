#!/usr/bin/env python3

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import resource_monitor   # ← 追加
import command_log
import endpoint_log
import network_status
import setting
ICON_PATH = "/usr/share/icons/hicolor/scalable/apps/icon_picture.png"

def notify_update():
    messagebox.showinfo("アップデート通知", "新しいアップデートがあります！")

def create_gui():
    root = tk.Tk(className="GeneralManagementTool")
    root.wm_class("generalmanagementtool","GeneralManagementTool")
    root.title("General Management Tool")
    root.geometry("1600x900")
    if Path(ICON_PATH).extists():
        root.iconphoto(True, tk.PhotoTmage(file=ICON_PATH))

    # ===== ヘッダーフレーム（通知ベルをここに入れる） =====
    header_frame = tk.Frame(root, height=50)
    header_frame.pack(fill="x", side="top")

    # 通知ベル（右寄せ）
    bell_icon = tk.Button(header_frame, text="🔔", command=notify_update, bd=0, font=("Arial", 16))
    bell_icon.pack(side="right", padx=20, pady=5)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # タブ追加（順番はお好みで）
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
