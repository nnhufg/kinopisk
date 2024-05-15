CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT not null,
    file_path TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work(id),
    FOREIGN KEY (genre_id) REFERENCES content.genre(id),
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work(id),
    FOREIGN KEY (person_id) REFERENCES content.person(id),
    role TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE INDEX IF NOT EXISTS idx_title ON content.film_work (title);

CREATE UNIQUE INDEX IF NOT EXISTS idx_film_work_genre ON content.genre_film_work (film_work_id, genre_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_film_work_person ON content.person_film_work (film_work_id, person_id);

ALTER TABLE content.genre ADD CONSTRAINT uk_name UNIQUE (name);
ALTER TABLE content.person ADD CONSTRAINT uk_full_name UNIQUE (full_name);