# platinum_lyric_project

## Description of preliminary data preprocessing

<<<<<<< HEAD
Throughout the intital data cleaning process, it was decided to merge the lyrics dataset with the billboard datasets for the main model and the Spotify dataset with billboard datasets for an additional second model. Each model is separately trained to predict the succuess of a song based on either lyrics or musical features. It was also decided to use a binary label that indicates whether a song would be on the top hit list or not. This binary label, of course, does not put into account for the songs' place on the list and the length of the time it stayed on the list. 

It should also be noted that the process started from stemmed bag of words as opposed to raw text. The bag of words was filtered to non-English words as well as words with less than 3 characters (with the exception of words that could be meaningful in sentiment analysis), special characters and numbers. 

- multiple datasets - multiple merges (which combination works best?)
- choosing to use binary values (hit or miss) as success measure
- starting from stemmed bag of words
- losing word features like non-English, special characters, numbers, small words, etc


##  Description of preliminary feature engineering and preliminary feature selection, including decision making process 

- choosing to separate the features and design two models for each set for a healthy dataset size 
- in the first round of model design, keeping the values to a simple count of each word. could try more complex calculations after the first trial
- keeping the year as a feature and encoding it so it is not treated as numerical values
- changing all 0 values to 1 to fit Naive Bayes Classification

=======
- multiple datasets - multiple merges (which combination works best?)
- choosing to use binary values (hit or miss) as success measure
- starting from stemmed bag of words
- losing word features like non-English, special characters, numbers, small words, etc


##  Description of preliminary feature engineering and preliminary feature selection, including decision making process 

- choosing to separate the features and design two models for each set for a healthy dataset size 
- in the first round of model design, keeping the values to a simple count of each word. could try more complex calculations after the first trial
- keeping the year as a feature and encoding it so it is not treated as numerical values
- changing all 0 values to 1 to fit Naive Bayes Classification

>>>>>>> bd51085ce9c88d499cee9b268553fc3610f821c4
##  Description of how data was split into training and testing sets 
- splitting the dataframe ready for the model into X and y where yxs is the 'target_success' column and X is all other columns 
- using train_test_split from sklearn module
- if necessary, oversampling the "miss songs" class, as there seems to be an imbalance between two classes
##  Explanation of model choice, including limitations and benefits

- Decision-making Process

  -- sample size: we have a relatively small sample size, less than 100k
  -- target prediction type: categorical/binary
  -- labeled vs unlabeled: labeled data
  -- data type: text data
  
- The Model - Naive Bayes
  -- benefits:
<<<<<<< HEAD
    --- good for sentiment prediction (?)
=======
    --- good for sentiment prediction
>>>>>>> bd51085ce9c88d499cee9b268553fc3610f821c4
    --- can make predictions in real time - fast prediction that is requires to respond to user's requests
    --- could work with less training data 
    --- handles lots of irrelevant (noisy) features 
  -- limitations: 
    --- assumes features are independent of each other which means it can't make sense of potential relations between features
    --- harder interpretation of results
- Algorithms

  In the first trial the two algorithms listed below are being trained and tested:
  
  -- The Complement Naive Bayes Classifier - this algorithm is particularly suited for imbalanced data sets
  
  -- The multinomial Naive Bayes Classifier - this algorithm is suitable for classifications with discrete features, such as word counts for text classification

## References

- https://scikit-learn.org/stable/modules/naive_bayes.html
- http://blog.echen.me/2011/04/27/choosing-a-machine-learning-classifier/
- https://www.dataschool.io/comparing-supervised-learning-algorithms/
- https://www.machinelearningplus.com/predictive-modeling/how-naive-bayes-algorithm-works-with-example-and-full-code/
