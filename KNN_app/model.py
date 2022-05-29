import pandas as pd 
import numpy as np
from sklearn.neighbors import NearestNeighbors

#import the dataset!
ratings = pd.read_csv('ratings.csv', usecols=['userId','movieId','rating'])
movies = pd.read_csv('movies.csv',usecols=['movieId','title','genres'])

#merge the two datasets to obtain movies and ratings onto the same pandas dataframe !
merged_ratings = pd.merge(ratings, movies, how='inner', on='movieId')
final_ratings = merged_ratings.pivot_table(index = 'title',columns='userId',values='rating',fill_value=0)


#this copy will hold the predicted ratings in later stages !
final_ratings_copy = final_ratings.copy()
pred_ratings= final_ratings.copy()

#The viewer of the page needs to be added !
def addUser(rating_list):
    length = len(final_ratings.columns.tolist())
    final_ratings[(length+1)] = rating_list
    final_ratings_copy[(length+1)] = rating_list
    pred_ratings[(length+1)] = rating_list

 # a function to calculated the pariwise distances between EVERY movie and every other movie , we use Scikit -KNN to calculate the distances snce it uses HIGHLY
def fit_no_params(k_int):
    k = int(k_int)
    knn = NearestNeighbors(metric = 'cosine', algorithm='brute')
    knn.fit(final_ratings.values)
    differences,movie_indices = distances, indices = knn.kneighbors(final_ratings.values, n_neighbors=k,return_distance=True)
    return differences,movie_indices


def fit_no_params_euclidean(k_int):
    k = int(k_int)
    knn = NearestNeighbors(metric = "minkowski",p=2,algorithm='brute')
    knn.fit(final_ratings.values)
    differences,movie_indices = knn.kneighbors(final_ratings.values, n_neighbors=k,return_distance=True)
    print("The differences array is = ",differences)
    return differences,movie_indices


def print_recommendations(user,num_recommended_movies,final_ratings_copy):
  print('The list of the Movies {} Has Watched \n'.format(user))
  

  for m in final_ratings[final_ratings[user] > 0][user].index.tolist():
    print(m)
  
  print('\n')

  recommended_movies = []

  for m in final_ratings[final_ratings[user] == 0].index.tolist():
    index_df = final_ratings.index.tolist().index(m)
    predicted_rating = final_ratings_copy.iloc[index_df, final_ratings_copy.columns.tolist().index(user)]
    recommended_movies.append((m, predicted_rating,index_df))

  sorted_rm = sorted(recommended_movies, key=lambda x:x[1], reverse=True)
  
  print('The list of the Recommended Movies \n')
  rank = 1
  for recommended_movie in sorted_rm[:num_recommended_movies]:
    
    print('{}: {} - predicted rating:{}'.format(rank, recommended_movie[0], recommended_movie[1]))
    rank = rank + 1

  return sorted_rm[:num_recommended_movies]  

