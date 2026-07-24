import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import os
import sys
import webbrowser

from game_detector import detect_games
from installer import install_radio_pack
from restore import restore_backup
from update_checker import check_update


# ==========================
# App Configuration
# ==========================

APP_NAME = "Persian Radio Manager"
APP_VERSION = "v1.0.0"
DEVELOPER = "Yoosef"
TELEGRAM_CHANNEL = "@Persian_Radio_Pack"
TELEGRAM_CHANNEL_URL = "https://t.me/Persian_Radio_Pack"
GITHUB = "https://github.com/yoosefzeynali-ship-it/Persian-Radio-Pack"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ==========================
# Resource Path Helper
# (works both in dev and when frozen with PyInstaller)
# ==========================

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# ==========================
# Detect Games
# ==========================

games = detect_games()


# ==========================
# Helper Functions
# ==========================

def set_status(text):
    status.configure(text=text)


def build_status_text(installed="Unknown", latest="Unknown", state="Ready"):
    return f"""
📻 Persian Radio Pack

Euro Truck Simulator 2
{"Found ✅" if games["ETS2"] else "Not Found ❌"}

American Truck Simulator
{"Found ✅" if games["ATS"] else "Not Found ❌"}

Installed Version
{installed}

Latest Version
{latest}

Status
{state}
"""


# ==========================
# Install
# ==========================

def install_process():
    ets2 = bool(ets2_checkbox.get())
    ats = bool(ats_checkbox.get())

    if not ets2 and not ats:
        app.after(0, lambda: messagebox.showwarning(
            "Select Game", "Please select at least one game."
        ))
        return

    app.after(0, lambda: install_button.configure(state="disabled"))
    app.after(0, lambda: set_status(build_status_text(state="Installing...")))

    try:
        result = install_radio_pack(install_ets2=ets2, install_ats=ats)
    except Exception as e:
        result = False
        print(f"Install Error: {e}")

    if result:
        app.after(0, lambda: set_status(build_status_text(state="Installed Successfully ✅")))
        app.after(0, lambda: messagebox.showinfo(
            "Completed", "Radio Pack installed successfully."
        ))
    else:
        app.after(0, lambda: set_status(build_status_text(state="Installation Failed ❌")))
        app.after(0, lambda: messagebox.showerror("Error", "Installation failed."))

    app.after(0, lambda: install_button.configure(state="normal"))


def install_radio():
    threading.Thread(target=install_process, daemon=True).start()


# ==========================
# Restore
# ==========================

def restore_process():
    ets2 = bool(ets2_checkbox.get())
    ats = bool(ats_checkbox.get())

    if not ets2 and not ats:
        app.after(0, lambda: messagebox.showwarning(
            "Select Game", "Please select at least one game."
        ))
        return

    app.after(0, lambda: restore_button.configure(state="disabled"))
    app.after(0, lambda: set_status(build_status_text(state="Restoring Backup...")))

    try:
        result = restore_backup(restore_ets2=ets2, restore_ats=ats)
    except Exception as e:
        result = False
        print(f"Restore Error: {e}")

    if result:
        app.after(0, lambda: set_status(build_status_text(state="Backup Restored ✅")))
        app.after(0, lambda: messagebox.showinfo(
            "Restore", "Backup restored successfully."
        ))
    else:
        app.after(0, lambda: set_status(build_status_text(state="Restore Failed ❌")))
        app.after(0, lambda: messagebox.showerror("Restore", "Restore failed."))

    app.after(0, lambda: restore_button.configure(state="normal"))


def restore_radio():
    threading.Thread(target=restore_process, daemon=True).start()


# ==========================
# Update Checker
# ==========================

def update_process():
    try:
        data = check_update()
    except Exception as e:
        data = {"error": str(e)}

    if "error" in data:
        app.after(0, lambda: messagebox.showerror("GitHub", data["error"]))
        return

    installed = data["installed"] if data["installed"] is not None else "Not Installed"
    latest = data["latest"]
    state = "Update Available ⬆" if data["update_available"] else "Up To Date ✅"

    app.after(0, lambda: set_status(build_status_text(installed, latest, state)))
    app.after(0, lambda: messagebox.showinfo(
        "Check Update",
        f"""
Installed Version

{installed}

Latest Version

{latest}

Status

{state}
"""
    ))


def update_radio():
    threading.Thread(target=update_process, daemon=True).start()


# ==========================
# Backup
# ==========================

def backup_radio():
    messagebox.showinfo(
        "Backup",
        "Backup is created automatically before every installation."
    )


