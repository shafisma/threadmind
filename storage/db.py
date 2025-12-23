import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS summaries (
 id INTEGER PRIMARY KEY,
 guild_id TEXT,
 channel_id TEXT,
 content TEXT,
 created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decisions (
 id INTEGER PRIMARY KEY,
 channel_id TEXT,
 decision TEXT,
 confidence REAL
);

CREATE TABLE IF NOT EXISTS auto_config (
 channel_id TEXT PRIMARY KEY,
 interval INTEGER,
 last_run INTEGER
);

CREATE TABLE IF NOT EXISTS guild_settings (
 guild_id TEXT PRIMARY KEY,
 tone TEXT DEFAULT 'professional',
 gemini_api_key TEXT
);

CREATE TABLE IF NOT EXISTS permissions (
 guild_id TEXT,
 role_id TEXT,
 command TEXT
);
""")
conn.commit()
