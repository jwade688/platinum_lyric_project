# platinum_lyric_project
​
## Project Overview
The team will build a model that trains the lyrics of a song to predict whether a song will be a hit or not. The team will also use models to find out what other features of songs will predict a song’s success. Other features may include genre, key, tempo, danceability, energy, valence, speechiness, instrumentalness, liveness, loudness, etc. We will also set out to see what qualities do popular songs have by looking for patterns in lyric usage and in the values of the other features.\

## Overview of deliverables:
This is where you can find each deliverable:
- [Presentation](https://docs.google.com/presentation/d/1A0AKYPwMegvyjUKwBNw9hxdayrQQJ91O0xqz_ttyTOk/edit?usp=sharing)
- ETL overview: ETL/ETL_README.md
- ML overview: README_ML.md
- [Web app deployed to Heroku](https://platinum-lyric.herokuapp.com/)
- [Tableau Dashboard](https://public.tableau.com/profile/jacob.wade#!/vizhome/platinum_tableau_dashboard2/Featurestory?publish=yes)

__Reason for selected topic:__ This topic was selected for its potential usability in real-life, by plugging in the metrics and lyrics of unreleased songs to determine the likelihood of its success.\
​
__Project questions__: 
- Can a song’s lyrics predict its success? 
- What features predict a song’s success?
​
## Data Source
* see ETL/ETL_README.md
​
## Technologies Used
* __Data Cleaning and Analysis:__
Python and Pandas will be used to clean the data and perform an exploratory analysis in Jupyter Notebook.
​
* __Database Storage:__
We used a PostgreSQL database to join the data, which was then uploaded to and AWS S3 bucket and will be integrated with our machine learning model and with the app's JavaScript file to create visualizations.
​
* __Machine Learning:__
SciKitLearn is the Python Machine Learning library we will be using to create the classifier.
​
* __Dashboard:__
The dashboard will be created using an HTML template, a Python app, SQLAlchemy to pull data from the Database, Plotly to create visualizations, including interactive elements using JavaScript/jQuery. The final app will be deployed to Heroku.

## Communication protocol:
- Daily slack communications
- 2-4 zoom calls 
- Code reviews on GitHub