# ==========================
# Links / About
# ==========================

def open_github():
    webbrowser.open(GITHUB)


def open_telegram():
    webbrowser.open(TELEGRAM_CHANNEL_URL)


def show_about():
    messagebox.showinfo(
        "About Persian Radio Manager",
        f"""
Persian Radio Manager
Version {APP_VERSION}

Developer:
{DEVELOPER}

Telegram:
{TELEGRAM_CHANNEL}

GitHub:
yoosefzeynali-ship-it

Supports:
• Euro Truck Simulator 2
• American Truck Simulator

© 2026 Yoosef Zeynali
All Rights Reserved.
"""
    )


# ==========================
# Main Window
# ==========================

app = ctk.CTk()
app.title(APP_NAME)
app.geometry("520x620")
app.resizable(False, False)

try:
    logo = tk.PhotoImage(file=resource_path("assets/logo.png"))
    app.iconphoto(True, logo)
except Exception as e:
    print(f"Icon Error: {e}")


# ==========================
# Scrollable Container
# ==========================

container = ctk.CTkScrollableFrame(app, width=480, height=580)
container.pack(padx=15, pady=15, fill="both", expand=True)


# ==========================
# Header
# ==========================

ctk.CTkLabel(
    container,
    text="🎙 Persian Radio Manager",
    font=("Arial", 26, "bold")
).pack(pady=(20, 5))

ctk.CTkLabel(
    container,
    text=f"Version {APP_VERSION}",
    font=("Arial", 14)
).pack()


# ==========================
# Status Box
# ==========================

status_frame = ctk.CTkFrame(container)
status_frame.pack(fill="x", padx=20, pady=20)

status = ctk.CTkLabel(
    status_frame,
    text=build_status_text(),
    justify="left",
    font=("Arial", 14)
)
status.pack(padx=20, pady=20)


# ==========================
# Game Selection
# ==========================

ctk.CTkLabel(
    container,
    text="Select Games",
    font=("Arial", 18, "bold")
).pack(pady=(10, 5))

ets2_checkbox = ctk.CTkCheckBox(container, text="Euro Truck Simulator 2")
ets2_checkbox.pack(pady=5)

ats_checkbox = ctk.CTkCheckBox(container, text="American Truck Simulator")
ats_checkbox.pack(pady=5)

if games["ETS2"]:
    ets2_checkbox.select()
else:
    ets2_checkbox.configure(state="disabled")

if games["ATS"]:
    ats_checkbox.select()
else:
    ats_checkbox.configure(state="disabled")


# ==========================
# Actions
# ==========================

ctk.CTkLabel(
    container,
    text="Actions",
    font=("Arial", 18, "bold")
).pack(pady=15)

install_button = ctk.CTkButton(
    container, text="📥 Install Radio Pack", width=300, height=42,
    command=install_radio
)
install_button.pack(pady=8)

ctk.CTkButton(
    container, text="🔄 Check for Update", width=300, height=42,
    command=update_radio
).pack(pady=8)

ctk.CTkButton(
    container, text="💾 Backup", width=300, height=42,
    command=backup_radio
).pack(pady=8)

restore_button = ctk.CTkButton(
    container, text="♻ Restore Backup", width=300, height=42,
    command=restore_radio
)
restore_button.pack(pady=8)

ctk.CTkButton(
    container, text="💬 Telegram", width=300, height=42,
    command=open_telegram
).pack(pady=8)

ctk.CTkButton(
    container, text="🌐 GitHub", width=300, height=42,
    command=open_github
).pack(pady=8)

ctk.CTkButton(
    container, text="ℹ About", width=300, height=42,
    command=show_about
).pack(pady=8)


# ==========================
# Footer
# ==========================

ctk.CTkLabel(
    container, text=f"Developed by {DEVELOPER}", font=("Arial", 13)
).pack(pady=(25, 25))


# ==========================
# Load Version Info On Startup (non-blocking)
# ==========================

def load_version_on_start():
    try:
        data = check_update()
        if "error" not in data:
            installed = data["installed"] if data["installed"] is not None else "Not Installed"
            latest = data["latest"]
            state = "Update Available ⬆" if data["update_available"] else "Up To Date ✅"
            app.after(0, lambda: set_status(build_status_text(installed, latest, state)))
    except Exception as e:
        print(f"Update Check Error: {e}")


threading.Thread(target=load_version_on_start, daemon=True).start()


# ==========================
# Run
# ==========================

app.mainloop()