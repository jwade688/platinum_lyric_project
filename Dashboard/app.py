from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import password
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

app = Flask(__name__)

# Set up postgres connection
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:{password}@localhost:5432/tennis_db"
# "postgres://admin:donotusethispassword@aws-us-east-1-portal.19.dblayer.com:15813/compose"

# Create a Flask-SQLAlchemy instance
db = SQLAlchemy(app)

def lyrics_BoW():
    lyrics = "My house is beautiful"
    # Tokenizing
    words = nltk.word_tokenize(lyrics)
    
    # Create an object of class PorterStemmer; set stopwords from NLTK as variable
    porter = PorterStemmer()
    stop_words = stopwords.words('english')

    # Removing stopwords and stemming the remaining ones
    filtered_lyrics = [porter.stem(w) for w in words if not w in stop_words]
    
    # Creating frequency of each word and storing in dataframe
    wordfreq = {}
    for word in filtered_lyrics:
        if word not in wordfreq.keys():
            wordfreq[word] = 1
        else:
            wordfreq[word] += 1
    
    # Updating dictionary with the genre (user input)
    genre = "rock"
    wordfreq.update({"genre": genre})

    # Adding dictionary to dataframe to be used in the ML Model
    wordfreq_df = pd.DataFrame(data=wordfreq, index=[0])


def create_plot():
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe

    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]   

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

class Players(db.Model):
    __tablename__ = 'players'

    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    hand = db.Column(db.String())
    country_code = db.Column(db.String())

    def __repr__(self): 
        return f"<Customer {self.first_name}>"


@app.route("/")
def index():
    graphJSON = create_plot()
    return render_template("index.html", graphJSON=graphJSON)


@app.route("/tennis_players", methods=['GET'])

def tennis_players():
    players = Players.query.all()
    results = [
        {
            "id": player.player_id,
            "name": player.first_name
        } for player in players
    ]
    return {"players": results}


if __name__ == "__main__":
   app.run(debug=True)