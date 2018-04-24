SET GLOBAL innodb_buffer_pool_size = 100000000;

ALTER TABLE users ADD PRIMARY KEY (id);

ALTER TABLE title_types ADD PRIMARY KEY (id);

ALTER TABLE titles ADD PRIMARY KEY (id);
ALTER TABLE titles
ADD CONSTRAINT titles_type_fk
FOREIGN KEY (type_id) REFERENCES title_types(id);
CREATE INDEX titles_primary_title_idx ON titles (primary_title);
CREATE INDEX titles_original_title_idx ON titles (original_title);
CREATE INDEX titles_imdb_id_idx ON titles (imdb_id);

ALTER TABLE genres ADD PRIMARY KEY (id);

ALTER TABLE has_genre ADD PRIMARY KEY (title_id, genre_id);
ALTER TABLE has_genre
ADD CONSTRAINT has_genre_title_fk
FOREIGN KEY (title_id) REFERENCES titles(id);
ALTER TABLE has_genre
ADD CONSTRAINT has_genre_genre_fk
FOREIGN KEY (genre_id) REFERENCES genres(id);

ALTER TABLE episodes ADD PRIMARY KEY (title_id);
ALTER TABLE episodes
ADD CONSTRAINT episodes_title_fk
FOREIGN KEY (title_id) REFERENCES titles(id);
ALTER TABLE episodes
ADD CONSTRAINT episodes_parent_title_fk
FOREIGN KEY (parent_title_id) REFERENCES titles(id);

ALTER TABLE rates ADD PRIMARY KEY (user_id, title_id);
ALTER TABLE rates
ADD CONSTRAINT rates_user_fk
FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE rates
ADD CONSTRAINT rates_title_fk
FOREIGN KEY (title_id) REFERENCES titles(id);

ALTER TABLE people ADD PRIMARY KEY (id);
CREATE INDEX people_name_idx ON people (name);

ALTER TABLE known_for ADD PRIMARY KEY (people_id, title_id);
ALTER TABLE known_for
ADD CONSTRAINT known_for_people_fk
FOREIGN KEY (people_id) REFERENCES people(id);
ALTER TABLE known_for
ADD CONSTRAINT known_for_title_fk
FOREIGN KEY (title_id) REFERENCES titles(id);

ALTER TABLE writes ADD PRIMARY KEY (people_id, title_id);
ALTER TABLE writes
ADD CONSTRAINT writes_people_fk
FOREIGN KEY (people_id) REFERENCES people(id);
ALTER TABLE writes
ADD CONSTRAINT writes_title_fk
FOREIGN KEY (title_id) REFERENCES titles(id);

ALTER TABLE directs ADD PRIMARY KEY (people_id, title_id);
ALTER TABLE directs
ADD CONSTRAINT directs_people_fk
FOREIGN KEY (people_id) REFERENCES people(id);
ALTER TABLE directs
ADD CONSTRAINT directs_title_fk
FOREIGN KEY (title_id) REFERENCES titles(id);

ALTER TABLE professions ADD PRIMARY KEY (id);

ALTER TABLE has_profession ADD PRIMARY KEY (people_id, profession_id);
ALTER TABLE has_profession
ADD CONSTRAINT has_profession_people_fk
FOREIGN KEY (people_id) REFERENCES people(id);
ALTER TABLE has_profession
ADD CONSTRAINT has_profession_profession_fk
FOREIGN KEY (profession_id) REFERENCES professions(id);
