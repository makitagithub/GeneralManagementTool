import tkinter as tk
from tkinter import ttk
import psutil

def format_bytes(size):
    # 単位付きで人間が読みやすい形式に変換
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def create_frame(parent):
    frame = ttk.Frame(parent)

    title = tk.Label(frame, text="Network Status", font=("Arial", 18, "bold"))
    title.pack(pady=10)

    tree = ttk.Treeview(frame, columns=("iface", "sent", "recv"), show="headings", height=15)
    tree.heading("iface", text="Interface Name")
    tree.heading("sent", text="Sent")
    tree.heading("recv", text="Received")
    tree.column("iface", width=250, anchor="center")
    tree.column("sent", width=200, anchor="center")
    tree.column("recv", width=200, anchor="center")
    tree.pack(padx=40, pady=10, fill="both", expand=True)

    net_io = psutil.net_io_counters(pernic=True)
    for iface, counters in net_io.items():
        if counters.bytes_sent == 0 and counters.bytes_recv == 0:
            continue  # 送受信がゼロならスキップ（リアリティのため）
        tree.insert("", "end", values=(
            iface,
            format_bytes(counters.bytes_sent),
            format_bytes(counters.bytes_recv)
        ))

    return frame

