import socket
import threading
import tkinter as tk
from tkinter import messagebox
import pyautogui
import io
import time
from functions import file_config

class SenderClient:
    def __init__(self, master, ip_server):
        self.master = master
        self.ip_server = ip_server
        self.sock = None
        self.running = False

        master.title("سندر - اشتراک صفحه")
        master.configure(bg="#f0f0f0")
        master.minsize(400, 300)

        # مرکز صفحه
        main_frame = tk.Frame(master, bg="#f0f0f0")
        main_frame.pack(expand=True)

        title = tk.Label(main_frame, text="اتصال به سرور", font=("Segoe UI", 16, "bold"), bg="#f0f0f0")
        title.pack(pady=(20, 10))

        # IP Input
        tk.Label(main_frame, text="IP سرور:", font=("Segoe UI", 12), bg="#f0f0f0").pack(anchor="w", padx=20)
        self.ip_entry = tk.Entry(main_frame, width=30, font=("Segoe UI", 11))
        self.ip_entry.insert(0, self.ip_server)
        self.ip_entry.pack(pady=5)

        # کد ویور
        tk.Label(main_frame, text="کد ویور:", font=("Segoe UI", 12), bg="#f0f0f0").pack(anchor="w", padx=20)
        self.code_entry = tk.Entry(main_frame, width=20, font=("Segoe UI", 11))
        self.code_entry.pack(pady=5)

        # دکمه ارسال
        self.send_button = tk.Button(
            main_frame, text="🚀 شروع ارسال", font=("Segoe UI", 12),
            bg="#4CAF50", fg="white", padx=10, pady=5, command=self.start_sending
        )
        self.send_button.pack(pady=20)

        # وضعیت
        self.status_label = tk.Label(
            main_frame, text="وضعیت: آماده", fg="#333", bg="#f0f0f0",
            font=("Segoe UI", 11, "italic")
        )
        self.status_label.pack(pady=10)

        # بستن امن
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

                time.sleep(0.2)
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
    IP_SERVER = file_config()
    if IP_SERVER:
        root = tk.Tk()
        app = SenderClient(root, IP_SERVER)
        root.mainloop()
