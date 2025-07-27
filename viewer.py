import socket
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import json


class ViewerClient:
    def __init__(self, master, ip_server):
        self.master = master
        self.ip_server = ip_server
        self.sock = None
        self.running = False
        self.current_image = None

        self.fullscreen = tk.BooleanVar()

        # تنظیمات پنجره اصلی
        master.title("ویوور تصویر")
        master.geometry("900x600")
        master.configure(bg="#f5f5f5")
        master.minsize(600, 400)

        # ساخت فریم اصلی
        main_frame = tk.Frame(master, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # فریم بالایی برای تنظیمات
        top_frame = tk.Frame(main_frame, bg="#f5f5f5")
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # فیلد IP
        tk.Label(top_frame, text="IP سرور:", font=("Segoe UI", 11), bg="#f5f5f5").grid(row=0, column=0, sticky="w")
        self.ip_entry = tk.Entry(top_frame, font=("Segoe UI", 11), width=20)
        self.ip_entry.insert(0, self.ip_server)
        self.ip_entry.grid(row=0, column=1, padx=5)

        # دکمه اتصال
        self.connect_button = tk.Button(top_frame, text="اتصال", font=("Segoe UI", 10, "bold"),
                                        bg="#4caf50", fg="white", padx=10, command=self.connect)
        self.connect_button.grid(row=0, column=2, padx=10)

        # نمایش کد ویوور
        self.code_label = tk.Label(main_frame, text="کد شما: ---", font=("Segoe UI", 12), fg="#1e88e5", bg="#f5f5f5")
        self.code_label.pack()

        # گزینه تمام‌صفحه
        tk.Checkbutton(main_frame, text="نمایش تمام صفحه", variable=self.fullscreen, onvalue=True, offvalue=False,
                       font=("Segoe UI", 10), bg="#f5f5f5").pack()

        # فریم نمایش تصویر
        self.image_label = tk.Label(main_frame, bg="#000")
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=10)

        self.master.bind("<Escape>", lambda e: self.master.attributes('-fullscreen', False))
        self.master.bind("<Configure>", self.on_resize)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def connect(self):
        ip = self.ip_entry.get().strip()
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, 5000))
            self.sock.sendall(b'VIEWER')
            code = self.sock.recv(1024).decode()
            self.code_label.config(text=f"کد شما: {code}")
            self.running = True

            if self.fullscreen.get():
                self.master.attributes('-fullscreen', True)

            threading.Thread(target=self.receive_images, daemon=True).start()

        except Exception as e:
            messagebox.showerror("خطا", f"اتصال ممکن نیست:\n{e}")

    def receive_images(self):
        while self.running:
            try:
                length_data = self.sock.recv(8)
                if not length_data:
                    break
                img_size = int(length_data.decode())
                img_data = b''
                while len(img_data) < img_size:
                    chunk = self.sock.recv(img_size - len(img_data))
                    if not chunk:
                        return
                    img_data += chunk

                image = Image.open(io.BytesIO(img_data))
                self.current_image = image
                self.show_image(image)

            except Exception as e:
                print(f"[ERROR] در دریافت تصویر: {e}")
                break

    def show_image(self, image):
        if not self.running:
            return

        window_width = self.image_label.winfo_width() or 400
        window_height = self.image_label.winfo_height() or 300

        img_ratio = image.width / image.height
        window_ratio = window_width / window_height

        if window_ratio > img_ratio:
            new_height = window_height
            new_width = int(new_height * img_ratio)
        else:
            new_width = window_width
            new_height = int(new_width / img_ratio)

        resized = image.resize((new_width, new_height), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(resized)

        self.image_label.config(image=tk_img)
        self.image_label.image = tk_img

    def on_resize(self, event):
        if self.current_image:
            self.show_image(self.current_image)

    def on_close(self):
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    with open('file.config', 'r', encoding='utf-8') as file:
        data = json.load(file)
    IP_SERVER = data['IP_SERVER']
    app = ViewerClient(root, IP_SERVER)
    root.mainloop()
