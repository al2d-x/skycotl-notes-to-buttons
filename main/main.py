from loader import load_active_map
from mapper import map_active_map
from exporter import export_html_stack
from pathlib import Path

def main():
    raw_mapping = load_active_map()

    # for table_idx, value in raw_mapping.items(): print(f"Table {table_idx}: {value}")

    labeled_mapping = map_active_map(raw_mapping)

    # for table_idx, value in labeled_mapping.items(): print(f"Table {table_idx}: {value}")

    # Export HTML with stacked icons (responsive grid)
    out_path = export_html_stack(labeled_mapping)  # writes to ../export/export.html by default
    print(f"Exported to: {out_path}")

if __name__ == "__main__":
    main()
