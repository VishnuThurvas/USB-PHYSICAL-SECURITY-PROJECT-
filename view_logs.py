import tkinter as tk
import sqlite3
from tkinter import ttk

def show_logs():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usb_logs")
    logs = cursor.fetchall()
    conn.close()

    win = tk.Toplevel()
    win.title("USB Logs")
    win.geometry("600x300")

    tree = ttk.Treeview(win, columns=("Time", "Type", "Description"), show="headings")
    tree.heading("Time", text="Time")
    tree.heading("Type", text="Event Type")
    tree.heading("Description", text="Description")
    tree.pack(fill=tk.BOTH, expand=True)

    for log in logs:
        tree.insert("", tk.END, values=(log[1], log[2], log[3]))