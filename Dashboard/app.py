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
from tensorflow import keras

app = Flask(__name__)

# Set up postgres connection
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgres://postgres:{password}@platinum-rds.cbu3an3ywyth.us-east-2.rds.amazonaws.com/Platinum_Lyrics"

# Create a Flask-SQLAlchemy instance
db = SQLAlchemy(app)

# Declaring global variables so they can be used outside of functions
genre = ""
# Empty features_by_year_results list will be filled with data from database.
features_by_year_results = []
# Set selected_feature so that features_by_year chart has an initial plot to show:
selected_feature = "mode"
# Read csv of word frequencies for successful and unsuccessful song lyrics
top_wordfreq_df = pd.read_csv('word_freq_df.csv')

def lyrics_BoW(lyrics):
    # Creating dictionary to match trained ML model, with words as keys and filled with zeros
    model_dict = dict.fromkeys(word_columns, 0)
    print("Entering lyrics_BoW function.")
    # Tokenizing
    words = nltk.word_tokenize(lyrics)
    print(f"words from lyrics_BoW: {words}")
    # Create an object of class PorterStemmer; set stopwords from NLTK as variable
    porter = PorterStemmer()
    stop_words = stopwords.words('english')

    # Removing stopwords and stemming the remaining ones
    filtered_lyrics = [porter.stem(w) for w in words if not w in stop_words]
    print(f"filtered_lyics from lyrics_BoW: {filtered_lyrics}")
    # Creating frequency of each word and storing in model_dict dictionary
    for word in filtered_lyrics:
        if word in model_dict.keys():
            model_dict[word] += 1
    print(model_dict)
    
    # Creating final DataFrame
    lyrics_df = pd.DataFrame(data=model_dict, index=[0])

    # Creating numpy array from dictionary
    model_array = lyrics_df.to_numpy()
    # model_array = np.array([list(model_dict.values())])
    
    # Load the ML model from the file 
    # cnb_model = joblib.load("NB_model_v1.1.pkl")
    # model = pickle.load(open('NB_model_v1.1.pkl','rb'))
    model = keras.models.load_model("nn_model_v1.1.h5")

    # Feed model_array into ML Model, returning prediction
    # prediction = cnb_model.predict(model_dict)
    prediction = model.predict(model_array)[0][0]
    
    # prediction = "True"
    print(f"Prediction from lyrics_BoW: {prediction}")

    if prediction <= 0.5:
        prediction = "False"
    elif prediction > 0.5:
        prediction = "True"
    else:
        prediction = ""

    return prediction

def plot_features_by_year(feature):
    print("Entering plot_features_by_year() function")
    global features_by_year_results
    # When user changes feature in dropdown, function (from route feature_select) that retrieves
    # user's feature selection runs and updates selected_feature variable
    
    # Call function from route that retrieves values from database
    # Returns list of dictionaries, each dictionary is one element (one row)
    features_by_year_results = by_year()
    
    year = [element["year"] for element in features_by_year_results]
    feature_values = [element[feature] for element in features_by_year_results]
    # print(f"feature_values from plot_features_by_year() function: {feature_values}")

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
    # print(f"plot_bubble_chart()--> features_by_year_results: {features_by_year_results}")

    year = [element["year"] for element in features_by_year_results]
    energy = [element["energy"] for element in features_by_year_results]
    acoustiness = [element["acoustiness"] for element in features_by_year_results]
    loudness = [element["loudness"] for element in features_by_year_results]

    # print(f"Year: {year}")
    # print(f"Energy: {energy}")
    # print(f"Acousiness: {acoustiness}")
    # print(f"Loudness: {loudness}")

    # data = [
    #     go.Scatter(
    #         x = year,
    #         y = loudness,
    #         mode = "markers",
    #         marker = dict(
    #             size = [n*100 for n in energy],
    #             color = acoustiness,
    #             colorscale='Viridis'
    #             )
    #     )
    # ]

    # layout = dict(
    #     title = "Bubble Chart Title",
    #     xaxis = dict(
    #         title_text = "Year"
    #     ),
    #     yaxis = dict(
    #         title_text = "Loudness"
    #     )
    # )

    graph_data = {"year": year, "energy": energy, "acoustiness": acoustiness, "loudness": loudness}
    data_JSON = json.dumps(graph_data)
    # bubble_graph = [data, layout]

    # bubble_chart_JSON = json.dumps(bubble_graph, cls=plotly.utils.PlotlyJSONEncoder)

    # print(f"Return bubble_chart_JSON: {bubble_chart_JSON}")

    # return bubble_chart_JSON
    return data_JSON

