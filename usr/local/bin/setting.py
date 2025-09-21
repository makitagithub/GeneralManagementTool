import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import subprocess
import os

# バージョン情報とアップデート確認機能をインポート
from client import get_application_version

def create_frame(parent):
    frame = tk.Frame(parent, width=1600, height=900)
    frame.pack_propagate(False)

    # タイトル（画面中央）
    title = tk.Label(frame, text="Settings", font=("Arial", 18, "bold"))
    title.pack(pady=10)

    version_label = tk.Label(frame, text="Version: 1.0.0", font=("Arial", 16))
    version_label.pack(pady=30)

def update_application():
    """設定画面から呼び出されるアップデート関数"""
    # ここにダウンロードする特定の.debファイルのURLを指定
    download_url = "http://10.0.2.15/update/GeneralManagementTool-v2.1.0.deb"

    try:
        # ダウンロード
        messagebox.showinfo("ソフトウェア更新", "アップデートファイルをダウンロード中...")
        res = requests.get(download_url, stream=True)
        res.raise_for_status()

        deb_filename = os.path.basename(download_url)
        temp_file_path = f"/tmp/{deb_filename}"

        with open(temp_file_path, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # インストールコマンドを実行 (管理者権限が必要)
        messagebox.showinfo("ソフトウェア更新", "アップデートをインストール中...パスワードが求められます。")
        install_command = ["sudo", "dpkg", "-i", temp_file_path]
        subprocess.run(install_command, check=True)

        messagebox.showinfo("更新完了", "アプリケーションは最新版に更新されました。再起動してください。")
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("エラー", f"ダウンロードに失敗しました: {e}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("エラー", f"インストールの実行に失敗しました: {e}")

def create_frame(notebook):
    frame = tk.Frame(notebook)
    
    # バージョン情報
    version_label = tk.Label(frame, text=f"バージョン: {get_application_version()}")
    version_label.pack(pady=20)

    # ソフトウェア更新ボタン
    update_button = ttk.Button(frame, text="ソフトウェア更新", command=update_application)
    update_button.pack(pady=10)

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