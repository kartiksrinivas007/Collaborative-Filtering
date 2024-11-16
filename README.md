# Recommendation Engine 
This is a movie recommendation engine that has been implemented and deployed as a `Flask` application.
It uses SQLAlchemy on the inside.
There are two classes of algorithms -- one that uses matrix factorization like (SVD) and the other that uses clustering algorithms 
based on various different metrics (euclidean, cosine etc).

The dataset being used for the movies is the [MovieLens Dataset](https://movielens.org/)

### Installation and running-

```console
cd RecomEngine
pip install -r requirements.txt
python app.py
```

Now open the devolopment server
  
### Similarities

You can find similar movies to the ones in the dataset by navigating to the similarites parts and entering a MovieID from the dataset
The clustering algorithm will find the closest neighbours and return them to you

### Predictions
Just enter some ratings for movies by entering the Movie-ID and ratings and then press "Predict Ratings"
This will then run a weighted average of the ratings of all similar movies for every movie and SORT the results,
and present to you the hgihest rated movies
  
 