def plot_unique_words_bubble():
    global top_wordfreq_df
    # Get word frequencies of top 100 successful and unsuccessful songs
    top100_s = top_wordfreq_df.sort_values('freq in successful', ascending=False).iloc[:100]['words'].to_list()
    top100_u = top_wordfreq_df.sort_values('freq in unsuccessful', ascending=False).iloc[:102]['words'].to_list()
    top100_u.remove("que")
    top100_u.remove("nigga")
    # Get unique words in successful and unsuccessful songs
    top100_s_unique = [word for word in top100_s if word not in top100_u]
    top100_u_unique = [word for word in top100_u if word not in top100_s]
    # Get frequencies of unique words
    s_unique_f = []
    for word in top100_s_unique:
        s_unique_f.append(top_wordfreq_df['freq in successful'][top_wordfreq_df['words']==word].values[0])
    u_unique_f = []
    for word in top100_u_unique:
        u_unique_f.append(top_wordfreq_df['freq in unsuccessful'][top_wordfreq_df['words']==word].values[0])
    # Get size list
    s_size = [f*300 for f in s_unique_f]
    u_size = [f*300 for f in u_unique_f]
    # Add lists to dictionary, then to JSON
    unique = {
        'top100_s_unique': top100_s_unique, 's_unique_f': s_unique_f,
        'top100_u_unique': top100_u_unique, 'u_unique_f': u_unique_f,
        's_size': s_size, 'u_size': u_size
    }
    unique_JSON = json.dumps(unique)
    return unique_JSON

def plot_freq_words_bar():
    global top_wordfreq_df
    # Get word frequencies of successful and unsuccessful songs
    s_freq = top_wordfreq_df.iloc[1:21]['freq in successful'].to_list()
    u_freq = top_wordfreq_df.iloc[1:21]['freq in unsuccessful'].to_list()
    words = top_wordfreq_df.iloc[1:21]['words'].to_list()
    # Define colors for chart
    colors_s = ['lightsteelblue',] * 20
    colors_s[0] = 'steelblue'
    colors_u = ['darksalmon',] * 20
    colors_u[0] = 'indianred'

    freq = {'words': words,'s_freq': s_freq, 'u_freq': u_freq, 'colors_s': colors_s, 'colors_u': colors_u}
    freq_JSON = json.dumps(freq)
    return freq_JSON



class PlatinumFeatures(db.Model):
    __tablename__ = 'platinum_features'

    song_year = db.Column(db.BigInteger(), primary_key=True)
    feature_popularity = db.Column(db.Float())
    target_success = db.Column(db.Float())
    feature_duration = db.Column(db.Float())
    feature_tempo = db.Column(db.Float())
    feature_key = db.Column(db.Float())
    feature_mode = db.Column(db.Float())
    feature_acousticness = db.Column(db.Float())
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

    def __init__(self, song_year):
            self.song_year = song_year


@app.route("/")
def index():
    global selected_feature
    print(f"Selected feature: {selected_feature}")
    features_by_year_JSON = plot_features_by_year(selected_feature)
    # bubble_chart_JSON = plot_bubble_chart()
    data_JSON = plot_bubble_chart()
    freq_JSON = plot_freq_words_bar()
    unique_JSON = plot_unique_words_bubble()
    print("Back to route /")
    # print(f"Return bubble_chart_JSON from route /: {bubble_chart_JSON}")
    # return render_template("index.html", features_by_year_JSON=features_by_year_JSON, bubble_chart_JSON=bubble_chart_JSON)
    # return render_template("index.html")
    return render_template("index.html", features_by_year_JSON=features_by_year_JSON, data_JSON=data_JSON, freq_JSON=freq_JSON, unique_JSON=unique_JSON)


