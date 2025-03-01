
-- Profiles table to store preset profiles
CREATE TABLE profiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name)
);

-- Model types table (classification, regression, clustering, etc.)
CREATE TABLE model_types (
    model_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Models table to store ML model metadata
CREATE TABLE models (
    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    model_type_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    serialized_path TEXT,  -- Path to the serialized model file
    parameters TEXT,       -- JSON string of model parameters
    metrics TEXT,          -- JSON string of model performance metrics
    FOREIGN KEY (profile_id) REFERENCES profiles(profile_id) ON DELETE CASCADE,
    FOREIGN KEY (model_type_id) REFERENCES model_types(model_type_id),
    UNIQUE(profile_id, name)
);

-- Table for model features/configuration
CREATE TABLE model_features (
    feature_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    feature_name TEXT NOT NULL,
    feature_type TEXT NOT NULL,
    configuration TEXT,    -- JSON string for feature-specific configuration
    FOREIGN KEY (model_id) REFERENCES models(model_id) ON DELETE CASCADE,
    UNIQUE(model_id, feature_name)
);

-- Table for model version history
CREATE TABLE model_versions (
    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    version_number INTEGER NOT NULL,
    serialized_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metrics TEXT,          -- JSON string of model performance metrics
    parameters TEXT,       -- JSON string of model parameters
    FOREIGN KEY (model_id) REFERENCES models(model_id) ON DELETE CASCADE,
    UNIQUE(model_id, version_number)
);