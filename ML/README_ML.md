# platinum_lyric_project - v2

## Description of preliminary data preprocessing

Throughout the initial data cleaning process, it was decided to merge the lyrics dataset with the billboard datasets for 
the main model and the Spotify dataset with billboard datasets for an additional second model. Each model is separately trained 
to predict the success of a song based on either lyrics or musical features. It was also decided to use a binary label that 
indicates whether a song would be on the top hit list or not. This binary label, of course, does not put into account for the 
songs' place on the list and the length of the time it stayed on the list. 

It should also be noted that the process started from stemmed bag of words as opposed to raw text. The bag of words was 
filtered to non-English words as well as words with less than 3 characters (with the exception of words that could be 
meaningful in sentiment analysis), special characters and numbers. 


##  Description of preliminary feature engineering and preliminary feature selection, including decision making process 

As mentioned before, we decided not to merge the Spotify and Lyrics datasets for two reasons. One, to keep the number of features more 
manageable (there are over 1500 lyrics features before merging) and also to avoid shrinking the dataset by merging. In the first round of model 
design, we decided to keep all word counts as features. 

However, to optimize the model and reduce the noisy features fed into the model (after the first round), we experimented with a few feature engineering models, such as Backward Elimination, PCA and LASSO Regularizartion. While the first two did not exaclty work for our dataset, LASSO seemed to be a good fit and it reduced our features to 579 (vs. 1553 original features). We felt confident about LASSO as a feature engineering method, since our primary goal here is prediction and not necessarily findng the "most important features". LASSO also seems to protect the model against overfitting compared to other feature selection methods (see ref. #5).

##  Description of how data was split into training and testing sets 

After splitting the dataset into x and y using sklearn train_test_split, stratified by y , we also resampled them, because we have an
imbalanced dataset. 

Lastly, we scaled the features using StandardScaler. This allowed us to not only have scaled feature values, but also to avoid having 
classes with 0 probability as Naive Bayes Classification algorithms do not perform well with classes of 0 probability.

##  Explanation of model choice, including limitations and benefits

- Decision-making Process

In the first round of training, we chose the Naive Bayes models (The Complement and GaussianNB algorithms) for the following reasons:

  -- labeled vs unlabeled: we, of course, are dealing with labeled data. That in itself limited our options to certain classification models.
  -- target prediction type: our label is a binary value.
  -- small sample size: we have a relatively small sample size (less than 100k) and Naive Bayes model seem 
  to be a good fit for smaller samples.
  -- data type: Naive Bayes models are considered to work well with text data, which is the data type we have.
  -- prediction time: our interactive dashboard takes input from user in form of text and returns prediction on how the song 
  would do in the market. A fast (real-time) prediction model like Naive Bayes seems to be the perfect fit for this requirement. 
  -- noisy data: we have a massive feature set and that means there is potentially a lot of noisy features in there. Naive Bayes 
  handles noisy features pretty well.
  -- The Complement Naive Bayes Classifier - this algorithm is particularly suited for imbalanced data sets.
  -- The GaussianNB Naive Bayes Classifier - this algorithm is the most common Naive Bayes algorithm which 
  assumes a normal distribution in classes.

  However, there are limitations to our models:

  -- The Naive Bayes models assume features are independent of each other and do not learn from relationships between features. 
  -- These models could be harder to interpret.

  - Additional Model: Deep Learning Model

Lastly, we experimented with an ANN model to compare its accuracy with our other models. We anticipated the Keras ANN model to be a good fit for our dataset because we have a very complex and wide feature set. However this model has its own limitations:

  -- It is even harder to interpret.
  -- It doesn't make predictions as quickly (and so far, we have not figured out how we could save/ pickle it)
  -- It is prone to overfit.

- Results and Optimizations: 

The results of the first round of training were not exactly encouraging. The accuracy scores for our models were as followed:

 -- ComplementNB Naive Bayes - 0.64
 -- GaussianNB Naive Bayes - 0.48
 -- Keras ANN (50 epochs) - 0.91 on train and 0.76 on test data. With a rather high loss number (1.8), we concluded that this model was overfitting. 

So we got to work. In the second round of training, we fed a reduced feature set (using LASSO Regularization method) to our models. We also reduced a hidden layer and 30 epochs from the Keras ANN model to avoid overfitting. The accuracy scores of the second round of training were as followed:

 -- ComplementNB Naive Bayes - 0.71
 -- GaussianNB Naive Bayes - 0.48
 -- Keras ANN (50 epochs) - 0.88 on train and 0.73 on test data. Our loss on this model also dropped significantly to 0.73 on test and 0.26 on train data. 

While the optimization results were encouraging, we did not stop there. We decided to experiment with an ensemble model. Ensemble models are commonly used to boost predictive accuracy by combining the predictions of multiple machine learning models. We chose Random Forest Classifier because it is a robust model that is less impacted by noisy features. However, it is a rather complex model that requires more computational power and longer training time. Depending on the number of estimators, this model could also get significantly larger when trained which means saving it to use for predictions on the dashboard could potentially be problematic. Since Random Forest Classifiers could handle a lot of features and potentially some noisy one, we decide to train it first using all our features, with 500 estimators. The accuracy scores were as followed:

  -- Random Forest Classifier - 0.78

This looked quite promising. In addition to that, we were able to get a list of important features which would allow us to filter through our features if necessary, in later revisions. However, this ended up being so big that saving and using it to make predictions was essentially impossible.



  
## References

- 1)https://scikit-learn.org/stable/modules/naive_bayes.html
- 2)http://blog.echen.me/2011/04/27/choosing-a-machine-learning-classifier/
- 3)https://www.dataschool.io/comparing-supervised-learning-algorithms/
- 4)https://www.machinelearningplus.com/predictive-modeling/how-naive-bayes-algorithm-works-with-example-and-full-code/
- 5)https://stats.stackexchange.com/questions/367155/why-lasso-for-feature-selection
- 6)https://blogs.sas.com/content/subconsciousmusings/2017/05/18/stacked-ensemble-models-win-data-science-competitions/
- 7)https://theprofessionalspoint.blogspot.com/2019/02/advantages-and-disadvantages-of-random.html


