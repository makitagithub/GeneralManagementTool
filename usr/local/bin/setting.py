# usr/local/bin/setting.py
import tkinter as tk
from tkinter import ttk, messagebox

def create_frame(parent):
    frame = tk.Frame(parent, width=1600, height=900)
    frame.pack_propagate(False)

    # タイトル（画面中央）
    title = tk.Label(frame, text="Settings", font=("Arial", 18, "bold"))
    title.pack(pady=10)

    version_label = tk.Label(frame, text="Version: 1.0.0", font=("Arial", 16))
    version_label.pack(pady=30)
    
    # --- Update Check ---
    def check_update():
        update_label.config(text="No updates available")

    update_button = tk.Button(frame, text="Check for Updates", command=check_update)
    update_button.pack(pady=(30, 5))

    update_label = tk.Label(frame, text="", font=("Arial", 12))
    update_label.pack(pady=5)

    # --- Display Settings ---
    display_frame = tk.LabelFrame(frame, text="Display Settings", font=("Arial", 14, "bold"))
    display_frame.pack(padx=20, pady=10, fill="x")
    

    # テーマ選択
    tk.Label(display_frame, text="Theme:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    theme_var = tk.StringVar(value="Light")
    theme_menu = ttk.Combobox(display_frame, textvariable=theme_var, values=["Light", "Dark"], state="readonly")
    theme_menu.grid(row=0, column=1, padx=10, pady=5)

    # 言語選択
    tk.Label(display_frame, text="Display Language:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    language_var = tk.StringVar(value="日本語")
    language_menu = ttk.Combobox(display_frame, textvariable=language_var, values=["日本語", "English"], state="readonly")
    language_menu.grid(row=1, column=1, padx=10, pady=5)

    # 通知のオンオフ
    notify_var = tk.BooleanVar(value=True)
    notify_check = tk.Checkbutton(display_frame, text="Enable Notifications", variable=notify_var, font=("Arial", 12))
    notify_check.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)

    # --- Security Settings ---
    security_frame = tk.LabelFrame(frame, text="Security Settings", font=("Arial", 14, "bold"))
    security_frame.pack(padx=20, pady=10, fill="x")

    # パスワード変更
    tk.Label(security_frame, text="New Password:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    new_pw = tk.Entry(security_frame, show="*")
    new_pw.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(security_frame, text="Confirm Password:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    confirm_pw = tk.Entry(security_frame, show="*")
    confirm_pw.grid(row=1, column=1, padx=10, pady=5)

    def change_password():
        if new_pw.get() != confirm_pw.get():
            messagebox.showerror("Error", "Passwords do not match")
        else:
            messagebox.showinfo("Success", "Password has been updated (mock)")

    pw_button = tk.Button(security_frame, text="Change Password", command=change_password)
    pw_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Two-Factor Authentication (mock)
    mfa_var = tk.BooleanVar()
    mfa_check = tk.Checkbutton(security_frame, text="Enable Two-Factor Authentication", variable=mfa_var, font=("Arial", 12))
    mfa_check.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=5)

    return frame

