#main/app.py
"""
GUI application (Tk)
====================
Top-level Tkinter window and UI wiring:
- File picking and export path derivation
- Profile selection and validation display
- Help/About/Version menu items (no auto-update checks)
- Delegates conversion to ConversionService (loader → mapper → exporter)
"""

import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import webbrowser, sys

# services
from services.conversion import ConversionService
from docs.service import DocsService
from ui.dialogs import show_text_dialog

# profiles
from profiles import PROFILES, get_profile_report, refresh_profiles, ASSETS_DIR

APP_TITLE   = "Sky: Notes → Buttons"
APP_VERSION = "2.0.0"

# Point this at your repo (or releases page directly)
GITHUB_REPO_URL     = "https://github.com/<you>/skycotl-notes-to-buttons"
GITHUB_RELEASES_URL = f"{GITHUB_REPO_URL}/releases"

# ttkbootstrap (optional)
try:
    from ttkbootstrap import ttk, Style
    USING_BOOTSTRAP = True
except Exception:
    from tkinter import ttk
    Style = None
    USING_BOOTSTRAP = False

APP_TITLE   = "Sky: Notes → Buttons"
APP_VERSION = "2.0.0"

class App(tk.Tk):
    def __init__(self, conversion: ConversionService, docs: DocsService):
        super().__init__()
        self.conversion = conversion
        self.docs = docs

        self.title(APP_TITLE)
        self.minsize(560, 280)

        # icon
        try:
            base = Path(__file__).resolve().parents[1]
            ico = base / "assets" / "scotl_minimalist.ico"
            png = base / "assets" / "scotl_minimalist.png"
            if ico.exists():
                self.iconbitmap(str(ico.resolve()))
            elif png.exists():
                self._icon_img = tk.PhotoImage(file=str(png.resolve()))
                self.iconphoto(True, self._icon_img)
        except Exception as e:
            logging.info("Icon not set: %s", e)

        if USING_BOOTSTRAP:
            try:
                Style(theme="darkly")
            except Exception as e:
                logging.info("ttkbootstrap failed; fallback: %s", e)
                self._apply_fallback_style()
        else:
            self._apply_fallback_style()

        # Vars
        self.in_path = tk.StringVar()
        self.out_path = tk.StringVar()
        self.profile_var = tk.StringVar(value=(sorted(PROFILES.keys())[0] if PROFILES else ""))
        self._out_is_auto = True

        self._build_menu()

        pad = {"padx": 10, "pady": 8}
        frm = ttk.Frame(self); frm.pack(fill="both", expand=True, **pad)

        ttk.Label(frm, text="Input HTML:").grid(row=0, column=0, sticky="w")
        in_entry = ttk.Entry(frm, textvariable=self.in_path, width=50)
        in_entry.grid(row=0, column=1, sticky="ew", **pad)
        ttk.Button(frm, text="Browse…", command=self.pick_input).grid(row=0, column=2)

        ttk.Label(frm, text="Export to:").grid(row=1, column=0, sticky="w")
        out_entry = ttk.Entry(frm, textvariable=self.out_path, width=50)
        out_entry.grid(row=1, column=1, sticky="ew", **pad)
        ttk.Button(frm, text="Browse…", command=self.pick_output).grid(row=1, column=2)
        out_entry.bind("<KeyRelease>", lambda e: setattr(self, "_out_is_auto", False))

        ttk.Label(frm, text="Button profile:").grid(row=2, column=0, sticky="w")
        self.prof_box = ttk.Combobox(
            frm, textvariable=self.profile_var, values=sorted(PROFILES.keys()), state="readonly", width=28
        )
        self.prof_box.grid(row=2, column=1, sticky="w", **pad)
        self.prof_box.bind("<<ComboboxSelected>>", self._on_profile_change)

        self.prof_warn = ttk.Label(frm, text="", foreground="#f46666", wraplength=460)
        self.prof_warn.grid(row=3, column=1, columnspan=2, sticky="w", padx=10, pady=(0, 4))

        self.start_btn = ttk.Button(frm, text="Start", command=self.run_convert)
        self.start_btn.grid(row=4, column=1, sticky="e", **pad)

        self.status = ttk.Label(frm, text="Ready.", foreground="#5a6")
        self.status.grid(row=5, column=0, columnspan=3, sticky="w", **pad)
        frm.columnconfigure(1, weight=1)

        self._update_profile_warning()

    # ------- styles
    def _apply_fallback_style(self):
        style = ttk.Style(self)
        try: style.theme_use("clam")
        except Exception: pass
        ROOT_BG = "#121315"; PANEL_BG = "#151719"; FG = "#dfe3e6"
        self.configure(bg=ROOT_BG)
        style.configure(".", background=ROOT_BG, foreground=FG)
        style.configure("TFrame", background=ROOT_BG)
        style.configure("TLabel", background=ROOT_BG, foreground=FG)
        style.configure("TEntry", fieldbackground=PANEL_BG, foreground=FG)
        style.configure("TCombobox", fieldbackground=PANEL_BG, foreground=FG)
        style.configure("TButton", padding=6)

    # ------- menu
    def _build_menu(self):
        m = tk.Menu(self)

        filem = tk.Menu(m, tearoff=0)
        filem.add_command(label="Open Input…", command=self.pick_input, accelerator="Ctrl+O")
        filem.add_command(label="Set Export…", command=self.pick_output, accelerator="Ctrl+Shift+S")
        filem.add_separator()
        filem.add_command(label="Exit", command=self.quit, accelerator="Ctrl+Q")
        m.add_cascade(label="File", menu=filem)

        self.bind_all("<Control-o>", lambda e: self.pick_input())
        self.bind_all("<Control-Shift-s>", lambda e: self.pick_output())
        self.bind_all("<Control-q>", lambda e: self.quit())

        helpm = tk.Menu(m, tearoff=0)

        def _about(_evt=None):
            body = self.docs.read_text("about.txt") or "(Missing file: docs/about.txt)"
            show_text_dialog(self, f"About — v{APP_VERSION}", body)

        def _profiles_help():
            body = self.docs.read_text("help_profiles.txt") or "(Missing file: docs/help_profiles.txt)"
            show_text_dialog(self, "Profile naming (1–15)", body)

        def _add_profile_help():
            body = self.docs.read_text("help_add_profile.txt") or "(Missing file: docs/help_add_profile.txt)"
            show_text_dialog(self, "How to add a profile", body)

        licenses_menu = tk.Menu(helpm, tearoff=0)
        lic_files = self.docs.list_license_files()
        if lic_files:
            for p in lic_files:
                title = p.stem.replace("_", " ").title()
                licenses_menu.add_command(
                    label=title,
                    command=lambda path=p: show_text_dialog(
                        self, f"License — {path.stem}", path.read_text(encoding="utf-8", errors="ignore")
                    ),
                )
        else:
            licenses_menu.add_command(label="(no license files found)", state="disabled")

        helpm.add_command(label="Profile naming (1–15)", command=_profiles_help)
        helpm.add_command(label="How to add a profile", command=_add_profile_help)
        helpm.add_command(label="Open profiles folder", command=self._open_profiles_folder)
        helpm.add_command(label="Validate selected profile", command=self._show_profile_validation)
        helpm.add_command(label="Reload profiles", command=self._refresh_profiles, accelerator="F5")
        helpm.add_cascade(label="Licenses", menu=licenses_menu)
        helpm.add_separator()
        helpm.add_command(label="About", command=_about, accelerator="F1")
        helpm.add_command(label=f"Version… (v{APP_VERSION})", command=self._show_version)


        self.bind_all("<F5>", self._refresh_profiles)
        self.bind_all("<F1>", _about)

        m.add_cascade(label="Help", menu=helpm)
        self.config(menu=m)

    # ------- helpers
    def _open_profiles_folder(self):
        path = ASSETS_DIR
        try:
            if sys.platform.startswith("win"):
                import os; os.startfile(path)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                import os; os.system(f'open "{path}"')
            else:
                import os; os.system(f'xdg-open "{path}"')
        except Exception:
            messagebox.showinfo("Profiles folder", str(path))

    def _show_profile_validation(self):
        key = (self.profile_var.get() or "").strip()
        rep = get_profile_report(key)
        message = "OK: profile has 1.png–15.png and no out-of-range files." if rep.valid else ("\n".join(rep.problems) or "Invalid profile.")
        show_text_dialog(self, f"Profile validation — {key}", message)

    def _refresh_profiles(self, _evt=None):
        new_profiles = refresh_profiles()
        values = sorted(new_profiles.keys())
        self.prof_box["values"] = values
        if self.profile_var.get() not in values:
            self.profile_var.set(values[0] if values else "")
        self._update_profile_warning()

    def _on_profile_change(self, _evt=None):
        in_file = self.in_path.get().strip()
        if self._out_is_auto and in_file:
            stem = Path(in_file).stem
            prof = (self.profile_var.get() or "xbox").strip()
            self.out_path.set(str(Path(in_file).with_name(f"{stem}_{prof}_buttons.html")))
        self._update_profile_warning()

    def _update_profile_warning(self):
        key = (self.profile_var.get() or "").strip()
        rep = get_profile_report(key)
        tip = " ".join(rep.problems) if rep.problems else ""
        # hover tooltip kept in your original code — omit here for brevity; keep your existing implementation if you want
        if rep.valid:
            self.prof_warn.config(text="")
            self.start_btn.config(state="normal")
        else:
            self.prof_warn.config(text="⚠ Invalid profile. Hover for details.")
            self.start_btn.config(state="disabled")

            

    def _show_version(self):
        """Show current version and let user open the GitHub releases page."""
        from ui.dialogs import show_text_dialog
        body = (
            f"{APP_TITLE}\n\n"
            f"Current version: v{APP_VERSION}\n\n"
            "This app does not auto-check for updates.\n"
            "Click the button below (or copy the URL) to check releases on GitHub:\n\n"
            f"{GITHUB_RELEASES_URL}\n"
        )
        # Use the existing read-only text dialog (no hyperlinks), then ask to open.
        show_text_dialog(self, "Version / Updates", body)
        import webbrowser, tkinter.messagebox as mbox
        if mbox.askyesno("Open GitHub?", "Open the GitHub Releases page in your browser?"):
            webbrowser.open(GITHUB_RELEASES_URL)

    # ------- IO actions
    def pick_input(self):
        path = filedialog.askopenfilename(title="Select input HTML", filetypes=[("HTML files", "*.html;*.htm"), ("All files", "*.*")])
        if path:
            self.in_path.set(path)
            if self._out_is_auto or not self.out_path.get().strip():
                stem = Path(path).stem
                prof = (self.profile_var.get() or "xbox").strip()
                self.out_path.set(str(Path(path).with_name(f"{stem}_{prof}_buttons.html")))
                self._out_is_auto = True

    def pick_output(self):
        path = filedialog.asksaveasfilename(title="Save export as", defaultextension=".html", filetypes=[("HTML", "*.html")])
        if path:
            self.out_path.set(path)
            self._out_is_auto = False

    def run_convert(self):
        in_file = self.in_path.get().strip()
        out_file = self.out_path.get().strip()
        profile = (self.profile_var.get() or "xbox").strip()

        if not in_file:
            messagebox.showwarning("Missing input", "Please choose an input HTML file.")
            return
        if not out_file:
            messagebox.showwarning("Missing export path", "Please choose where to save the export.")
            return

        try:
            self.start_btn.config(state="disabled")
            self.status.config(text="Working…")
            out_path = self.conversion.convert(in_file, out_file, title="Sky: Notes to Buttons", profile=profile)
            self.status.config(text=f"Done → {out_path}")
            if messagebox.askyesno("Open export?", "Export complete. Open in browser?"):
                webbrowser.open(Path(out_path).resolve().as_uri())
        except Exception as e:
            logging.exception("Conversion failed")
            messagebox.showerror("Error", str(e))
            self.status.config(text="Failed.")
        finally:
            self._update_profile_warning()
