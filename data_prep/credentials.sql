ALTER TABLE users ADD COLUMN username VARCHAR(255);
ALTER TABLE users ADD UNIQUE (username);
CREATE INDEX users_username_idx ON users (username);
ALTER TABLE users ADD COLUMN password VARCHAR(255);
