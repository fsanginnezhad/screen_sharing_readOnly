import socket
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io

class ViewerClient:
    def __init__(self, master):
        self.master = master
        self.sock = None
        self.running = False

        self.fullscreen = tk.BooleanVar()
        self.custom_width = tk.StringVar()
        self.custom_height = tk.StringVar()

        master.title("ویور - دریافت تصویر")
        master.geometry("1280x768")

        # بخش ورودی IP
        tk.Label(master, text="IP سرور:", font=("Helvetica", 12)).pack()
        self.ip_entry = tk.Entry(master, width=30)
        self.ip_entry.insert(0, '127.0.0.1')
        self.ip_entry.pack(pady=5)

        # دکمه اتصال
        self.connect_button = tk.Button(master, text="اتصال", command=self.connect)
        self.connect_button.pack(pady=10)

        # نمایش کد ویور
        self.code_label = tk.Label(master, text="کد شما: ---", font=("Helvetica", 14), fg="blue")
        self.code_label.pack(pady=10)

        # گزینه Fullscreen
        tk.Checkbutton(master, text="نمایش تمام صفحه", variable=self.fullscreen, onvalue=True, offvalue=False).pack(pady=5)

        # ورودی سایز سفارشی
        tk.Label(master, text="سایز سفارشی (اختیاری):").pack()
        size_frame = tk.Frame(master)
        tk.Label(size_frame, text="عرض:").pack(side=tk.LEFT)
        tk.Entry(size_frame, width=5, textvariable=self.custom_width).pack(side=tk.LEFT)
        tk.Label(size_frame, text="ارتفاع:").pack(side=tk.LEFT)
        tk.Entry(size_frame, width=5, textvariable=self.custom_height).pack(side=tk.LEFT)
        size_frame.pack(pady=5)

        # بخش نمایش تصویر
        self.image_label = tk.Label(master)
        self.image_label.pack(expand=True)

        self.master.bind("<Escape>", lambda e: self.master.attributes('-fullscreen', False))
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

                # انتخاب سایز تصویر
                if self.fullscreen.get():
                    self.master.attributes('-fullscreen', True)
                    screen_width = self.master.winfo_screenwidth()
                    screen_height = self.master.winfo_screenheight()
                    image = image.resize((screen_width, screen_height))
                elif self.custom_width.get().isdigit() and self.custom_height.get().isdigit():
                    w = int(self.custom_width.get())
                    h = int(self.custom_height.get())
                    image = image.resize((w, h))
                else:
                    image = image.resize((400, 300))  # پیش‌فرض

                tk_img = ImageTk.PhotoImage(image)
                self.image_label.config(image=tk_img)
                self.image_label.image = tk_img
            except Exception as e:
                print(f"[ERROR] در دریافت تصویر: {e}")
                break

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
    app = ViewerClient(root)
    root.mainloop()






# import socket
# import threading
# import tkinter as tk
# from tkinter import messagebox
# from PIL import Image, ImageTk
# import io

# class ViewerClient:
#     def __init__(self, master):
#         self.master = master
#         self.sock = None
#         self.running = False

#         self.fullscreen = tk.BooleanVar()
#         self.custom_width = tk.StringVar()
#         self.custom_height = tk.StringVar()

#         master.title("🎥 ویور - نمایش صفحه")
#         master.geometry("1024x720")
#         master.configure(bg="#f0f0f0")

#         self.build_ui()
#         self.master.bind("<Escape>", lambda e: self.master.attributes('-fullscreen', False))
#         self.master.protocol("WM_DELETE_WINDOW", self.on_close)

#     def build_ui(self):
#         # بخش بالا برای تنظیمات
#         top_frame = tk.Frame(self.master, bg="#f0f0f0")
#         top_frame.pack(pady=10)

#         # IP سرور
#         tk.Label(top_frame, text="IP سرور:", font=("Helvetica", 11), bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=5)
#         self.ip_entry = tk.Entry(top_frame, width=25)
#         self.ip_entry.insert(0, '127.0.0.1')
#         self.ip_entry.grid(row=0, column=1, padx=5)

#         # دکمه اتصال
#         self.connect_button = tk.Button(top_frame, text="اتصال", command=self.connect, width=10, bg="#4CAF50", fg="white")
#         self.connect_button.grid(row=0, column=2, padx=10)

#         # کد ویور
#         self.code_label = tk.Label(self.master, text="کد شما: ---", font=("Helvetica", 14, "bold"), fg="#333", bg="#f0f0f0")
#         self.code_label.pack(pady=10)

#         # گزینه‌ها (fullscreen + سایز)
#         options_frame = tk.Frame(self.master, bg="#f0f0f0")
#         options_frame.pack(pady=5)

#         # Fullscreen
#         tk.Checkbutton(options_frame, text="تمام صفحه", variable=self.fullscreen, bg="#f0f0f0").grid(row=0, column=0, padx=10)

#         # سایز سفارشی
#         tk.Label(options_frame, text="عرض:", bg="#f0f0f0").grid(row=0, column=1)
#         tk.Entry(options_frame, width=5, textvariable=self.custom_width).grid(row=0, column=2, padx=5)

#         tk.Label(options_frame, text="ارتفاع:", bg="#f0f0f0").grid(row=0, column=3)
#         tk.Entry(options_frame, width=5, textvariable=self.custom_height).grid(row=0, column=4, padx=5)

#         # نمایش تصویر
#         self.image_frame = tk.Frame(self.master, bg="black")
#         self.image_frame.pack(expand=True, fill="both", pady=10, padx=10)

#         self.image_label = tk.Label(self.image_frame, bg="black")
#         self.image_label.pack(expand=True)

#     def connect(self):
#         ip = self.ip_entry.get().strip()
#         try:
#             self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self.sock.connect((ip, 5000))
#             self.sock.sendall(b'VIEWER')
#             code = self.sock.recv(1024).decode()
#             self.code_label.config(text=f"کد شما: {code}")
#             self.running = True
#             threading.Thread(target=self.receive_images, daemon=True).start()
#         except Exception as e:
#             messagebox.showerror("خطا", f"اتصال ممکن نیست:\n{e}")

#     def receive_images(self):
#         while self.running:
#             try:
#                 length_data = self.sock.recv(8)
#                 if not length_data:
#                     break
#                 img_size = int(length_data.decode())
#                 img_data = b''
#                 while len(img_data) < img_size:
#                     chunk = self.sock.recv(img_size - len(img_data))
#                     if not chunk:
#                         return
#                     img_data += chunk

#                 image = Image.open(io.BytesIO(img_data))

#                 # تعیین اندازه تصویر
#                 if self.fullscreen.get():
#                     self.master.attributes('-fullscreen', True)
#                     w = self.master.winfo_screenwidth()
#                     h = self.master.winfo_screenheight()
#                     image = image.resize((w, h))
#                 elif self.custom_width.get().isdigit() and self.custom_height.get().isdigit():
#                     w = int(self.custom_width.get())
#                     h = int(self.custom_height.get())
#                     image = image.resize((w, h))
#                 else:
#                     image = image.resize((600, 400))

#                 tk_img = ImageTk.PhotoImage(image)
#                 self.image_label.config(image=tk_img)
#                 self.image_label.image = tk_img
#             except Exception as e:
#                 print(f"[ERROR] در دریافت تصویر: {e}")
#                 break

#     def on_close(self):
#         self.running = False
#         if self.sock:
#             try:
#                 self.sock.close()
#             except:
#                 pass
#         self.master.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ViewerClient(root)
#     root.mainloop()
