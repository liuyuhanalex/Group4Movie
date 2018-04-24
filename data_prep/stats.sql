SET GLOBAL innodb_buffer_pool_size = 100000000;

CREATE TABLE IF NOT EXISTS stats (
    id INT AUTO_INCREMENT,
    title_count INT,
    people_count INT,
    user_count INT,
    rating_count INT,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS top_titles (
    rank INT,
    title_id INT,
    -- We want the index clustered on rank since we'll be sorting on it
    PRIMARY KEY (rank),
    FOREIGN KEY (title_id) REFERENCES titles(id)
);

-- This would be recomputed periodically
DELETE FROM top_titles;
SET @rank := 0;
INSERT INTO top_titles (rank, title_id)
SELECT @rank := @rank + 1 AS rank, id
FROM titles
ORDER BY avg_rating * num_ratings DESC
LIMIT 10;

DELETE FROM stats;
INSERT INTO stats (title_count, people_count, user_count, rating_count)
SELECT
    (SELECT COUNT(*) FROM titles),
    (SELECT COUNT(*) FROM people),
    (SELECT COUNT(*) FROM users),
    (SELECT COUNT(*) FROM rates);

CREATE TRIGGER title_count_incr BEFORE INSERT ON titles
FOR EACH ROW
UPDATE stats
SET title_count = title_count + 1;

CREATE TRIGGER title_count_decr BEFORE DELETE ON titles
FOR EACH ROW
UPDATE stats
SET title_count = title_count - 1;

CREATE TRIGGER people_count_incr BEFORE INSERT ON people
FOR EACH ROW
UPDATE stats
SET people_count = people_count + 1;

CREATE TRIGGER people_count_decr BEFORE DELETE ON people
FOR EACH ROW
UPDATE stats
SET people_count = people_count - 1;

CREATE TRIGGER user_count_incr BEFORE INSERT ON users
FOR EACH ROW
UPDATE stats
SET user_count = user_count + 1;

CREATE TRIGGER user_count_decr BEFORE DELETE ON users
FOR EACH ROW
UPDATE stats
SET user_count = user_count - 1;

CREATE TRIGGER rating_count_incr BEFORE INSERT ON rates
FOR EACH ROW
UPDATE stats
SET rating_count = rating_count + 1;

CREATE TRIGGER rating_count_decr BEFORE DELETE ON rates
FOR EACH ROW
UPDATE stats
SET rating_count = rating_count - 1;
