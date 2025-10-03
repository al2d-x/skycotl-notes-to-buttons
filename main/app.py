# app.py
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import webbrowser

from loader import load_active_map
from mapper import map_active_map
from exporter import export_html_stack
from profiles import PROFILES  # required

APP_TITLE = "Sky: Notes → Buttons"

# ttkbootstrap (optional)
try:
    from ttkbootstrap import ttk, Style   # pip install ttkbootstrap
    USING_BOOTSTRAP = True
except Exception:
    from tkinter import ttk
    Style = None
    USING_BOOTSTRAP = False


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.minsize(520, 260)

        if USING_BOOTSTRAP:
            try:
                Style(theme="darkly")
            except Exception:
                self._apply_fallback_style()
        else:
            self._apply_fallback_style()

        # Vars
        self.in_path = tk.StringVar()
        self.out_path = tk.StringVar()
        self.profile_var = tk.StringVar(value=list(PROFILES.keys())[0])

        # Track whether out_path is auto-derived (so we can safely update it)
        self._out_is_auto = True

        # Menu
        self._build_menu()

        pad = {"padx": 10, "pady": 8}
        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, **pad)

        # Input row
        ttk.Label(frm, text="Input HTML:").grid(row=0, column=0, sticky="w")
        in_entry = ttk.Entry(frm, textvariable=self.in_path, width=50)
        in_entry.grid(row=0, column=1, sticky="ew", **pad)
        ttk.Button(frm, text="Browse…", command=self.pick_input).grid(row=0, column=2)

        # Output row
        ttk.Label(frm, text="Export to:").grid(row=1, column=0, sticky="w")
        out_entry = ttk.Entry(frm, textvariable=self.out_path, width=50)
        out_entry.grid(row=1, column=1, sticky="ew", **pad)
        ttk.Button(frm, text="Browse…", command=self.pick_output).grid(row=1, column=2)

        # If user types manually, stop auto-updating the output path
        out_entry.bind("<KeyRelease>", lambda e: setattr(self, "_out_is_auto", False))

        # Profile row
        ttk.Label(frm, text="Button profile:").grid(row=2, column=0, sticky="w")
        self.prof_box = ttk.Combobox(
            frm,
            textvariable=self.profile_var,
            values=list(PROFILES.keys()),
            state="readonly",
            width=20,
        )
        self.prof_box.grid(row=2, column=1, sticky="w", **pad)
        self.prof_box.bind("<<ComboboxSelected>>", self._on_profile_change)

        # Start
        self.start_btn = ttk.Button(frm, text="Start", command=self.run_convert)
        self.start_btn.grid(row=3, column=1, sticky="e", **pad)

        # Status
        self.status = ttk.Label(frm, text="Ready.", foreground="#5a6")
        self.status.grid(row=4, column=0, columnspan=3, sticky="w", **pad)

        frm.columnconfigure(1, weight=1)

    # ---------- helpers ----------
    def _make_default_out(self, in_path: str, profile: str) -> str:
        """
        Build default export filename next to the input:
        <stem>_<profile>_buttons.html
        """
        p = Path(in_path)
        stem = p.stem  # original name without extension
        safe_profile = (profile or "xbox").strip()
        out_name = f"{stem}_{safe_profile}_buttons.html"
        return str(p.with_name(out_name))

    # ---------- UI plumbing ----------
    def _apply_fallback_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        ROOT_BG = "#121315"
        PANEL_BG = "#151719"
        FG = "#dfe3e6"
        self.configure(bg=ROOT_BG)
        style.configure(".", background=ROOT_BG, foreground=FG)
        style.configure("TFrame", background=ROOT_BG)
        style.configure("TLabel", background=ROOT_BG, foreground=FG)
        style.configure("TEntry", fieldbackground=PANEL_BG, foreground=FG)
        style.configure("TCombobox", fieldbackground=PANEL_BG, foreground=FG)
        style.configure("TButton", padding=6)

    def _build_menu(self):
        m = tk.Menu(self)
        filem = tk.Menu(m, tearoff=0)
        filem.add_command(label="Open Input…", command=self.pick_input)
        filem.add_command(label="Set Export…", command=self.pick_output)
        filem.add_separator()
        filem.add_command(label="Exit", command=self.quit)
        m.add_cascade(label="File", menu=filem)

        def _about():
            profiles_list = ", ".join(PROFILES.keys())
            messagebox.showinfo(
                "About",
                f"{APP_TITLE}\n"
                "Converts Sky: Children of the Light (saved HTML sheets from https://sky-music.github.io/) "
                "into controller/keyboard button charts.\n"
                "Fan tool — not affiliated with the game developer.\n"
                f"Profiles: {profiles_list}\n"
                "https://github.com/al2d-x"
            )

        helpm = tk.Menu(m, tearoff=0)
        helpm.add_command(label="About", command=_about)
        m.add_cascade(label="Help", menu=helpm)
        self.config(menu=m)

    def _on_profile_change(self, _evt=None):
        """When profile changes, update out path only if it's still auto."""
        in_file = self.in_path.get().strip()
        if self._out_is_auto and in_file:
            self.out_path.set(self._make_default_out(in_file, self.profile_var.get()))

    # ---------- actions ----------
    def pick_input(self):
        path = filedialog.askopenfilename(
            title="Select input HTML",
            filetypes=[("HTML files", "*.html;*.htm"), ("All files", "*.*")]
        )
        if path:
            self.in_path.set(path)
            # Update default export name to "<stem>_<profile>_buttons.html"
            if self._out_is_auto or not self.out_path.get().strip():
                self.out_path.set(self._make_default_out(path, self.profile_var.get()))
                self._out_is_auto = True  # keep auto mode

    def pick_output(self):
        path = filedialog.asksaveasfilename(
            title="Save export as",
            defaultextension=".html",
            filetypes=[("HTML", "*.html")]
        )
        if path:
            self.out_path.set(path)
            self._out_is_auto = False  # user chose a manual path

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
            self.status.config(text="Parsing…")
            raw = load_active_map(in_file)

            self.status.config(text="Mapping…")
            mapped = map_active_map(raw, profile=profile)

            self.status.config(text="Exporting…")
            out_path = export_html_stack(
                mapped, out_file, title="Sky: Notes to Buttons", profile=profile
            )

            self.status.config(text=f"Done → {out_path}")
            if messagebox.askyesno("Open export?", "Export complete. Open in browser?"):
                webbrowser.open(Path(out_path).resolve().as_uri())
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Failed.")
        finally:
            self.start_btn.config(state="normal")


if __name__ == "__main__":
    App().mainloop()
