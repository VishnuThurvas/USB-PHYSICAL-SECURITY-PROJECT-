import tkinter as tk
from tkinter import messagebox
import usb_gui
import view_logs

def show_dashboard():
    dash = tk.Tk()
    dash.title("USB Security Dashboard")
    dash.geometry("500x400")

    tk.Label(dash, text="Welcome to USB Security", font=("Arial", 16)).pack(pady=20)

    tk.Button(dash, text="View USB Logs", command=view_logs.show_logs, width=30).pack(pady=10)
    tk.Button(dash, text="USB Controls", command=usb_gui.show_controls, width=30).pack(pady=10)
    tk.Button(dash, text="Exit", command=dash.destroy, width=30).pack(pady=10)

    dash.mainloop()