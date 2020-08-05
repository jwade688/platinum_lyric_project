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
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:{password}@localhost:5432/platinum_lyric"
# "postgres://admin:donotusethispassword@aws-us-east-1-portal.19.dblayer.com:15813/compose"

# Create a Flask-SQLAlchemy instance
db = SQLAlchemy(app)

# Declaring global variables
model_dict = {}
genre = ""
prediction = ""
features_by_year_results = []
selected_feature = "mode"

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

def plot_features_by_year(feature):
    print("Entering plot_features_by_year() function")
    global features_by_year_results
    # When user changes feature in dropdown, function (from route feature_select) that retrieves
    # user's feature selection runs and updates selected_feature variable
    print(f"Selected feature (plot_features_by_year() function): {selected_feature}")
    # Call function from route that retrieves values from database
    # Returns list of dictionaries, each dictionary is one element (row)
    features_by_year_results = by_year()
    print(f"plot_features_by_year()--> features_by_year_results from by_year() function: {features_by_year_results}")
    print(feature)
    year = [element["year"] for element in features_by_year_results]
    # feature_values = [element[feature] for element in features_by_year_results]
    feature_values = [element[feature] for element in features_by_year_results]


    data = [
        go.Bar(
            x = year,
            y = feature_values
        )
    ]

    features_by_year_JSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    
    return features_by_year_JSON

def plot_bubble_chart():
    print("Entering plot_bubble_chart() function.")
    global features_by_year_results
    print(f"plot_bubble_chart()--> features_by_year_results: {features_by_year_results}")

    # features_by_year_results = by_year()
    year = [element["year"] for element in features_by_year_results]
    energy = [element["energy"] for element in features_by_year_results]
    acoustiness = [element["acoustiness"] for element in features_by_year_results]
    loudness = [element["loudness"] for element in features_by_year_results]

    # graph = [
    #     dict(
    #         data = go.Scatter[
    #             dict(
    #                 x = year,
    #                 y = loudness,
    #                 mode = "markers",
    #                 marker = dict(
    #                     size = [n*100 for n in energy],
    #                     color = acoustiness,
    #                     colorscale='Viridis'
    #                     )
    #             )
    #         ],

    #         layout = dict(
    #             title = 'Bubble Chart Title',
    #             xaxis_title = "X Axis Title",
    #             yaxis_title = "X Axis Title"
    #         )
    #     )
    # ]


    data = [
        go.Scatter(
            x = year,
            y = loudness,
            mode = "markers",
            marker = dict(
                size = [n*100 for n in energy],
                color = acoustiness,
                colorscale='Viridis'
                )
        )
    ]

    # layout = dict(
    #             title = 'Bubble Chart Title',
    #             xaxis_title = "X Axis Title",
    #             yaxis_title = "X Axis Title"
    #         )

    bubble_chart_JSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    print(f"Return bubble_chart_JSON: {bubble_chart_JSON}")

    return bubble_chart_JSON

class Players(db.Model):
    __tablename__ = 'players'

    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    hand = db.Column(db.String())
    country_code = db.Column(db.String())

    def __repr__(self): 
        return f"<Customer {self.first_name}>"


class Byyear(db.Model):
    __tablename__ = 'features_by_year'

    feature_year = db.Column(db.BigInteger(), primary_key=True)
    feature_popularity = db.Column(db.Float())
    target_success = db.Column(db.Float())
    feature_duration = db.Column(db.Float())
    feature_tempo = db.Column(db.Float())
    feature_key = db.Column(db.Float())
    feature_mode = db.Column(db.Float())
    feature_acoustiness = db.Column(db.Float())
    feature_instrumentalness = db.Column(db.Float())
    feature_danceability = db.Column(db.Float())
    feature_energy = db.Column(db.Float())
    feature_liveness = db.Column(db.Float())
    feature_loudness = db.Column(db.Float())
    feature_speechiness = db.Column(db.Float())
    feature_valence = db.Column(db.Float())
    feature_explicit = db.Column(db.Float())
    target_peak = db.Column(db.Float())
    target_weeks = db.Column(db.Float())

    def __init__(self, feature_year):
        self.feature_year = feature_year

@app.route("/")
def index():
    global selected_feature
    print(f"Selected feature: {selected_feature}")
    features_by_year_JSON = plot_features_by_year(selected_feature)
    bubble_chart_JSON = plot_bubble_chart()
    print("Back to route /")
    print(f"Return bubble_chart_JSON from route /: {bubble_chart_JSON}")
    return render_template("index.html", features_by_year_JSON=features_by_year_JSON, bubble_chart_JSON=bubble_chart_JSON)


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
    global prediction
    # global genre
    
    if request.method == 'POST':
        print("Entering runmodel route")
        print(f"Genre from run_model function: {genre}")
        # Updating dictionary with the genre (user input)
        # POSSIBLE PROBLEM: "song_genre" is being inserted in the middle of the dictionary, in alphabetical order
        model_dict["song_genre"] = genre
        # Creating final DataFrame to pass into the model function
        # df = pd.DataFrame(data=model_dict, index=[0])
        
        # Call the ML Model function within this function
        # modeltest(df)
        # ML Model function will return binary prediction
        prediction = 0

        # return jsonify(prediction)
    return render_template("index.html", prediction=prediction)

@app.route("/feature_select/<userInput>", methods=["GET"])
def input_feature(userInput=None):
    print("Entering input_feature() function in /feature_select route")
    
    global selected_feature
    response = jsonify(userInput)
    response.headers.add("Access-Control-Allow-Origin", "*")
    selected_feature = json.dumps(userInput).strip('"')
    
    print(f"Selected feature (input_feature() function): {selected_feature}")

    # Call plot function to create plot using selected_feature variable
    features_by_year_JSON = plot_features_by_year(selected_feature)

    return render_template("index.html", features_by_year_JSON=features_by_year_JSON)
    # return response

@app.route("/features_by_year")
def by_year():
    global features_by_year_results
    print("Entering by_year() function in /features_by_year route to pull from Postgres")
    # Query database for all values from features_by_year table (defined in Byyear Class)
    features_by_year = Byyear.query.all()
    features_by_year_results = [
        {
            "year": year.feature_year,
            "mode": year.feature_mode,
            "acoustiness": year.feature_acoustiness,
            "instrumentalness": year.feature_instrumentalness,
            "danceability": year.feature_danceability,
            "energy": year.feature_energy,
            "liveness": year.feature_liveness,
            "loudness": year.feature_loudness,
            "speechiness": year.feature_speechiness

        } for year in features_by_year
    ]
    print("Returning features_by_year_results from by_year() function")
    return features_by_year_results



if __name__ == "__main__":
    app.run(debug=True)
    # we first try to grab the port from the app’s environment, and if not found, it defaults to port 5000
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
