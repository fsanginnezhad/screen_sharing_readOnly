# 📡 Screen Share System - Python GUI over Network

A complete cross-device screen-sharing solution built with Python. Includes a GUI server, viewer, and sender — all connected via local network or the internet. Perfect for remote monitoring, support, or presentations.

---

## 🚀 Features

- 🖥️ Graphical Server with live client status
- 📺 Viewer receives real-time screen images
- 📤 Sender captures and transmits full screen using `pyautogui`
- 🔑 Secure session via viewer code (1-to-1 mapping)
- 🧭 Fullscreen toggle for viewers
- 🔌 Works on LAN or over the Internet
- 🎨 Clean and responsive GUI (Tkinter)

---

## 🧱 Project Structure

```
.
├── server.py     # Graphical server managing viewer codes and connections
├── viewer.py     # Connects to server and receives live screen feed
├── sender.py     # Captures and sends full-screen image to a viewer
├── README.md     # Project documentation
```

---

## 🛠️ Requirements

```bash
pip install -r requirements.txt
```

> 📝 Make sure to allow screen capture permissions (especially on macOS)

---

## 📦 How to Run

### 1️⃣ Run Server

```bash
python server.py
```

- Waits for incoming viewer/sender connections
- Shows live list of viewers + generated codes
- You can start/stop the server from the GUI

---

### 2️⃣ Run Viewer

```bash
python viewer.py
```

- Enter server IP
- Receives a unique code from server
- Displays live screen images
- Click **"Fullscreen"** to enter immersive mode

---

### 3️⃣ Run Sender

```bash
python sender.py
```

- Enter server IP and the viewer code (given by the viewer)
- Captures your full screen using `pyautogui`
- Streams image to viewer in real time

---

## 🌐 Access Over the Internet

This app supports external access beyond local network.

### To do that:

1. Deploy the `server.py` on a VPS with public IP
2. Make sure port **5000** is open in firewall and router
3. Viewer and Sender can then connect via the server's **public IP**

> ⚠️ Encryption and authentication are not implemented in v1 — use a VPN or tunnel (like `ngrok`) if security is a concern

---

## 🔐 Security Notice

This is a proof-of-concept version.

Planned features for production:
- 🔒 TLS encryption (SSL)
- 🔑 Password protection for viewer codes
- ⛔ IP/port filtering & access control

---

## 📤 Packaging as EXE (Optional)

Using `pyinstaller`:

```bash
pyinstaller --onefile --noconsole server.py
pyinstaller --onefile --noconsole viewer.py
pyinstaller --onefile --noconsole sender.py
```

You can also use `auto-py-to-exe` for GUI-based build.

---

## 🤝 Contributing

Want to help improve this? Fork the repo, submit PRs, or open an issue!  
All ideas and bug reports are welcome.

---

## 👨‍💻 Developer

Built with ❤️ in Python 3  
Created by: [ّFarshad Sanginnezhad](https://github.com/fsanginnezhad/)

---

## 📄 License

MIT License — free for personal or commercial use.

---

## 💬 Contact

Have questions or ideas? Reach out via GitHub or email.
