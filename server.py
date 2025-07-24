# import socket
# import threading
# import tkinter as tk
# from tkinter import messagebox

# class ServerApp:
#     def __init__(self, master):
#         self.master = master
#         master.title("🖥️ سرور - مدیریت اتصال")
#         master.geometry("420x330")
#         master.configure(bg="#f8f8f8")

#         self.server_socket = None
#         self.clients = {}
#         self.viewer_codes = {}
#         self.running = False
#         self.next_code = 1000

#         self.build_ui()

#     def build_ui(self):
#         title = tk.Label(self.master, text="سرور اشتراک‌گذاری", font=("Helvetica", 16, "bold"), bg="#f8f8f8")
#         title.pack(pady=10)

#         self.status_label = tk.Label(self.master, text="وضعیت: آفلاین", fg="red", font=("Helvetica", 12), bg="#f8f8f8")
#         self.status_label.pack(pady=5)

#         btn_frame = tk.Frame(self.master, bg="#f8f8f8")
#         btn_frame.pack(pady=10)

#         self.start_button = tk.Button(btn_frame, text="شروع سرور", bg="#4CAF50", fg="white", width=15, command=self.start_server)
#         self.start_button.grid(row=0, column=0, padx=10)

#         self.stop_button = tk.Button(btn_frame, text="توقف سرور", bg="#F44336", fg="white", width=15, command=self.stop_server)
#         self.stop_button.grid(row=0, column=1, padx=10)
#         self.stop_button.config(state=tk.DISABLED)

#         tk.Label(self.master, text="ویورها:", font=("Helvetica", 12), bg="#f8f8f8").pack(pady=5)

#         self.viewer_listbox = tk.Listbox(self.master, height=10, width=45)
#         self.viewer_listbox.pack(pady=5)

#         self.master.protocol("WM_DELETE_WINDOW", self.on_close)

#     def start_server(self):
#         try:
#             self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self.server_socket.bind(('', 5000))
#             self.server_socket.listen(5)
#             self.running = True
#             self.status_label.config(text="وضعیت: آنلاین", fg="green")
#             self.start_button.config(state=tk.DISABLED)
#             self.stop_button.config(state=tk.NORMAL)
#             threading.Thread(target=self.accept_clients, daemon=True).start()
#         except Exception as e:
#             messagebox.showerror("خطا", f"راه‌اندازی سرور ممکن نیست:\n{e}")

#     def accept_clients(self):
#         while self.running:
#             try:
#                 client_sock, addr = self.server_socket.accept()
#                 client_type = client_sock.recv(1024).decode()

#                 if client_type == "VIEWER":
#                     code = str(self.next_code)
#                     self.next_code += 1
#                     self.viewer_codes[code] = client_sock
#                     self.clients[client_sock] = ("VIEWER", code)
#                     client_sock.sendall(code.encode())
#                     self.viewer_listbox.insert(tk.END, f"{addr[0]} - کد: {code}")
#                     print(f"[NEW VIEWER] {addr} - Code {code}")
#                 elif client_type == "SENDER":
#                     threading.Thread(target=self.handle_sender, args=(client_sock,), daemon=True).start()
#             except Exception as e:
#                 if self.running:
#                     print(f"[ERROR] در اتصال کلاینت: {e}")

#     def handle_sender(self, sender_sock):
#         try:
#             code = sender_sock.recv(1024).decode().strip()
#             if code not in self.viewer_codes:
#                 sender_sock.sendall(b"INVALID")
#                 sender_sock.close()
#                 return

#             sender_sock.sendall(b"OK")
#             viewer_sock = self.viewer_codes[code]

#             while self.running:
#                 length_data = sender_sock.recv(8)
#                 if not length_data:
#                     break
#                 img_size = int(length_data.decode())
#                 img_data = b''
#                 while len(img_data) < img_size:
#                     chunk = sender_sock.recv(img_size - len(img_data))
#                     if not chunk:
#                         break
#                     img_data += chunk

#                 viewer_sock.sendall(length_data)
#                 viewer_sock.sendall(img_data)

#         except Exception as e:
#             print(f"[ERROR] در ارتباط با سندر: {e}")
#         finally:
#             sender_sock.close()

#     def stop_server(self):
#         self.running = False
#         try:
#             if self.server_socket:
#                 self.server_socket.close()
#                 self.server_socket = None
#         except:
#             pass

#         for sock in self.clients:
#             try:
#                 sock.close()
#             except:
#                 pass
#         self.clients.clear()
#         self.viewer_codes.clear()
#         self.viewer_listbox.delete(0, tk.END)
#         self.status_label.config(text="وضعیت: آفلاین", fg="red")
#         self.start_button.config(state=tk.NORMAL)
#         self.stop_button.config(state=tk.DISABLED)

#     def on_close(self):
#         self.stop_server()
#         self.master.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ServerApp(root)
#     root.mainloop()








import socket
import threading
import tkinter as tk
from tkinter import messagebox
import random
import string

HOST = '0.0.0.0'
PORT = 5000
hostname = socket.gethostname()
IP_SERVER = socket.gethostbyname(hostname)

connections = {}  # key: code, value: {'viewer': conn, 'sender': conn}

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
            role = conn.recv(1024).decode().strip()  # 'VIEWER' or 'SENDER'
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
        status_label_ip.config(text=f"IP Server: {IP_SERVER}:{PORT}", fg="blue")
    except:
        messagebox.showerror("خطا", "خطا در راه‌اندازی سرور")

def go_offline():
    server.stop()
    status_label.config(text="وضعیت: آفلاین", fg="red")
    status_label_ip.config(text="")

root = tk.Tk()
root.title("سرور اشتراک صفحه")

root.geometry("300x200")
tk.Label(root, text="سرور اشتراک صفحه", font=("Helvetica", 16)).pack(pady=10)

status_label = tk.Label(root, text="وضعیت: آفلاین", fg="red", font=("Helvetica", 12))
status_label.pack(pady=5)

tk.Button(root, text="آنلاین شدن", width=20, command=go_online).pack(pady=5)
tk.Button(root, text="آفلاین شدن", width=20, command=go_offline).pack(pady=5)

status_label_ip = tk.Label(root, text="", fg="black", font=("Helvetica", 12))
status_label_ip.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", lambda: (server.stop(), root.destroy()))
root.mainloop()