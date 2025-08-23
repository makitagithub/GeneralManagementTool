import tkinter as tk
from tkinter import ttk

# ダミーデータ：開発部門の社員PC
employee_devices = [
    {"pc_name": "dev-pc001", "employee": "佐藤一郎", "ip": "192.168.10.21", "status": "Online"},
    {"pc_name": "dev-pc002", "employee": "鈴木花子", "ip": "192.168.10.22", "status": "Offline"},
    {"pc_name": "dev-pc003", "employee": "田中洋介", "ip": "192.168.10.23", "status": "Online"},
    {"pc_name": "dev-pc004", "employee": "山本美咲", "ip": "192.168.10.24", "status": "Online"},
]

def create_frame(parent):
    frame = ttk.Frame(parent)
    
    title = tk.Label(frame, text="Endpoint Management", font=("Arial", 18, "bold"))
    title.pack(pady=10)

    columns = ("pc_name", "employee", "ip", "status")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
    tree.pack(fill="both", padx=40, pady=10, expand=True)

    # ヘッダー
    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, anchor="center", width=150)

    # ステータスによる色分け（タグ定義）
    tree.tag_configure("online", background="#e0ffe0")   # 緑っぽい背景
    tree.tag_configure("offline", background="#ffe0e0")  # 赤っぽい背景

    # データ挿入
    for device in employee_devices:
        tag = "online" if device["status"] == "Online" else "offline"
        tree.insert("", "end", values=(device["pc_name"], device["employee"], device["ip"], device["status"]), tags=(tag,))

    return frame

