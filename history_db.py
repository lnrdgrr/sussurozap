import os
import sqlite3
from datetime import datetime

import paths

_DATA_DIR = os.path.join(paths.base_dir(), "data")
_DB_PATH = os.path.join(_DATA_DIR, "history.db")


def _get_conn():
    os.makedirs(_DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transcriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                transcript_text TEXT NOT NULL,
                created_at TEXT NOT NULL,
                duration_sec REAL,
                model_used TEXT
            )
            """
        )


def save_transcription(filename, filepath, transcript_text, duration_sec, model_used):
    created_at = datetime.now().isoformat(timespec="seconds")
    with _get_conn() as conn:
        cursor = conn.execute(
            """
            INSERT INTO transcriptions
                (filename, filepath, transcript_text, created_at, duration_sec, model_used)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (filename, filepath, transcript_text, created_at, duration_sec, model_used),
        )
        return cursor.lastrowid


def get_history_grouped_by_day():
    """Returns a list of {date, items[]} ordered from most recent day to oldest,
    and items within each day ordered most recent first."""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM transcriptions ORDER BY created_at DESC"
        ).fetchall()

    groups = []
    groups_by_date = {}
    for row in rows:
        date_key = row["created_at"][:10]
        if date_key not in groups_by_date:
            group = {"date": date_key, "items": []}
            groups_by_date[date_key] = group
            groups.append(group)
        groups_by_date[date_key]["items"].append(
            {
                "id": row["id"],
                "filename": row["filename"],
                "transcript_text": row["transcript_text"],
                "created_at": row["created_at"],
                "duration_sec": row["duration_sec"],
                "model_used": row["model_used"],
            }
        )
    return groups
