import tkinter as tk
from tkinter import ttk
import os

LOG_DIR = "/usr/local/share/general-logs"

def create_frame(parent):
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True)

    # タイトル（画面中央）
    title = tk.Label(frame, text="Log Management", font=("Arial", 18, "bold"))
    title.pack(pady=10)
    

    # 中身を中央に配置するための内側フレーム
    inner_frame = ttk.Frame(frame)
    inner_frame.pack(anchor="center")

    # Employee List Label
    name_label = tk.Label(inner_frame, text="Employee List")
    name_label.grid(row=0, column=0, sticky="w")

    # Employee Listbox
    employee_listbox = tk.Listbox(inner_frame, height=25, width=25)
    employee_listbox.grid(row=1, column=0, padx=20, pady=10)

    # Log Display Area
    log_display = tk.Text(inner_frame, width=80, height=25)
    log_display.grid(row=1, column=1, padx=20, pady=10)



    def update_employee_list():
        employee_listbox.delete(0, tk.END)
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        for filename in os.listdir(LOG_DIR):
            if filename.endswith(".log"):
                name = filename.replace(".log", "")
                employee_listbox.insert(tk.END, name)

    def show_selected_log(event):
        selection = employee_listbox.curselection()
        if selection:
            index = selection[0]
            name = employee_listbox.get(index)
            file_path = os.path.join(LOG_DIR, f"{name}.log")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    log_display.delete("1.0", tk.END)
                    log_display.insert(tk.END, f.read())
            except Exception as e:
                log_display.delete("1.0", tk.END)
                log_display.insert(tk.END, f"読み込みエラー: {e}")

    employee_listbox.bind("<<ListboxSelect>>", show_selected_log)

    update_employee_list()

    return frame

