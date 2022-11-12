DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS model;
DROP TABLE IF EXISTS model_type;
DROP TABLE IF EXISTS features;
DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS league;
DROP TABLE IF EXISTS season;
DROP TABLE IF EXISTS season_team;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS country;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE model (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id INTEGER NOT NULL,
    features_id (BIT,BIT) NOT NULL,
    model_type_id INTEGER NOT NULL,
    title text NOT NULL,
    number_of_last_games INTEGER NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES user (id),
    FOREIGN KEY (features_id) REFERENCES feature (goal_result),
    FOREIGN KEY (model_type_id) REFERENCES model_type (id)
);

--Handled by admin only
CREATE TABLE model_type(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_code TEXT UNIQUE
);

CREATE TABLE features(
    goal BIT ,
    result BIT,
    constraint goal_result PRIMARY KEY (goal, result),
    constraint chk_null check (goal_id  or result)
);

CREATE TABLE match(
    id INT PRIMARY KEY AUTOINCREMENT,
    league_id INT,
    season_id INT,
    match_date Date,
    match_time Time,
    home_team_id INT,
    away_team_id INT,
    full_time_home_team_goals INT,
    full_time_result INT,
    B365D REAL,
    B365H REAL,
    B365A REAL,
    FOREIGN KEY (league_id) REFERENCES league(id),
    FOREIGN KEY (season_id) REFERENCES season(id),
    FOREIGN KEY (home_team_id) REFERENCES team(id),
    FOREIGN KEY (away_team_id) REFERENCES team(id)
);

CREATE TABLE league(
    id INT PRIMARY AUTOINCREMENT,
    league_name TEXT,
    country_id INT,
    FOREIGN KEY (country_id) REFERENCES country(id)
);

CREATE TABLE season(
    id INT PRIMARY AUTOINCREMENT,
    league_id INT,
    season_name TEXT,
    season_start Date,
    season_end Date,
    FOREIGN KEY (league_id) REFERENCES league(id)
);

CREATE TABLE season_team(
    season_id INT,
    team_id INT,
    FOREIGN KEY (season_id) REFERENCES season(id),
    FOREIGN KEY (team_id) REFERENCES team(id)
);

CREATE TABLE team(
    id INT PRIMARY AUTOINCREMENT,
    team_name TEXT,
    country_id INT
    FOREIGN KEY (country_id) REFERENCES country(id)
);

CREATE TABLE country(
    id INT PRIMARY AUTOINCREMENT,
    country_name TEXT
);