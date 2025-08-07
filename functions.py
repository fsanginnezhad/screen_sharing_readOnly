import json
from tkinter import messagebox


def file_config():
    try:
        with open('file.config', 'r', encoding='utf-8') as file:
            data = json.load(file)
        IP_SERVER = data['IP_SERVER']
    except FileNotFoundError:
        messagebox.showerror("Error", "IP Server not found\nError 403")
        IP_SERVER = ''
    return IP_SERVER
