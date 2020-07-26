# platinum_lyric_project
​
## Project Overview
The team will build a model that trains the lyrics of a song to predict whether a song will be a hit or not. The team will also use models to find out what other features of songs will predict a song’s success. Other features may include genre, key, tempo, danceability, energy, valence, speechiness, instrumentalness, liveness, loudness, etc. We will also set out to see what qualities do popular songs have by looking for patterns in lyric usage and in the values of the other features.
​
__Reason for selected topic:__ This topic was selected for its potential usability in real-life, by plugging in the metrics and lyrics of unreleased songs to determine the likelihood of its success.
​
__Project questions__: 
- Can a song’s lyrics predict its success? 
- What features predict a song’s success?
​
## Data Source
* [Lyrics data](http://millionsongdataset.com/musixmatch/): The musiXmatch Dataset
    - Columns: 'track_id', 'word' (list of words entered according to popularity)
* [Song ID Data](http://millionsongdataset.com/pages/getting-dataset/): From the Million Song Dataset
    - Columns: 'track id', 'artist name', 'song title'
* [Billboard Data](): Information about the MSD tracks that were also featured in the Billboard Hot 100 charts
    - Columns: 'MSD id', 'artist name', 'track title', 'release year', 'peak' (position in Billboard charts) and 'weeks' (the number of weeks in the charts)
* [Spotify Data](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks): 160k+ songs from Kaggle in CSV spanning from 1921 to 2020
    - Columns: 'acousticness', 'artists', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness'
​
## Technologies Used
* __Data Cleaning and Analysis:__
Python and Pandas will be used to clean the data and perform an exploratory analysis in Jupyter Notebook.
​
* __Database Storage:__
We intend to use a PostgreSQL database to store the data, which will be integrated with our machine learning model and with the app's JavaScript file to create visualizations.
​
* __Machine Learning:__
SciKitLearn is the Python Machine Learning library we will be using to create the classifier.
​
* __Dashboard:__
The dashboard will be created using JavaScript, including interactive visualizations using D3.js to retrieve data from our database, as well as Tableau visualizations. The final app will be deployed to GitHub Pages.
Coll

## Branch overview of deliverables:
This is where you can find each deliverable:
- technology.md: jacob_branch
- erd and cleaned data: coco_branch
- machine model mockup: samin_branch