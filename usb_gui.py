import tkinter as tk
from tkinter import messagebox, PhotoImage
from usb_monitor import monitor_usb, block_usb, unblock_usb
import threading

def show_controls():
    def handle_block():
        block_usb()
        messagebox.showinfo("USB Blocked", "USB ports have been disabled!")

    def handle_unblock():
        unblock_usb()
        messagebox.showinfo("USB Enabled", "USB ports have been enabled!")

    def start_monitor():
        threading.Thread(target=monitor_usb, daemon=True).start()


    # GUI Setup
    root = tk.Toplevel()
    root.title("USB Physical Security For Systems")
    root.configure(bg='black')
    root.geometry("500x600")
    root.resizable(True, True)

    # Project Info Button
    def show_info():
        messagebox.showinfo("Project Info", "USB Physical Drive Security Project\nFeatures: USB block/unblock, Suspicious USB detection, Intruder logging.")

    info_btn = tk.Button(root, text="Project Info", bg='red', fg='white', font=('Arial', 14, 'bold'), command=show_info)
    info_btn.pack(pady=10)

    # Title
    title = tk.Label(root, text="USB Physical Security!!!", font=('Arial', 20, 'bold'), bg='black', fg='white')
    title.pack(pady=10)

    # Image
    try:
        img = PhotoImage(file="logo.ico")
        image_label = tk.Label(root, image=img, bg='black')
        image_label.pack(pady=10)
    except Exception as e:
        print("Image not loaded", e)

    # Control Panel
    panel = tk.Frame(root, bg='gray', bd=2)
    panel.pack(pady=20)

    block_btn = tk.Button(panel, text="Disable USB", bg='red', fg='white', font=('Arial', 14), width=20, command=handle_block)
    block_btn.pack(pady=10)

    unblock_btn = tk.Button(panel, text="Enable USB", bg='red', fg='white', font=('Arial', 14), width=20, command=handle_unblock)
    unblock_btn.pack(pady=10)

    start_monitor()
    # root.mainloop()