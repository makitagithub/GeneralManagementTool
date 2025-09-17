#!/usr/bin/env python3

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import resource_monitor 
import command_log
import endpoint_log
import network_status
import setting

ICON_PATH = "/usr/share/icons/hicolor/scalable/apps/icon_picture.png"

def notify_update():
    """ベルマークボタンを押したときにclient.pyを起動する"""
    try:
        # client.pyのパスを指定（このスクリプトと同じディレクトリにあると仮定）
        client_script_path = os.path.join(os.path.dirname(__file__), "client.py")
        
        # subprocess.Popenを使ってclient.pyを新しいプロセスとして起動
        # これによりGUIがフリーズせずに済む
        subprocess.Popen(["python3", client_script_path])
        
        # ユーザーに通知
        messagebox.showinfo("通知", "アップデート確認ツールを起動しました。")
    except FileNotFoundError:
        messagebox.showerror("エラー", "client.pyが見つかりません。パスを確認してください。")
    except Exception as e:
        messagebox.showerror("エラー", f"ツールの起動中にエラーが発生しました: {e}")

def create_gui():
    root = tk.Tk(className="GeneralManagementTool")
    root.wm_class("generalmanagementtool","GeneralManagementTool")
    root.title("General Management Tool")
    root.geometry("1600x900")
    
    # Path.extists()は誤りなので修正
    if Path(ICON_PATH).exists():
        # PhotoTmage()は誤りなので修正
        root.iconphoto(True, tk.PhotoImage(file=ICON_PATH))

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