def CF_engine(userID,k,numrec):
    knn_obj = NearestNeighbors(metric = 'cosine',algorithm='brute')
    knn_obj.fit(final_ratings.values)
    differences,movie_indices = knn_obj.kneighbors(final_ratings.values,n_neighbors=k)
    print(final_ratings)
    user_index=final_ratings.columns.tolist().index(userID)
    

    for movie,title in list(enumerate(final_ratings_copy.index)):
        if(final_ratings_copy.iloc[movie,user_index] == 0):
            similar_movie_indices = movie_indices[movie].tolist()
            similar_movie_distances = differences[movie].tolist()

            if movie in similar_movie_indices:
                movieId = similar_movie_indices.index(movie)
                similar_movie_indices.remove(movie)
                similar_movie_distances.pop(movieId) 

            # However, if the percentage of ratings in the dataset is very low, there are too many 0s in the dataset. 
            # Some movies have all 0 ratings and the movies with all 0s are considered the same movies by NearestNeighbors(). 
            # Then,even the movie itself cannot be included in the indices. 
            # For example, indices[3] = [2 4 7] is possible if movie_2, movie_3, movie_4, and movie_7 have all 0s for their ratings.
            # In that case, we take off the farthest movie in the list. Therefore, 7 is taken off from the list, then indices[3] == [2 4].
            else:
                similar_movie_indices = similar_movie_indices[:k-1]
                similar_movie_distances = similar_movie_distances[:k-1]
                
            # movie_similarty = 1 - movie_distance    
            closeness = [1-x for x in similar_movie_distances]
            closeness_copy = closeness.copy()
            weighted_sum = 0

        # for each similar movie
            for s in range(0, len(closeness)):
            
            # check if the rating of a similar movie is zero
                if final_ratings_copy.iloc[similar_movie_indices[s], user_index] == 0:
                    # if the rating is zero, ignore the rating and the similarity in calculating the predicted rating
                    if len(closeness_copy) == (k - 1):
                        closeness_copy.pop(s)
                    
                    else:
                        closeness_copy.pop(s-(len(closeness)-len(closeness_copy)))

                # if the rating is not zero, use the rating and similarity in the calculation
                else:
                    weighted_sum = weighted_sum + closeness[s]*final_ratings_copy.iloc[similar_movie_indices[s],user_index]

                # check if the number of the ratings with non-zero is positive
                if len(closeness_copy) > 0:
                
                # check if the sum of the ratings of the similar movies is positive.
                    if sum(closeness_copy) > 0:
                        pred_rating = weighted_sum/sum(closeness_copy)

                    # Even if there are some movies for which the ratings are positive, some movies have zero similarity even though they are selected as similar movies.
                    # in this case, the predicted rating becomes zero as well  
                    else:
                        pred_rating = 0

                # if all the ratings of the similar movies are zero, then predicted rating should be zero
                else:
                    pred_rating = 0

    # place the predicted rating into the copy of the original dataset
            final_ratings_copy.iloc[movie,user_index] = pred_rating
    #print_recommendations(userID,numrec)

def return_similar_movie(movie_index):
    # movie_index = final_ratings.index.tolist().index(title)
    differences,movie_indices = fit_no_params(5)
    similar_movie_indices = movie_indices[movie_index].tolist()
    similar_movie_distances = differences[movie_index].tolist()
    k=""
    # movie_pos = similar_movie_indices.index(movie_index) # find the index of the movie itself , since it is the closest neighbour this will always be 0 
    # similar_movie_indices.remove(movie_index) # remove the movie itself in indices
    # similar_movie_distances.pop(movie_pos) # remove the movie itself in distances
    #There are tremendously special cases where nearly all the ratings tend to zero, i.e. nobody has rated these movies. this try block handles these special cases
    try:
        movie_pos = similar_movie_indices.index(movie_index) # find the index of the movie itself , since it is the closest neighbour this will always be 0 
        similar_movie_indices.remove(movie_index) # remove the movie itself in indices
        similar_movie_distances.pop(movie_pos)
    except:
        pass


    print("The Movies that are quite Similar to " , final_ratings.index[movie_index])
    for i in similar_movie_indices:
        movie_title = final_ratings.index[i]
        print(str(i+1) + ": " + movie_title) 
        k = k + str(i+1) + ": " + movie_title+ "<br>"
    return k,similar_movie_indices,similar_movie_distances

