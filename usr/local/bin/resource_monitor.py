import tkinter as tk
from tkinter import ttk
import socket
import platform
import psutil

def create_frame(notebook):
    frame = ttk.Frame(notebook)

    # タイトル
    title = tk.Label(frame, text="Resource Monitor", font=("Arial", 18, "bold"))
    title.pack(pady=10)

    # 基本情報
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_info = f"{platform.system()} {platform.release()}"

    info_text = f"""
Host：{hostname}
IPadress：{ip_address}
OS：{os_info}
"""
    info_label = tk.Label(frame, text=info_text.strip(), justify="left", font=("Consolas", 12), anchor="w")
    info_label.pack(padx=20, anchor="w")

    # グラフ共通設定
    graph_width = 600
    graph_height = 150

    # グラフエリア（2列表示にするためのフレーム）
    graph_frame = tk.Frame(frame)
    graph_frame.pack()

    canvas_cpu = tk.Canvas(graph_frame, width=graph_width, height=graph_height, bg="white", highlightthickness=1, highlightbackground="gray")
    canvas_traffic = tk.Canvas(graph_frame, width=graph_width, height=graph_height, bg="white", highlightthickness=1, highlightbackground="gray")
    canvas_memory = tk.Canvas(graph_frame, width=graph_width, height=graph_height, bg="white", highlightthickness=1, highlightbackground="gray")
    canvas_disk = tk.Canvas(graph_frame, width=graph_width, height=graph_height, bg="white", highlightthickness=1, highlightbackground="gray")

    # 2列に並べて配置
    canvas_cpu.grid(row=0, column=0, padx=10, pady=10)
    canvas_traffic.grid(row=0, column=1, padx=10, pady=10)
    canvas_memory.grid(row=1, column=0, padx=10, pady=10)
    canvas_disk.grid(row=1, column=1, padx=10, pady=10)


    # データ初期化
    cpu_data = [0] * 60
    traffic_sent = [0] * 60
    traffic_recv = [0] * 60
    mem_data = [0] * 60
    disk_data = [0] * 60

    prev_sent = psutil.net_io_counters().bytes_sent
    prev_recv = psutil.net_io_counters().bytes_recv

    def draw_line_graph(canvas, data, label, color, y_max, unit="%"):
        canvas.delete("all")
        canvas.create_line(40, 10, 40, graph_height - 20, fill="black")  # 縦軸
        canvas.create_line(40, graph_height - 20, graph_width - 10, graph_height - 20, fill="black")  # 横軸

        for i in range(1, len(data)):
            x1 = 40 + (i - 1) * ((graph_width - 50) / 59)
            y1 = graph_height - 20 - (data[i - 1] / y_max) * (graph_height - 30)
            x2 = 40 + i * ((graph_width - 50) / 59)
            y2 = graph_height - 20 - (data[i] / y_max) * (graph_height - 30)
            canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

        canvas.create_text(20, 20, text=f"{y_max}{unit}", fill="gray")
        canvas.create_text(20, graph_height - 20, text=f"0{unit}", fill="gray")
        canvas.create_text(graph_width / 2, graph_height - 5, text=label, fill="gray")

    def update():
        nonlocal prev_sent, prev_recv

        # CPU
        cpu = psutil.cpu_percent()
        cpu_data.append(cpu)
        cpu_data.pop(0)

        # Traffic
        net = psutil.net_io_counters()
        sent_diff = net.bytes_sent - prev_sent
        recv_diff = net.bytes_recv - prev_recv
        prev_sent, prev_recv = net.bytes_sent, net.bytes_recv
        traffic_sent.append(sent_diff)
        traffic_recv.append(recv_diff)
        traffic_sent.pop(0)
        traffic_recv.pop(0)

        # Memory
        mem_percent = psutil.virtual_memory().percent
        mem_data.append(mem_percent)
        mem_data.pop(0)

        # Disk
        disk_percent = psutil.disk_usage("/").percent
        disk_data.append(disk_percent)
        disk_data.pop(0)

        # 描画
        draw_line_graph(canvas_cpu, cpu_data, "CPU", "blue", 100)
        # 通信量は送受信2本描画
        canvas_traffic.delete("all")
        canvas_traffic.create_line(40, 10, 40, graph_height - 20, fill="black")
        canvas_traffic.create_line(40, graph_height - 20, graph_width - 10, graph_height - 20, fill="black")
        max_traffic = max(max(traffic_sent), max(traffic_recv), 1)
        for i in range(1, 60):
            x1 = 40 + (i - 1) * ((graph_width - 50) / 59)
            x2 = 40 + i * ((graph_width - 50) / 59)
            y1_sent = graph_height - 20 - (traffic_sent[i - 1] / max_traffic) * (graph_height - 30)
            y2_sent = graph_height - 20 - (traffic_sent[i] / max_traffic) * (graph_height - 30)
            canvas_traffic.create_line(x1, y1_sent, x2, y2_sent, fill="red", width=2)
            y1_recv = graph_height - 20 - (traffic_recv[i - 1] / max_traffic) * (graph_height - 30)
            y2_recv = graph_height - 20 - (traffic_recv[i] / max_traffic) * (graph_height - 30)
            canvas_traffic.create_line(x1, y1_recv, x2, y2_recv, fill="green", width=2)
        ##canvas_traffic.create_text(20, 20, text="↑多", fill="gray")
        canvas_traffic.create_text(20, graph_height - 20, text="0", fill="gray")
        canvas_traffic.create_text(graph_width / 2, graph_height - 5, text="Traffic（send:red、recv:green）", fill="gray")

        draw_line_graph(canvas_memory, mem_data, "Memory", "purple", 100)
        draw_line_graph(canvas_disk, disk_data, "Storage", "orange", 100)

        frame.after(1000, update)

    update()
    return frame
