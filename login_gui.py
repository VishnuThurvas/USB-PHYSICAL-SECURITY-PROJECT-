import tkinter as tk
from tkinter import messagebox
from database import create_tables, register_user, validate_user
import dashboard_gui

def open_dashboard():
    root.destroy()
    dashboard_gui.show_dashboard()

def register():
    if register_user(username_entry.get(), email_entry.get(), password_entry.get()):
        messagebox.showinfo("Success", "Registered successfully!")
    else:
        messagebox.showerror("Error", "User already exists!")

def login():
    if validate_user(email_entry.get(), password_entry.get()):
        messagebox.showinfo("Success", "Login successful!")
        open_dashboard()
    else:
        messagebox.showerror("Error", "Invalid credentials.")

create_tables()

root = tk.Tk()
root.title("USB Security Login")
root.geometry("300x300")

tk.Label(root, text="Username").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Register", command=register).pack(pady=10)
tk.Button(root, text="Login", command=login).pack()

root.mainloop()