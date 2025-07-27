import socket
import threading
import tkinter as tk
from tkinter import messagebox
import random
import string
from functions import file_config

HOST = '0.0.0.0'
PORT = 5000
IP_SERVER = file_config()

connections = {}

def generate_code(length=10):
    return ''.join(random.choices(string.digits, k=length))

class Server:
    def __init__(self):
        self.server_socket = None
        self.running = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(5)
        self.running = True
        print(f"[SERVER] Listening on {IP_SERVER}:{PORT}")
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
        print("[SERVER] Stopped.")

    def accept_connections(self):
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                print(f"[CONNECTION] From {addr}")
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()
            except:
                break

    def handle_client(self, conn):
        try:
            role = conn.recv(1024).decode().strip()
            if role == 'VIEWER':
                code = generate_code()
                connections[code] = {'viewer': conn, 'sender': None}
                conn.sendall(code.encode())
                print(f"[VIEWER] Code {code} assigned.")
            elif role == 'SENDER':
                conn.sendall(b'CODE?')
                code = conn.recv(1024).decode().strip()
                if code in connections and connections[code]['sender'] is None:
                    connections[code]['sender'] = conn
                    print(f"[SENDER] Connected to viewer {code}")
                    self.relay_data(code)
                else:
                    conn.sendall(b'INVALID')
                    conn.close()
        except Exception as e:
            print(f"[ERROR] {e}")

    def relay_data(self, code):
        viewer = connections[code]['viewer']
        sender = connections[code]['sender']
        try:
            while True:
                length_data = sender.recv(8)
                if not length_data:
                    break
                img_size = int(length_data.decode())
                img_data = b''
                while len(img_data) < img_size:
                    img_data += sender.recv(img_size - len(img_data))
                viewer.sendall(length_data + img_data)
        except Exception as e:
            print(f"[RELAY ERROR] {e}")
        finally:
            viewer.close()
            sender.close()
            del connections[code]

server = Server()

# ---------------- GUI ---------------- #

def go_online():
    try:
        server.start()
        status_label.config(text="وضعیت: آنلاین", fg="green")
        status_label_ip.config(text=f"IP سرور: {IP_SERVER}:{PORT}", fg="#444")
    except:
        messagebox.showerror("خطا", "خطا در راه‌اندازی سرور")

def go_offline():
    server.stop()
    status_label.config(text="وضعیت: آفلاین", fg="red")
    status_label_ip.config(text="")

if IP_SERVER:
    root = tk.Tk()
    root.title("📡 سرور اشتراک صفحه")
    root.geometry("350x250")
    root.configure(bg="#f4f4f4")

    # ---- استایل ---- #
    title = tk.Label(root, text="مدیریت سرور اشتراک صفحه", font=("Segoe UI", 16, "bold"), bg="#f4f4f4")
    title.pack(pady=(20, 10))

    status_label = tk.Label(root, text="وضعیت: آفلاین", fg="red", font=("Segoe UI", 12), bg="#f4f4f4")
    status_label.pack(pady=5)

    btn_frame = tk.Frame(root, bg="#f4f4f4")
    btn_frame.pack(pady=10)

    online_btn = tk.Button(
        btn_frame, text="🟢 آنلاین شدن", font=("Segoe UI", 11), width=15,
        bg="#4CAF50", fg="white", command=go_online
    )
    online_btn.grid(row=0, column=0, padx=5)

    offline_btn = tk.Button(
        btn_frame, text="🔴 آفلاین شدن", font=("Segoe UI", 11), width=15,
        bg="#F44336", fg="white", command=go_offline
    )
    offline_btn.grid(row=0, column=1, padx=5)

    status_label_ip = tk.Label(root, text="", fg="#333", font=("Segoe UI", 11), bg="#f4f4f4")
    status_label_ip.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: (server.stop(), root.destroy()))
    root.mainloop()
