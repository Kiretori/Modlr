import sqlite3
from sqlite3 import Cursor

from dataclasses import dataclass

from database import DB_PATH


@dataclass
class ProfileData:
    # Profile data
    profile_name: str
    profile_description: str

@dataclass
class ModelBlueprint:
    # Model type data
    model_type_id: int

    # Model data
    model_name: str
    model_description: str | None
    model_path: str
    parameters: str | None
    metrics: str | None

    # Features
    features: list[dict[str, str]] = None

    def __post_init__(self):
        if self.features is None:
            self.features = []


def insert_complete_preset(profile_data: ProfileData, model_blueprints: list[ModelBlueprint]) -> dict[str, str] | Exception:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        # Insert profile
        profile_id = insert_profile(cur, profile_data.profile_name, profile_data.profile_description)

        for blueprint in model_blueprints:
            model_id = insert_model(
                cur,
                profile_id,
                blueprint.model_type_id,
                blueprint.model_name,
                blueprint.model_description,
                blueprint.model_path,
                blueprint.parameters,
                blueprint.metrics,
            )

            feature_ids = []
            for feature in blueprint.features:
                feature_id = insert_model_feature(
                    cur,
                    model_id,
                    feature.get("feature_name", ""),
                    feature.get("feature_type", ""),
                    feature.get("configuration", ""),
                )
                feature_ids.append(feature_id)

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()


def insert_model_type(cur: Cursor, name: str, description: str) -> int | None:
    cur.execute(
        "INSERT INTO model_types (name, description) VALUES (?, ?)",
        (name, description),
    )

    return cur.lastrowid


def insert_model(
    cur: Cursor,
    profile_id: int,
    model_type_id: int,
    name: str,
    description: str,
    model_path: str,
    parameters: str,
    metrics: str,
) -> int | None:
    cur.execute(
        "INSERT INTO models (profile_id, model_type_id, name, description, serialized_path, parameters, metrics) VALUES (?, ?, ?, ?, ?, ?, ?)",
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
    return cur.lastrowid


def insert_model_feature(
    cur: Cursor, model_id: int, feature_name: str, feature_type: str, configuration: str
) -> int | None:
    cur.execute(
        "INSERT INTO model_features (model_id, feature_name, feature_type, configuration) VALUES (?, ?, ?, ?)",
        (
            model_id,
            feature_name,
            feature_type,
            configuration,
        ),
    )

    return cur.lastrowid


def insert_profile(cur: Cursor, name: str, description: str) -> None | int:
    cur.execute(
        "INSERT INTO profiles (name, description) VALUES (?, ?)",
        (
            name,
            description,
        ),
    )
    return cur.lastrowid

