# main/__main__.py
"""
CLI launcher
============
Entrypoint for `python -m main`. Wires up services and starts the Tk GUI.
"""
from main.app import App
from services.conversion import ConversionService
from docs.service import DocsService

from main.loader import load_active_map
from main.mapper import map_active_map
from main.exporter import export_html_stack

from main import __version__ as APP_VERSION

if __name__ == "__main__":
    print(f"Launching Sky: Notes → Buttons v{APP_VERSION} ...")
    App(
        conversion=ConversionService(load_active_map, map_active_map, export_html_stack),
        docs=DocsService(),
    ).mainloop()
