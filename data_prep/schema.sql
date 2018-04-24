CREATE TABLE IF NOT EXISTS users (
    id INT,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS title_types (
    id INT,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS titles (
    id INT,
    imdb_id VARCHAR(32),
    primary_title VARCHAR(255),
    original_title VARCHAR(255),
    is_adult BOOL,
    start_year INT,
    end_year INT,
    runtime FLOAT,
    type_id INT
);

CREATE TABLE IF NOT EXISTS genres (
    id INT,
    name VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS has_genre (
    title_id INT,
    genre_id INT
);

CREATE TABLE IF NOT EXISTS episodes (
    title_id INT,
    parent_title_id INT,
    season INT,
    episode INT
);

CREATE TABLE IF NOT EXISTS rates (
    user_id INT,
    title_id INT,
    rating INT
);

CREATE TABLE IF NOT EXISTS people (
    id INT,
    imdb_id VARCHAR(32),
    name VARCHAR(255),
    birth_year INT,
    death_year INT
);

CREATE TABLE IF NOT EXISTS known_for (
    people_id INT,
    title_id INT
);

CREATE TABLE IF NOT EXISTS writes (
    people_id INT,
    title_id INT
);

CREATE TABLE IF NOT EXISTS directs (
    people_id INT,
    title_id INT
);

CREATE TABLE IF NOT EXISTS professions (
    id INT,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS has_profession (
    people_id INT,
    profession_id INT
);
