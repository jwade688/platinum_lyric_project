# platinum_lyric_project

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
design, we decided to keep all word counts as features. Even though the model currently has a decent accuracy score, we understand that it 
is still fed some potentially noisy features. So our plan is to use Backward Elimination method to narrow down the features into a smaller 
but more significant set.


##  Description of how data was split into training and testing sets 

After splitting the dataset into x and y using sklearn train_test_split, stratified by y , we also resampled them, because we have an
imbalanced dataset. 

Lastly, we scaled the features using MinMaxScaler. This allowed us to not only have scaled feature values, but also to avoid having 
classes with 0 probability as Naive Bayes Classification algorithms do not perform well with classes of 0 probability.

##  Explanation of model choice, including limitations and benefits

- Decision-making Process

We chose the Naive Bayes models for the following reasons:

  -- labeled vs unlabeled: we, of course, are dealing with labeled data. That in itself limited our options to certain classification models.
  -- target prediction type: our label is a binary value.
  -- small sample size: we have a relatively small sample size (less than 100k) and Naive Bayes model seem 
  to be a good fit for smaller samples.
  -- data type: Naive Bayes models are considered to work well with text data, which is the data type we have.
  -- prediction time: our interactive dashboard takes input from user in form of text and returns prediction on how the song 
  would do in the market. A fast (real-time) prediction model like Naive Bayes seems to be the perfect fit for this requirement. 
  -- noisy data: we have a massive feature set and that means there is potentially a lot of noisy features in there. Naive Bayes 
  handles noisy features pretty well.

  However, there are limitations to our models:

  -- The Naive Bayes models assume features are independent of each other and do not learn from relationships between features. 
  -- These models could be harder to interpret.

- Algorithms

  In the first trial the two algorithms listed below are being trained and tested:
  
  -- The Complement Naive Bayes Classifier - this algorithm is particularly suited for imbalanced data sets
  
  -- The GaussianNB Naive Bayes Classifier - this algorithm is the most common Naive Bayes algorithm which 
  assumes a normal distribution in classes. 
  
## References

- https://scikit-learn.org/stable/modules/naive_bayes.html
- http://blog.echen.me/2011/04/27/choosing-a-machine-learning-classifier/
- https://www.dataschool.io/comparing-supervised-learning-algorithms/
- https://www.machinelearningplus.com/predictive-modeling/how-naive-bayes-algorithm-works-with-example-and-full-code/

