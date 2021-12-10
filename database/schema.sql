CREATE DATABASE IF NOT EXISTS aoe4_stats;
USE aoe4_stats;

CREATE TABLE IF NOT EXISTS match_record (
    match_id           BIGINT PRIMARY KEY,
    lobby_id           BIGINT,
    start_time         BIGINT,
    server             VARCHAR(32),

    game_version       INT,
    map_type           INT,

    player1_profile_id BIGINT,
    player1_civ        INT,
    player1_win        BOOLEAN,

    player2_profile_id BIGINT,
    player2_civ        INT,
    player2_win        BOOLEAN,

    winning_civ        INT,
    losing_civ         INT
);

CREATE TABLE IF NOT EXISTS queried_player (
    profile_id BIGINT PRIMARY KEY
);


