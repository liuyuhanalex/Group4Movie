-- Remove null genres
DELETE FROM has_genre
WHERE genre_id = (SELECT id FROM genres WHERE name = '\\N');

DELETE FROM genres WHERE name = '\\N';


-- Remove null professions
DELETE FROM has_profession
WHERE profession_id = (SELECT id FROM professions WHERE name IS NULL);

DELETE FROM professions WHERE name IS NULL;
