CREATE TABLE lyrics(
	track_id varchar(20),
	mxm_tid varchar(20),
	word varchar(50),
	word_count smallint,
	is_test smallint
);

CREATE TABLE spotify(
	spot_id varchar(100),
	artist_name VARCHAR(100),
	song_title VARCHAR(200),
	song_year smallint,
	feature_genre VARCHAR(300),	
	feature_popularity SMALLINT,
	feature_duration INTEGER,
	feature_key SMALLINT,	
	feature_acousticness NUMERIC,	
	feature_instrumentalness NUMERIC,	
	feature_tempo NUMERIC,	
	feature_mode SMALLINT,	
	feature_danceability NUMERIC,	
	feature_energy NUMERIC,	
	feature_liveness NUMERIC,
	feature_loudness NUMERIC,
	feature_speechiness NUMERIC,
	feature_valence NUMERIC,
	feature_explicit SMALLINT	
);

CREATE TABLE bb_id(
	track_id varchar(20),
	artist_name varchar(200),
	song_title varchar(200),
	song_year smallint,
	target_success smallint,
	target_weeks smallint,
	target_peak smallint,
	primary key	(track_id)
);	

CREATE TABLE bb_no_id(
	artist_name varchar(200),
	song_title varchar(200),
	song_year smallint,
	target_success smallint,
	target_weeks smallint,
	target_peak smallint
);	

CREATE TABLE million_songs(
	track_id varchar(20),
	artist_name varchar(200),
	song_title varchar(200),
	primary key(track_id)
);
