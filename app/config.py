from pathlib import Path
import os


def find_project_root(marker=".git"):
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / marker).exists():
            return parent
    return current.parent


log_file_path = Path(os.path.expanduser("~")) / ".seventeenlands" / "fake_seventeenlands.log"

project_root = find_project_root()
db_path = project_root / "database.db"
schema_path = project_root / "schema.sql"
template_path = project_root / "app/templates"