@app.route("/get_lyrics", methods=["GET", "POST"])
def get_lyrics():
    print("Entering /get_lyrics route")
    # Retrieve user input containing lyrics
    lyrics_input = request.args.get('userLyrics', 0, type=str)
    print(f"lyrics_input received in /get_lyrics route: {lyrics_input}")
    # Call lyrics_BoW function to process lyrics and run ML model, returning prediction
    prediction = lyrics_BoW(lyrics_input)
    print(f"Prediction from /get_lyrics route: {prediction}")
    return jsonify(result=prediction)
    

@app.route("/chart_feature_select", methods=["GET", "POST"])
def dropdown_feature():
    print("Entering /chart_feature_select")
    global selected_feature
    # Retrieve user input containing feature selection from the dropdown
    # If the key is missing a default value (here "mode") is returned
    feature_input = request.args.get('userFeatureSelect', 0, type=str)
    print(f"feature_input: {feature_input}")
    # Call plot function to create plot using selected_feature variable
    features_by_year_JSON = plot_features_by_year(feature_input)

    return jsonify(result=features_by_year_JSON)


# @app.route("/wordcloud_genre")
# def get_wordcloud_genre():
#     print("Entering /wordcloud_genre route")
#     # Retrieve user input containing first genre selection, referencing field's "name"
#     first_genre = request.args.get('first-genre', 0, type=str)
#     first = json.dumps(first_genre)
#     # Retrieve user input containing first genre selection, referencing field's "name"
#     second_genre = request.args.get('second-genre', 0, type=str)
#     second = json.dumps(second_genre)


# @app.route("/genre/<userInput>", methods=["GET"])
# def input_genre(userInput=None):
#     global genre
#     response = jsonify(userInput)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     genre = json.dumps(userInput)
#     print(f"Printing genre: {genre}")
#     return response


@app.route("/feature_select/<userInput>", methods=["GET"])
def input_feature(userInput=None):
        
    global selected_feature
    response = jsonify(userInput)
    response.headers.add("Access-Control-Allow-Origin", "*")
    selected_feature = json.dumps(userInput).strip('"')
    
    # Call plot function to create plot using selected_feature variable
    features_by_year_JSON = plot_features_by_year(selected_feature)

    return render_template("index.html", features_by_year_JSON=features_by_year_JSON)
    # return response



@app.route("/features_by_year")
def by_year():
    global features_by_year_results
    # Query database for all values from features_by_year table (defined in Byyear Class)
    # features_by_year = Byyear.query.all()
    features_test = PlatinumFeatures.query.all()

    # features_by_year_results = [
    #     {
    #         "year": year.feature_year,
    #         "mode": year.feature_mode,
    #         "acoustiness": year.feature_acoustiness,
    #         "instrumentalness": year.feature_instrumentalness,
    #         "danceability": year.feature_danceability,
    #         "energy": year.feature_energy,
    #         "liveness": year.feature_liveness,
    #         "loudness": year.feature_loudness,
    #         "speechiness": year.feature_speechiness

    #     } for year in features_by_year
    # ]

    features_testing = [
        {
            "year": year.song_year,
            "mode": year.feature_mode,
            "acoustiness": year.feature_acousticness,
            "instrumentalness": year.feature_instrumentalness,
            "danceability": year.feature_danceability,
            "energy": year.feature_energy,
            "liveness": year.feature_liveness,
            "loudness": year.feature_loudness,
            "speechiness": year.feature_speechiness

        } for year in features_test
    ]

    # return features_by_year_results
    return features_testing



if __name__ == "__main__":
    app.run(debug=True)
    # we first try to grab the port from the app’s environment, and if not found, it defaults to port 5000
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
