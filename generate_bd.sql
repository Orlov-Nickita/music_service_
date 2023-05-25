CREATE TABLE IF NOT EXISTS "users"
(
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(50) NOT NULL,
    token UUID
);

CREATE TABLE IF NOT EXISTS "record"
(
    id      SERIAL PRIMARY KEY,
    uuid    UUID,
    mp3     TEXT,
    link    TEXT,
    user_id INTEGER REFERENCES users (id)
);