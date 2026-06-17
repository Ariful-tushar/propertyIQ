CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,

    title TEXT NOT NULL,

    price INTEGER,

    size_of_property NUMERIC(6,2),

    rooms NUMERIC(4,1),

    location_of_property TEXT,

    description_of_property TEXT,

    property_url TEXT
    UNIQUE NOT NULL,

    image_url TEXT,

    source TEXT NOT NULL,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS property_metadata (
    property_id INTEGER PRIMARY KEY
    REFERENCES properties(id)
    ON DELETE CASCADE,

    attributes JSONB,

    ai_signals JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE property_analysis (
    id SERIAL PRIMARY KEY,

    property_id INTEGER
    REFERENCES properties(id)
    ON DELETE CASCADE,

    deal_score INTEGER CHECK (
        deal_score >= 0
        AND deal_score <= 100
    ),

    recommendation_label TEXT,
    summary TEXT,

    pros JSONB,
    cons JSONB,

    model_name TEXT,
    prompt_version TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scrape_logs (
    id SERIAL PRIMARY KEY,

    run_id TEXT,

    url TEXT,
    source TEXT,

    status TEXT,

    extraction_method TEXT,

    used_llm BOOLEAN DEFAULT FALSE,

    retry_count INTEGER DEFAULT 0,

    error_type TEXT,
    error_message TEXT,

    started_at TIMESTAMP,
    finished_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);