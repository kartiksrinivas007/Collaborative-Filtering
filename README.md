# Collaborative Filtering
This CF engine has been implemented as a `Flask` application

## KNN
### Installation and running-

```console
pip install -r requirements.txt
python3 app.py
```

Now open the devolopment server
  
### Similarities
You can find similar movies to the ones in the dataset by navigating to the Similarites parts and entering a MovieID
The KNN algorithm will find the closest neighbours and return them to you
### Predictions
  Just enter some ratings for movies by entering the Movie-ID and ratings and then press "Predict Ratings"
  This will then run a weighted average of the ratings of all similar movies for every movie and SORT the results,
  and present to you the hgihest rated movies
  
 >Zeros are possible, since this represent movies that have barely been rated by anyone !
 
