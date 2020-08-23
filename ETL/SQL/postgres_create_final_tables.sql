-- joining pivot and million_songs (without words columns that we'll add at the end) to get track_id, artist_name 
-- and song_title for each song
create table pivot_songs as
select p.track_id, m.artist_name, m.song_title
from pivot as p
inner join million_songs as m  using(track_id);

ALTER TABLE pivot_songs
ADD PRIMARY KEY (track_id);

-- join pivot_songs and bb_id on track_id
create table pivot_songs_bb as
select p.track_id, p.artist_name, p.song_title, b.song_year, b.target_success, b.target_weeks, b.target_peak
from pivot_songs as p
inner join bb_id as b using(track_id);

ALTER TABLE pivot_songs_bb
ADD PRIMARY KEY (track_id);

-- this is a test to select the remaining of pivot_songs (minus pivot_songs_bb) 
-- that we'll use in the next join - to avoid duplicates
select p.track_id, p.artist_name, p.song_title
from pivot_songs p
except
select pb.track_id, pb.artist_name, pb.song_title
from pivot_songs_bb pb

--join pivot_songs and bb_no_id on artist_name and song_title (already unique in bb_no_id)
create table pivot_songs_bb_no_id as
select p.track_id, p.artist_name, p.song_title, b.song_year, b.target_success, b.target_weeks, b.target_peak
from (
	select ps.track_id, ps.artist_name, ps.song_title
	from pivot_songs ps
	except
	select pb.track_id, pb.artist_name, pb.song_title
	from pivot_songs_bb pb
) as p
inner join bb_no_id as b
on p.artist_name = b.artist_name and p.song_title=b.song_title;

ALTER TABLE pivot_songs_bb_no_id
ADD PRIMARY KEY (track_id); --this gives error message, so there are duplicates "track_id"

--to delete duplicates (on track_id) we create a serial id (new primary key),
--then delete the rows with different id and same track_id
ALTER TABLE pivot_songs_bb_no_id
	ADD COLUMN id SERIAL PRIMARY KEY;

DELETE FROM pivot_songs_bb_no_id p1
    USING   pivot_songs_bb_no_id p2
WHERE  p1.id < p2.id  
    AND p1.track_id  = p2.track_id;
	
--concatenate both tables - pivot_songs_bb final set (without word columns)
--"ON CONFLICT (track_id) DO NOTHING;" says not to add any row with track_id already present (track_id is a primary key)
insert into pivot_songs_bb
(select p.track_id, p.artist_name, p.song_title, p.song_year, p.target_success, p.target_weeks, p.target_peak
 from pivot_songs_bb_no_id p)
ON CONFLICT (track_id)
DO NOTHING;

--drop unneccessary table
drop table pivot_songs_bb_no_id;

--adding the word columns to get the final platinum_lyrics table
create table platinum_lyrics as
select * 
from pivot_songs_bb
inner join pivot using (track_id);

--join final set pivot_songs_bb and spotify to get platinum_features
create table platinum_features as
select p.track_id, p.artist_name, p.song_title,p.song_year, s.feature_genre, s.feature_popularity, s.feature_duration, s.feature_key,
		s.feature_acousticness, s.feature_instrumentalness, s.feature_tempo, s.feature_mode, s.feature_danceability, s.feature_energy, s.feature_liveness,
		s.feature_loudness, s.feature_speechiness, s.feature_valence, s.feature_explicit, p.target_success, p.target_weeks, p.target_peak
from pivot_songs_bb p
inner join spotify s
on p.artist_name=s.artist_name and p.song_title=s.song_title
;

ALTER TABLE platinum_features
ADD PRIMARY KEY (track_id); --this gives error message, so there are duplicates "track_id"

ALTER TABLE platinum_features
	ADD COLUMN id SERIAL PRIMARY KEY;
	
DELETE FROM platinum_features p1
    USING   platinum_features p2
WHERE  p1.id < p2.id  
    AND p1.track_id  = p2.track_id;
	
alter table platinum_features
drop column id;

-- this is the final set platinum_features (without lryrics)
-- join with pivot to get the final set with lyrics and features, platinum_lyrics_features
create table platinum_lyrics_features as
select *
from platinum_features
inner join pivot using (track_id);


--- create the platinum_spotify table
--join with spotify only (no target success)
create table pivot_spotify as
select p.track_id, s.spot_id, p.artist_name, p.song_title, s.song_year, s.feature_genre
from pivot_songs p
inner join spotify s
on p.artist_name=s.artist_name and p.song_title=s.song_title;

alter pivot_spotify
add primary key(track_id);  -- error message : duplicates

ALTER TABLE pivot_spotify
	ADD COLUMN id SERIAL PRIMARY KEY;
	
DELETE FROM pivot_spotify p1
    USING   pivot_spotify p2
WHERE  p1.id < p2.id  
    AND p1.track_id  = p2.track_id;
	
select * from pivot_spotify;	

alter table pivot_spotify
drop column id;

create table platinum_spotify as
select *
from pivot_spotify
inner join pivot using(track_id);


-- remove 4 word columns that were problematic for machine 
--learning models but were not removed during data cleaning 

-- remove word_cost, word_oder, word_the, word_que columns from 
--all datasets
alter table pivot
drop column word_cost,
drop column word_oder,
drop column word_que,
drop column word_the;

alter table platinum_lyrics
drop column word_cost,
drop column word_oder,
drop column word_que,
drop column word_the;

alter table platinum_lyrics_features
drop column word_cost,
drop column word_oder,
drop column word_que,
drop column word_the;

alter table platinum_spotify
drop column word_cost,
drop column word_oder,
drop column word_que,
drop column word_the;



--------------------------------------------
--------------------------------------------
-- final sets:
-- platinum_lyrics
-- platinum_lyrics_features
-- platinum_features
-- platinum_spotify
-----------------------------------------------
----------------------------------------------




