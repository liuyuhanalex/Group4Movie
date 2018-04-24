SET GLOBAL innodb_buffer_pool_size = 100000000;
SET innodb_lock_wait_timeout=100;
SET SQL_SAFE_UPDATES = 0;

ALTER TABLE titles ADD COLUMN num_ratings INT;
ALTER TABLE titles ADD COLUMN avg_rating FLOAT;
ALTER TABLE users ADD COLUMN num_ratings INT;
ALTER TABLE genres ADD COLUMN num_titles INT;
ALTER TABLE genres ADD COLUMN num_ratings INT;
ALTER TABLE genres ADD COLUMN avg_rating FLOAT;

UPDATE titles t
SET t.num_ratings = (
    SELECT COUNT(*)
    FROM rates r
    WHERE r.title_id = t.id
),
t.avg_rating = (
    SELECT AVG(r.rating)
    FROM rates r
    WHERE r.title_id = t.id
);

UPDATE users u
SET u.num_ratings = (
    SELECT COUNT(*)
    FROM rates r
    WHERE r.user_id = u.id
);

UPDATE genres g
SET g.num_titles = (
    SELECT COUNT(DISTINCT h.title_id)
    FROM has_genre h
    WHERE h.genre_id = g.id
),
g.num_ratings = (
    SELECT COUNT(*)
    FROM rates r JOIN has_genre h ON r.title_id = h.title_id
    WHERE h.genre_id = g.id
),
g.avg_rating = (
    SELECT AVG(r.rating)
    FROM rates r JOIN has_genre h ON r.title_id = h.title_id
    WHERE h.genre_id = g.id
);

-- Note that order of updates matters. Here we update avg_rating first,
-- then num_ratings.
CREATE TRIGGER title_agg_insert BEFORE INSERT ON rates
FOR EACH ROW
UPDATE titles t
SET t.avg_rating = (
    (t.avg_rating * t.num_ratings + NEW.rating) /
    (t.num_ratings + 1.0)
),
t.num_ratings = t.num_ratings + 1
WHERE t.id = NEW.title_id;

CREATE TRIGGER title_agg_delete BEFORE DELETE ON rates
FOR EACH ROW
UPDATE titles t
SET t.avg_rating = (
    (t.avg_rating * t.num_ratings - OLD.rating) /
    (t.num_ratings - 1.0)
),
t.num_ratings = t.num_ratings - 1
WHERE t.id = OLD.title_id;

CREATE TRIGGER user_ratings_incr BEFORE INSERT ON rates
FOR EACH ROW
UPDATE users u
SET u.num_ratings = u.num_ratings + 1
WHERE u.id = NEW.user_id;

CREATE TRIGGER user_ratings_decr BEFORE DELETE ON rates
FOR EACH ROW
UPDATE users u
SET u.num_ratings = u.num_ratings - 1
WHERE u.id = OLD.user_id;

-- If we add a title to a genre, the genre gets that title's ratings.
-- Average is total sum over total count.
CREATE TRIGGER genre_add_title BEFORE INSERT ON has_genre
FOR EACH ROW
UPDATE genres g
SET g.num_titles = g.num_titles + 1,
g.avg_rating = (
    (g.avg_rating * g.num_ratings + (
        SELECT t.avg_rating * t.num_ratings
        FROM titles t
        WHERE t.id = NEW.title_id
    )) /
    (g.num_ratings + (
        SELECT t.num_ratings
        FROM titles t
        WHERE t.id = NEW.title_id
    ))
),
g.num_ratings = g.num_ratings + (
    SELECT t.num_ratings
    FROM titles t
    WHERE t.id = NEW.title_id
)
WHERE g.id = NEW.genre_id;

CREATE TRIGGER genre_remove_title BEFORE DELETE ON has_genre
FOR EACH ROW
UPDATE genres g
SET g.num_titles = g.num_titles - 1,
g.avg_rating = (
    (g.avg_rating * g.num_ratings - (
        SELECT t.avg_rating * t.num_ratings
        FROM titles t
        WHERE t.id = OLD.title_id
    )) /
    (g.num_ratings - (
        SELECT t.num_ratings
        FROM titles t
        WHERE t.id = OLD.title_id
    ))
),
g.num_ratings = g.num_ratings - (
    SELECT t.num_ratings
    FROM titles t
    WHERE t.id = OLD.title_id
)
WHERE g.id = OLD.genre_id;

CREATE TRIGGER genre_agg_insert BEFORE INSERT ON rates
FOR EACH ROW
UPDATE genres g
SET g.avg_rating = (
    (g.avg_rating * g.num_ratings + NEW.rating) /
    (g.num_ratings + 1.0)
),
g.num_ratings = g.num_ratings + 1
WHERE g.id IN (
    SELECT h.genre_id
    FROM titles t JOIN has_genre h ON t.id = h.title_id
    WHERE t.id = NEW.title_id
);

CREATE TRIGGER genre_agg_delete BEFORE DELETE ON rates
FOR EACH ROW
UPDATE genres g
SET g.avg_rating = (
    (g.avg_rating * g.num_ratings - OLD.rating) /
    (g.num_ratings - 1.0)
),
g.num_ratings = g.num_ratings - 1
WHERE g.id IN (
    SELECT h.genre_id
    FROM titles t JOIN has_genre h ON t.id = h.title_id
    WHERE t.id = OLD.title_id
);
