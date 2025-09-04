# main.py
from loader import load_active_map
from mapper import map_active_map
from exporter import export_html_stack
from pathlib import Path

def main():
    raw_mapping = load_active_map()

    # TODO delete later: numeric map
    for table_idx, value in raw_mapping.items():
        if value == "noValue":
            print(f"Table {table_idx}: noValue")
        else:
            print(f"Table {table_idx}: {', '.join(map(str, value))}")

    labeled_mapping = map_active_map(raw_mapping)

    # TODO delete later: labeled map
    for table_idx, value in labeled_mapping.items():
        if value == "noValue":
            print(f"Table {table_idx}: noValue")
        else:
            print(f"Table {table_idx}: {', '.join(value)}")

    # Export HTML with stacked icons (responsive grid)
    out_path = export_html_stack(labeled_mapping)  # writes to ../export/export.html by default
    print(f"//TODO delete later -> Exported to: {out_path}")

if __name__ == "__main__":
    main()