def return_similar_movie_euclidean(movie_index):
    differences,movie_indices = fit_no_params_euclidean(5)
    similar_movie_indices = movie_indices[movie_index].tolist()
    similar_movie_distances = differences[movie_index].tolist()
    k=""
    # movie_pos = similar_movie_indices.index(movie_index) # find the index of the movie itself , since it is the closest neighbour this will always be 0 
    # similar_movie_indices.remove(movie_index) # remove the movie itself in indices
    # similar_movie_distances.pop(movie_pos) # remove the movie itself in distances
    #There are tremendously special cases where nearly all the ratings tend to zero, i.e. nobody has rated these movies. this try block handles these special cases
    try:
        movie_pos = similar_movie_indices.index(movie_index) # find the index of the movie itself , since it is the closest neighbour this will always be 0 
        similar_movie_indices.remove(movie_index) # remove the movie itself in indices
        similar_movie_distances.pop(movie_pos)
    except:
        pass


    print("The Movies that are quite Similar to " , final_ratings.index[movie_index])
    for i in similar_movie_indices:
        movie_title = final_ratings.index[i]
        print(str(i+1) + ": " + movie_title) 
        k = k + str(i+1) + ": " + movie_title+ "<br>"
    return k,similar_movie_indices,similar_movie_distances

def CF_engine_euclidean(userID,k,final_ratings_copy):
    knn_obj = NearestNeighbors(metric = 'euclidean',algorithm='brute')
    knn_obj.fit(final_ratings.values)
    differences,movie_indices = knn_obj.kneighbors(final_ratings.values,n_neighbors=k)
    print(final_ratings)
    user_index=final_ratings.columns.tolist().index(userID)
    

    for movie,title in list(enumerate(final_ratings_copy.index)):
        if(final_ratings_copy.iloc[movie,user_index] == 0):
            similar_movie_indices = movie_indices[movie].tolist()
            similar_movie_distances = differences[movie].tolist()

            if movie in similar_movie_indices:
                movieId = similar_movie_indices.index(movie)
                similar_movie_indices.remove(movie)
                similar_movie_distances.pop(movieId) 

            # However, if the percentage of ratings in the dataset is very low, there are too many 0s in the dataset. 
            # Some movies have all 0 ratings and the movies with all 0s are considered the same movies by NearestNeighbors(). 
            # Then,even the movie itself cannot be included in the indices. 
            # For example, indices[3] = [2 4 7] is possible if movie_2, movie_3, movie_4, and movie_7 have all 0s for their ratings.
            # In that case, we take off the farthest movie in the list. Therefore, 7 is taken off from the list, then indices[3] == [2 4].
            else:
                similar_movie_indices = similar_movie_indices[:k-1]
                similar_movie_distances = similar_movie_distances[:k-1]
                
            # movie_similarty = 1 - movie_distance    
            closeness = [(1/(1+x)) for x in similar_movie_distances]
            closeness_copy = closeness.copy()
            weighted_sum = 0

        # for each similar movie
            for s in range(0, len(closeness)):
            
            # check if the rating of a similar movie is zero
                if final_ratings_copy.iloc[similar_movie_indices[s], user_index] == 0:
                    # if the rating is zero, ignore the rating and the similarity in calculating the predicted rating
                    if len(closeness_copy) == (k - 1):
                        closeness_copy.pop(s)
                    
                    else:
                        closeness_copy.pop(s-(len(closeness)-len(closeness_copy)))

                # if the rating is not zero, use the rating and similarity in the calculation
                else:
                    weighted_sum = weighted_sum + closeness[s]*final_ratings_copy.iloc[similar_movie_indices[s],user_index]

                # check if the number of the ratings with non-zero is positive
                if len(closeness_copy) > 0:
                
                # check if the sum of the ratings of the similar movies is positive.
                    if sum(closeness_copy) > 0:
                        pred_rating = weighted_sum/sum(closeness_copy)

                    # Even if there are some movies for which the ratings are positive, some movies have zero similarity even though they are selected as similar movies.
                    # in this case, the predicted rating becomes zero as well  
                    else:
                        pred_rating = 0

                # if all the ratings of the similar movies are zero, then predicted rating should be zero
                else:
                    pred_rating = 0

    # place the predicted rating into the copy of the original dataset
            final_ratings_copy.iloc[movie,user_index] = pred_rating
    #print_recommendations(userID,numrec)