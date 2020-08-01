from flask import Flask, render_template, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from config import password
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import os
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from word_columns import word_columns
from model import modeltest

app = Flask(__name__)

# Set up postgres connection
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:{password}@localhost:5432/tennis_db"
# "postgres://admin:donotusethispassword@aws-us-east-1-portal.19.dblayer.com:15813/compose"

# Create a Flask-SQLAlchemy instance
db = SQLAlchemy(app)

# Declaring global variables
model_dict = {}
genre = ""

def lyrics_BoW(lyrics):
    global model_dict

    # Creating dictionary to match trained ML model, with words as keys and filled with zeros
    model_dict = dict.fromkeys(word_columns, 0)

    # Tokenizing
    words = nltk.word_tokenize(lyrics)
    
    # Create an object of class PorterStemmer; set stopwords from NLTK as variable
    porter = PorterStemmer()
    stop_words = stopwords.words('english')

    # Removing stopwords and stemming the remaining ones
    filtered_lyrics = [porter.stem(w) for w in words if not w in stop_words]
    
    # Creating frequency of each word and storing in model_dict dictionary
    for word in filtered_lyrics:
        if word in model_dict.keys():
            model_dict[word] += 1
    
    print(f"Result from lyrics_BoW: {model_dict}")
    return model_dict

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
    # graphJSON = create_plot()
    # return render_template("index.html", graphJSON=graphJSON)
    return render_template("index.html")


@app.route("/lyrics/<userInput>", methods=["GET"])
def post_lyrics(userInput=None):

    # jsonify returns a flask.Response() object that already has the appropriate content-type header 'application/json' for use with json responses
    response = jsonify(userInput) 
    response.headers.add("Access-Control-Allow-Origin", "*")
    
    # return an encoded string.
    lyrics_json = json.dumps(userInput) 
    
    # Print user's input to the terminal
    print(f"Printing response: {lyrics_json}") 
    
    #Call function to preprocess lyrics and feed it through ML Model
    lyrics_BoW(lyrics_json)
    
    return response

# @app.route("/genre", methods=["POST"])
# def input_genre():
#     global genre
#     if request.method == 'POST':
#         genre = request.form['selectGenre']
#         print(f"Printing genre: {genre}")
#         return jsonify(genre)

@app.route("/genre/<userInput>", methods=["GET"])
def input_genre(userInput=None):
    global genre
    response = jsonify(userInput)
    response.headers.add("Access-Control-Allow-Origin", "*")
    genre = json.dumps(userInput)
    print(f"Printing genre: {genre}")
    return response


# @app.route("/genre", methods=["POST", "GET"])
# def input_genre():
#     global genre
#     if request.method == "POST":
#         selection = request.form["selectGenre"]
#         response = jsonify(selection)
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         genre = json.dumps(selection)
#         print(f"Printing genre: {genre}")
#     return response

# @app.route("/runmodel/<userInput>", methods=["GET"])
# def run_model(userInput=None):
#     global model_dict
#     response = jsonify(userInput)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     print("Entering runmodel route")
#     print(f"Genre from run_model function: {genre}")
#     # Updating dictionary with the genre (user input)
#     model_dict["song_genre"] = genre
        
#     # Creating final DataFrame
#     # df = pd.DataFrame(data=model_dict, index=[0])
        
#     # Call the ML Model function within this function
#     # modeltest(df)

#     return response

@app.route("/runmodel", methods=["GET", "POST"])
def run_model():
    global model_dict
    # global genre
    
    if request.method == 'POST':
        print("Entering runmodel route")
        print(f"Genre from run_model function: {genre}")
        # Updating dictionary with the genre (user input)
        # POSSIBLE PROBLEM: "song_genre" is being inserted in the middle of the dictionary, in alphabetical order
        model_dict["song_genre"] = genre
        # Creating final DataFrame
        # df = pd.DataFrame(data=model_dict, index=[0])
        
        # Call the ML Model function within this function
        # modeltest(df)

        # return render_template('index.html')
        return model_dict
    



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

db = SQLAlchemy()

# def query_to_list(query, include_field_names=True):
#     """Turns a SQLAlchemy query into a list of data values."""
#     column_names = []
#     for i, obj in enumerate(query.all()):
#         if i == 0:
#             column_names = [c.name for c in obj.__table__.columns]
#             if include_field_names:
#                 yield column_names
#         yield obj_to_list(obj, column_names)


# def obj_to_list(sa_obj, field_order):
#     """Takes a SQLAlchemy object - returns a list of all its data"""
#     return [getattr(sa_obj, field_name, None) for field_name in field_order]

if __name__ == "__main__":
    app.run(debug=True)
    # we first try to grab the port from the app’s environment, and if not found, it defaults to port 5000
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)