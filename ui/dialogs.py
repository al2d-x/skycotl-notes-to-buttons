#ui/dialogs.py
"""
UI helpers (dialogs)
====================
Small reusable Tk dialog helpers used by the main application.

Exports:
- show_text_dialog(parent, title, body): read-only text modal with scrollbar
- center_on_parent(win, parent): centers a Toplevel over its parent
"""

import tkinter as tk
from tkinter import ttk

def center_on_parent(win: tk.Toplevel, parent: tk.Tk) -> None:
    win.update_idletasks()
    x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (win.winfo_width() // 2)
    y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (win.winfo_height() // 2)
    win.geometry(f"+{x}+{y}")

def show_text_dialog(parent: tk.Tk, title: str, body: str) -> None:
    win = tk.Toplevel(parent)
    win.title(title)
    win.transient(parent)
    win.grab_set()
    win.minsize(520, 360)

    frm = ttk.Frame(win, padding=10)
    frm.pack(fill="both", expand=True)

    txt = tk.Text(frm, wrap="word", height=20, undo=False)
    yscroll = ttk.Scrollbar(frm, orient="vertical", command=txt.yview)
    txt.configure(yscrollcommand=yscroll.set)
    txt.insert("1.0", body or "(no content)")
    txt.configure(state="disabled")
    txt.grid(row=0, column=0, sticky="nsew")
    yscroll.grid(row=0, column=1, sticky="ns")

    ttk.Button(frm, text="Close", command=win.destroy).grid(row=1, column=0, sticky="e", pady=(8, 0))
    frm.columnconfigure(0, weight=1); frm.rowconfigure(0, weight=1)
    center_on_parent(win, parent)
