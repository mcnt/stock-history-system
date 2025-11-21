from pathlib import Path
import sqlite3
import shutil
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = DATA_DIR / 'sample_data.db'
SCHEMA_FILE = PROJECT_ROOT / 'src' / 'db' / 'schema.sql'

def is_sqlite_file(path: Path) -> bool:
    try:
        with path.open('rb') as f:
            return f.read(16).startswith(b"SQLite format 3")
    except Exception:
        return False

def initialize_database():
    if DB_FILE.exists() and not is_sqlite_file(DB_FILE):
        backup = DB_FILE.with_suffix(DB_FILE.suffix + '.corrupt.bak')
        shutil.move(str(DB_FILE), str(backup))
        print(f'Backed up invalid DB to: {backup}')

    conn = sqlite3.connect(str(DB_FILE))
    try:
        if SCHEMA_FILE.exists():
            sql = SCHEMA_FILE.read_text(encoding='utf-8')
            conn.executescript(sql)
            conn.commit()
            print(f'Schema applied to {DB_FILE}')
        else:
            print('schema.sql not found at', SCHEMA_FILE)
            sys.exit(1)
    finally:
        conn.close()

if __name__ == '__main__':
    try:
        initialize_database()
    except Exception as e:
        print('Error initializing DB:', e, file=sys.stderr)
        sys.exit(1)