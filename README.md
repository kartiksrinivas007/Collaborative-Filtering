# Collaborative Filtering
This CF engine has 2 main algorithms, one of them , the KNN has been implemented as a Flask application and the second is just a jupyter notebook file

## KNN
### Installation and running-

```console
cd KNN_app
conda activate virtualEnv
pip install -r requirements.txt
python3 app.py
```

Now open the devolopment server
  
### Similarities
You can find similar movies to the ones in the dataset by navigating to the Similarites parts and entering a MovieID
The KNN algorithm will find the closest neighbours and return them to you
### Predictions
  Just enter some ratings for movies by entering the MOvieID and ratings and then press "Predict Ratings"
  This will then run a weighted average of the ratings of all similar movies for every movie and SORT the results,
  and present to you the hgihest rated movies
  
 *Zeros are possible, since this represent movies that have barely been rated by anyone !*
  
 ## SVD
 ---
 
## Installation and running-
  Navigate to SVD algorithms and open the notebook file
  To run simply install vscode support for JUpyter under extensions, or  just upload the file to google colab
  
### Successfull Implementation (SVD_successful.ipynb) 
  I have created my own ratings matrix in SVD_succesfull and then used a MACHINE LEARNING model( built form scratch) to predict the ratings
  of a particular movie this uses CONTENT-BASED FILTERING, and a Mean squared Error loss along with Matrix decomposition(Simple Decomposition, not SVD)
  to predict the ratings of every user and the sensitivity of a particular user to a particular genre (theta)
### Failed Implementation(SVD_failed.ipynb)
  I tried to run this on the Movie Lens Dataset But the loss grows too large ! and it takes too much time to train !
  I didn't get enough to optimize the gradient descent!
  the code is more or less correct however.
  
 
