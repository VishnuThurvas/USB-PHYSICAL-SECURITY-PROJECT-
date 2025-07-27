# usb_gui.py
import tkinter as tk
from tkinter import messagebox, PhotoImage
from usb_monitor import detect_suspicious_usb, block_usb, unblock_usb
import threading


def handle_block():
    block_usb()
    messagebox.showinfo("USB Blocked", "USB ports have been disabled!")

def handle_unblock():
    unblock_usb()
    messagebox.showinfo("USB Enabled", "USB ports have been enabled!")

def start_monitor():
    threading.Thread(target=detect_suspicious_usb, daemon=True).start()


# GUI Setup
root = tk.Tk()
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
    img = PhotoImage(file="usb_icon.png")
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
root.mainloop()


# usb_monitor.py
import os
import time
import subprocess
import smtplib
from email.message import EmailMessage
from intruder import record_intruder_video

def send_alert_email():
    msg = EmailMessage()
    msg.set_content("Alert: Malicious USB device detected and blocked.")
    msg["Subject"] = "USB Security Alert"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = "user_email@gmail.com"

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("your_email@gmail.com", "your_password")
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("Failed to send email:", e)

def detect_suspicious_usb():
    known_ids = set()
    while True:
        result = subprocess.run("wmic logicaldisk get name", capture_output=True, text=True, shell=True)
        drives = set([line.strip() for line in result.stdout.splitlines() if ":" in line])
        new_drives = drives - known_ids
        if new_drives:
            print("New USB detected:", new_drives)
            record_intruder_video()
            send_alert_email()
            block_usb()
        known_ids = drives
        time.sleep(5)

def block_usb():
    os.system("reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 4 /f")

def unblock_usb():
    os.system("reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 3 /f")
