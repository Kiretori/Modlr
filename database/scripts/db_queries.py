import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "app.db"


def insert_model_type(name: str, description: str) -> int | None:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO model_types (name, description) VALUES (?, ?)",
            (name, description),
        )
        conn.commit()
        return cur.lastrowid


def insert_model(
    profile_id: int,
    model_type_id: int,
    name: str,
    description: str,
    model_path: str,
    parameters: str,
    metrics: str,
) -> int | None:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO models (profile_id, model_type_id, name, description, model_path, parameters, metrics) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                profile_id,
                model_type_id,
                name,
                description,
                model_path,
                parameters,
                metrics,
            ),
        )
        conn.commit()
        return cur.lastrowid


def insert_model_feature(
    model_id: int, feature_name: str, feature_type: str, configuration: str
) -> int | None:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO model_features (model_id, feature_name, feature_type, configuration) VALUES (?, ?, ?, ?)",
            (
                model_id,
                feature_name,
                feature_type,
                configuration,
            ),
        )
        conn.commit()
        return cur.lastrowid


def insert_profile(name: str, description: str) -> None | int:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO profiles (name, description) VALUES (?, ?)",
            (
                name,
                description,
            ),
        )
        conn.commit()
        return cur.lastrowid
