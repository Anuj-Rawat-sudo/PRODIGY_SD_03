import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE_NAME = "contacts.json"

# -----------------------------
# Load Contacts
# -----------------------------
def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# -----------------------------
# Save Contacts
# -----------------------------
def save_contacts():
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)

contacts = load_contacts()

# -----------------------------
# Refresh Table
# -----------------------------
def refresh_table(data=None):
    for row in tree.get_children():
        tree.delete(row)

    if data is None:
        data = contacts

    for contact in data:
        tree.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"]))

# -----------------------------
# Add Contact
# -----------------------------
def add_contact():
    name = name_var.get().strip()
    phone = phone_var.get().strip()
    email = email_var.get().strip()

    if name == "" or phone == "" or email == "":
        messagebox.showerror("Error", "All fields are required.")
        return

    contacts.append({
        "name": name,
        "phone": phone,
        "email": email
    })

    save_contacts()
    refresh_table()
    clear_fields()

# -----------------------------
# Select Contact
# -----------------------------
def select_contact(event):
    selected = tree.focus()

    if not selected:
        return

    values = tree.item(selected, "values")

    name_var.set(values[0])
    phone_var.set(values[1])
    email_var.set(values[2])

# -----------------------------
# Update Contact
# -----------------------------
def update_contact():
    selected = tree.focus()

    if not selected:
        messagebox.showwarning("Warning", "Select a contact.")
        return

    index = tree.index(selected)

    contacts[index] = {
        "name": name_var.get(),
        "phone": phone_var.get(),
        "email": email_var.get()
    }

    save_contacts()
    refresh_table()
    clear_fields()

# -----------------------------
# Delete Contact
# -----------------------------
def delete_contact():
    selected = tree.focus()

    if not selected:
        messagebox.showwarning("Warning", "Select a contact.")
        return

    index = tree.index(selected)

    del contacts[index]

    save_contacts()
    refresh_table()
    clear_fields()

# -----------------------------
# Search Contact
# -----------------------------
def search_contact():
    keyword = search_var.get().lower()

    result = []

    for contact in contacts:
        if keyword in contact["name"].lower():
            result.append(contact)

    refresh_table(result)

# -----------------------------
# Clear Fields
# -----------------------------
def clear_fields():
    name_var.set("")
    phone_var.set("")
    email_var.set("")
    search_var.set("")
    refresh_table()

# -----------------------------
# GUI
# -----------------------------
root = tk.Tk()
root.title("Contact Management System")
root.geometry("700x500")
root.resizable(False, False)

title = tk.Label(root,
                 text="CONTACT MANAGEMENT SYSTEM",
                 font=("Arial", 18, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
search_var = tk.StringVar()

tk.Label(frame, text="Name").grid(row=0, column=0, padx=10, pady=5)
tk.Entry(frame, textvariable=name_var, width=30).grid(row=0, column=1)

tk.Label(frame, text="Phone").grid(row=1, column=0, padx=10, pady=5)
tk.Entry(frame, textvariable=phone_var, width=30).grid(row=1, column=1)

tk.Label(frame, text="Email").grid(row=2, column=0, padx=10, pady=5)
tk.Entry(frame, textvariable=email_var, width=30).grid(row=2, column=1)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add", width=12, command=add_contact).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update", width=12, command=update_contact).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete", width=12, command=delete_contact).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Clear", width=12, command=clear_fields).grid(row=0, column=3, padx=5)

search_frame = tk.Frame(root)
search_frame.pack()

tk.Label(search_frame, text="Search Name").grid(row=0, column=0)

tk.Entry(search_frame,
         textvariable=search_var,
         width=25).grid(row=0, column=1)

tk.Button(search_frame,
          text="Search",
          command=search_contact).grid(row=0, column=2, padx=10)

tree = ttk.Treeview(root,
                    columns=("Name", "Phone", "Email"),
                    show="headings",
                    height=10)

tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")

tree.column("Name", width=180)
tree.column("Phone", width=150)
tree.column("Email", width=300)

tree.pack(pady=20)

tree.bind("<<TreeviewSelect>>", select_contact)

refresh_table()

root.mainloop()