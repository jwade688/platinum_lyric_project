from flask import Flask, render_template, jsonify, request
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
from word_columns import word_columns

app = Flask(__name__)

# Set up postgres connection
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:{password}@localhost:5432/tennis_db"
# "postgres://admin:donotusethispassword@aws-us-east-1-portal.19.dblayer.com:15813/compose"

# Create a Flask-SQLAlchemy instance
db = SQLAlchemy(app)


from word_columns import word_columns

def lyrics_BoW(lyrics):
    
    # Creating dataframe to match trained ML model, with words as columns and row filled with zeros
    print(len(word_columns))    
    z = numpy.zeros(dtype=int, shape=(1,len(word_columns)))
    model_df = pd.DataFrame(z, columns=word_columns)

    # Tokenizing
    words = nltk.word_tokenize(lyrics)
    
    # Create an object of class PorterStemmer; set stopwords from NLTK as variable
    porter = PorterStemmer()
    stop_words = stopwords.words('english')

    # Removing stopwords and stemming the remaining ones
    filtered_lyrics = [porter.stem(w) for w in words if not w in stop_words]
    
    # Creating frequency of each word and storing in dataframe
    for word in filtered_lyrics:
        if word in model_df.columns:
            model_df[word] += 1
    
    # Updating dictionary with the genre (user input)
    genre = "rock"
    model_df["genre"] = genre

    return filtered_lyrics


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

@app.route("/lyrics/<userInput>", methods=["GET"])

def post_lyrics(userInput=None):
    print(userInput) # This will print user's input to the terminal

    # response = jsonify("hard coded test from Flask route")
    response = jsonify(userInput) # returns a flask.Response() object that already has the appropriate content-type header 'application/json' for use with json responses
    response.headers.add("Access-Control-Allow-Origin", "*")

    lyrics_json = json.dumps(userInput) # return an encoded string, which would require manually adding the MIME type header.
    print(f"Printing response: {lyrics_json}")
    # lyrics_BoW(lyrics_json)
    
    return response # Function returns this, but only gets printed to Console because of d3.json function --> console.log(data)



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
    # we first try to grab the port from the app’s environment, and if not found, it defaults to port 5000
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)