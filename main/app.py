# app.py
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import webbrowser

from loader import load_active_map
from mapper import map_active_map
from exporter import export_html_stack

APP_TITLE = "Sky: Notes → Buttons"

# Check availability of ttkbootstrap at module load (don't call Style yet)
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
        self.minsize(520, 220)

        # --- If ttkbootstrap is available, instantiate Style() AFTER root exists.
        if USING_BOOTSTRAP:
            # create the theme now — doing this after root creation avoids an extra hidden window
            try:
                Style(theme="darkly")  # choose theme; no master argument
            except Exception:
                # fallback to builtin styling if Style() fails for any reason
                self._apply_fallback_style()
        else:
            self._apply_fallback_style()
        # ------------------------------------------------

        # Vars
        self.in_path = tk.StringVar()
        self.out_path = tk.StringVar()

        # Menu
        self._build_menu()

        # Content
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

        # Start
        self.start_btn = ttk.Button(frm, text="Start", command=self.run_convert)
        self.start_btn.grid(row=2, column=1, sticky="e", **pad)

        # Status
        self.status = ttk.Label(frm, text="Ready.", foreground="#5a6")
        self.status.grid(row=3, column=0, columnspan=3, sticky="w", **pad)

        frm.columnconfigure(1, weight=1)

    def _apply_fallback_style(self):
        """Apply a simple dark fallback theme using builtin ttk (no extra deps)."""
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
        style.configure("TButton", padding=6)

    def _build_menu(self):
        m = tk.Menu(self)
        filem = tk.Menu(m, tearoff=0)
        filem.add_command(label="Open Input…", command=self.pick_input)
        filem.add_command(label="Set Export…", command=self.pick_output)
        filem.add_separator()
        filem.add_command(label="Exit", command=self.quit)
        m.add_cascade(label="File", menu=filem)

        helpm = tk.Menu(m, tearoff=0)
        helpm.add_command(label="About", command=lambda: messagebox.showinfo(
            "About",
            f"{APP_TITLE}\n"
            "Converts Sky: Children of the Light (saved HTML sheets from https://sky-music.github.io/) into controller button charts.\n"
            "Fan tool — not affiliated with the game developer, info, tips and help found under the README.\n"
            "https://github.com/al2d-x"
        ))
        m.add_cascade(label="Help", menu=helpm)
        self.config(menu=m)

    def pick_input(self):
        path = filedialog.askopenfilename(
            title="Select input HTML",
            filetypes=[("HTML files", "*.html;*.htm"), ("All files", "*.*")]
        )
        if path:
            self.in_path.set(path)
            # Default export path next to input
            default_out = Path(path).with_suffix(".export.html")
            if not self.out_path.get():
                self.out_path.set(str(default_out))

    def pick_output(self):
        path = filedialog.asksaveasfilename(
            title="Save export as",
            defaultextension=".html",
            filetypes=[("HTML", "*.html")]
        )
        if path:
            self.out_path.set(path)

    def run_convert(self):
        in_file = self.in_path.get().strip()
        out_file = self.out_path.get().strip()

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

            # for i, v in raw.items(): print(f"Table {i}: {v}")  # debug

            mapped = map_active_map(raw)

            # for i, v in mapped.items(): print(f"Table {i}: {v}")  # debug

            self.status.config(text="Exporting…")
            out_path = export_html_stack(mapped, out_file, title="Sky: Notes to Buttons")
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
