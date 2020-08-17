# app.py Mapping Ideas and Pseudocode

## User Input for ML Model
* There's a listener on the lyrics text field. When it changes, a function in app.py
takes that input:\
__TOKENIZE__ by word (using NLTK) __>__ __NORMALIZE__ by stemming  __=__ __Bag of Words__\
(It could also include other inputs from the user, like the energy of the song, danceability, genre, etc.)

* That Bag of Words gets fed into the ML Model (plus other possible features we might've asked from the user), which will return a binary prediction: __Hit or Not__.

* Function will take that prediction and display the result to the user:
    - If Hit > display this text
    - If Not a Hit > display this other text

## Comparison Charts
* Function takes the __Bag of Words__ from user input and displays it in the same plot as a Bag of Words from the Database, comparing them (2 different wordclouds, or comparing the feeling of most words: mostly positive or negative?). User can select the __Year__ or the __Genre__, which will filter the data and return the Bag of Words for that selection.

## Static Charts
* 