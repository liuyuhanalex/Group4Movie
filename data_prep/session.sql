CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40),
    session_data TEXT,
    expire_date DATETIME,
    PRIMARY KEY (session_key)
);

CREATE INDEX session_expire_data_idx ON django_session (expire_date);
