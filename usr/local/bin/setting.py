import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import subprocess
import os

# バージョン情報とアップデート確認機能をインポート
from client import get_application_version

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

    return frame