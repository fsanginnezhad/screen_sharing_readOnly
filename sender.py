# import socket
# import threading
# import tkinter as tk
# from tkinter import messagebox
# import pyautogui
# import time
# import io
# from PIL import Image

# class SenderClient:
#     def __init__(self, master):
#         self.master = master
#         master.title("📤 سندر - اشتراک‌گذاری صفحه")
#         master.geometry("400x250")
#         master.configure(bg="#f4f4f4")

#         self.sock = None
#         self.running = False

#         self.ip_var = tk.StringVar()
#         self.code_var = tk.StringVar()

#         self.build_ui()

#     def build_ui(self):
#         tk.Label(self.master, text="آدرس IP سرور:", font=("Helvetica", 11), bg="#f4f4f4").pack(pady=5)
#         tk.Entry(self.master, textvariable=self.ip_var, width=30).pack(pady=5)
#         self.ip_var.set('127.0.0.1')

#         tk.Label(self.master, text="کد ویور:", font=("Helvetica", 11), bg="#f4f4f4").pack(pady=5)
#         tk.Entry(self.master, textvariable=self.code_var, width=15).pack(pady=5)

#         self.start_button = tk.Button(self.master, text="شروع اشتراک‌گذاری", bg="#2196F3", fg="white", command=self.start_sharing)
#         self.start_button.pack(pady=15)

#         self.status_label = tk.Label(self.master, text="وضعیت: آماده", bg="#f4f4f4", fg="black")
#         self.status_label.pack(pady=5)

#         self.master.protocol("WM_DELETE_WINDOW", self.stop_sharing)

#     def start_sharing(self):
#         ip = self.ip_var.get().strip()
#         code = self.code_var.get().strip()
#         try:
#             self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self.sock.connect((ip, 5000))
#             self.sock.sendall(b'SENDER')
#             time.sleep(0.5)
#             self.sock.sendall(code.encode())
#             response = self.sock.recv(1024)
#             if response != b'OK':
#                 raise Exception("کد نامعتبر است.")
#             self.running = True
#             self.status_label.config(text="در حال ارسال تصویر...", fg="green")
#             threading.Thread(target=self.send_screen, daemon=True).start()
#         except Exception as e:
#             messagebox.showerror("خطا", str(e))

#     def send_screen(self):
#         try:
#             while self.running:
#                 screenshot = pyautogui.screenshot()
#                 with io.BytesIO() as output:
#                     screenshot.save(output, format='JPEG')
#                     data = output.getvalue()
#                 length = f"{len(data):08}".encode()
#                 self.sock.sendall(length)
#                 self.sock.sendall(data)
#                 time.sleep(0.1)
#         except Exception as e:
#             print(f"[ERROR] ارسال تصویر: {e}")
#         finally:
#             self.sock.close()

#     def stop_sharing(self):
#         self.running = False
#         if self.sock:
#             try:
#                 self.sock.close()
#             except:
#                 pass
#         self.master.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SenderClient(root)
#     root.mainloop()







import socket
import threading
import tkinter as tk
from tkinter import messagebox
import pyautogui
from PIL import Image
import io
import time
import json

class SenderClient:
    def __init__(self, master, ip_server):
        self.master = master
        self.ip_server = ip_server
        self.sock = None
        self.running = False

        master.title("سندر - اشتراک صفحه")
        master.geometry("400x300")

        tk.Label(master, text="IP سرور:", font=("Helvetica", 12)).pack()
        self.ip_entry = tk.Entry(master, width=30)
        self.ip_entry.insert(0, self.ip_server)
        self.ip_entry.pack(pady=5)

        tk.Label(master, text="کد ویور:", font=("Helvetica", 12)).pack()
        self.code_entry = tk.Entry(master, width=20)
        self.code_entry.pack(pady=5)

        self.send_button = tk.Button(master, text="شروع ارسال", command=self.start_sending)
        self.send_button.pack(pady=15)

        self.status_label = tk.Label(master, text="وضعیت: آماده", fg="blue")
        self.status_label.pack(pady=10)

        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_sending(self):
        ip = self.ip_entry.get().strip()
        code = self.code_entry.get().strip()
        if not code:
            messagebox.showwarning("کد نیاز است", "لطفا کد ویور را وارد کنید")
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, 5000))
            self.sock.sendall(b'SENDER')
            time.sleep(0.5)
            response = self.sock.recv(1024)
            if response == b'CODE?':
                self.sock.sendall(code.encode())
                self.status_label.config(text="در حال ارسال تصویر...", fg="green")
                self.running = True
                threading.Thread(target=self.send_loop, daemon=True).start()
            else:
                messagebox.showerror("کد نامعتبر", "کد وارد شده اشتباه است یا ویور فعال نیست.")
                self.sock.close()
        except Exception as e:
            messagebox.showerror("خطا", f"اتصال ممکن نیست:\n{e}")

    def send_loop(self):
        try:
            while self.running:
                screenshot = pyautogui.screenshot()
                with io.BytesIO() as buffer:
                    screenshot.save(buffer, format="JPEG", quality=50)
                    img_bytes = buffer.getvalue()

                size_str = f"{len(img_bytes):08}".encode()
                self.sock.sendall(size_str + img_bytes)

                time.sleep(0.2)  # ارسال هر 0.5 ثانیه
        except Exception as e:
            print(f"[ERROR] در ارسال تصویر: {e}")
            self.status_label.config(text="خطا در ارسال", fg="red")
        finally:
            self.sock.close()

    def on_close(self):
        self.running = False
        try:
            if self.sock:
                self.sock.close()
        except:
            pass
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    with open('file.config', 'r', encoding='utf-8') as file:
        data = json.load(file)
    IP_SERVER = data['IP_SERVER']
    app = SenderClient(root, IP_SERVER)
    root.mainloop()
