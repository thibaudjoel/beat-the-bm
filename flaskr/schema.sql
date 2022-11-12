DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS model;
DROP TABLE IF EXISTS model_type;
DROP TABLE IF EXISTS feature;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE model (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id INTEGER NOT NULL,
    feature_id INTEGER NOT NULL,
    model_type_id INTEGER NOT NULL,
    title text NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES user (id),
    FOREIGN KEY (feature_id) REFERENCES feature (id),
    FOREIGN KEY (model_type_id) REFERENCES model_type (id)
);

--Handled by admin only
CREATE TABLE model_type(
    id INTEGER PRIMARY KEY,
    type TEXT UNIQUE
)
--Handled by admin
CREATE TABLE feature(
    id INTEGER PRIMARY KEY,
    feature text
)