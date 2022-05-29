from crypt import methods
from flask import Flask,render_template,jsonify,request,redirect,url_for
import numpy as np
import model as cf


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
rating_list = list(np.zeros(len(cf.final_ratings.index.tolist())))
items = cf.final_ratings.index.tolist()
items_selected =[]
id_selected =[]
count = 0




# class MovieDatabase(db.Model):
#     movie_Id = db.Column(db.Integer(),nullable=False,primary_key=True)
#     movie_number= db.Column(db.Integer(),nullable=False)
#     movie_name= db.Column(db.String(length=50),nullable=False,unique=False)

#     def __repr__(self):
#         return f"{self.movie_name}"




@app.route("/")
def show_home():
    # print(cf.final_ratings.index.tolist())
    return render_template("index.html",items = items)

@app.route("/predictions",methods=["GET","POST"])
def show_predictions():
    show_details = 0
    if request.method == "POST":
        show_details=1
        movieID=request.form["movieID"]
        print(int(movieID))
        recomm,sim_indices,sim_distances = cf.return_similar_movie(int(movieID))
        movieselected = items[int(movieID)]
        print(movieselected)
        print(sim_indices)
        items_closest = []
        distances_closest = []
        id_closest =[]
        for i in range(len(sim_indices)):
            id_closest.append(sim_indices[i])
            items_closest.append(items[sim_indices[i]])
            distances_closest.append(sim_distances[i])
        print(items_closest)
        return render_template("predictions.html",items = items_closest, distances = distances_closest, id = id_closest, movieselected = movieselected, show_details = show_details)
    else:
        items_closest = []
        id_closest= []
        distances_closest=[]
        movieselected=""
        return render_template("predictions.html",items = items_closest, distances = distances_closest, id = id_closest, movieselected = movieselected, show_details = show_details)


@app.route('/ratings',methods=["GET","POST"])
def show_ratings():
    # return "this is the ratings page"
    if request.method == "POST":
        movieID=request.form["movieID"]
        rating=request.form["rating"]
        items_selected.append(items[int(movieID)])
        id_selected.append(int(movieID))
        # display(cf.final_ratings)
        print(movieID)
        print(rating)
        print("items = ",items_selected)
        rating_list[int(movieID)]=float(rating)
        print("value is = ",rating_list[int(movieID)])
        return redirect("/ratings")
    else: 
        return render_template("ratings.html",items= items_selected, rating_list = rating_list,id = id_selected)

@app.route("/clear")
def clear():
    global count
    global rating_list
    global items_selected
    global id_selected
    count = count + 1
    rating_list = list(np.zeros(len(cf.final_ratings.index.tolist())))
    items_selected =[]
    id_selected =[]
    try:
        cf.final_ratings.drop(611,inplace=True,axis = 1)
        cf.final_ratings_copy.drop(611,inplace=True,axis = 1)
        cf.pred_ratings.drop(611,inplace=True,axis = 1)
    except:
        pass
    return redirect("/ratings")

@app.route('/ratingspredictions')
def show_ratingspredictions():
    # return "this is the ratings predictions page"
    print(np.where(np.array(rating_list) > 0))
    print(len(rating_list))
    cf.addUser(rating_list)
    # display(cf.final_ratings)
    cf.CF_engine(611,5,10)
    sorted_movies = cf.print_recommendations(611,10,cf.final_ratings_copy)
    sorted_movie_names = [i[0] for i in sorted_movies]
    sorted_movie_ratings = [i[1] for i in sorted_movies]
    sorted_movie_ids = [i[2] for i in sorted_movies]
    sorted_movie_items = []
    clear()
    return render_template("ratingspredictions.html",items = sorted_movie_names,ratings = sorted_movie_ratings,id = sorted_movie_ids)

@app.route('/euclidean',methods=["GET","POST"])
def show_euclidean():
    show_details = 0
    if request.method == "POST":
        show_details=1
        movieID=request.form["movieID"]
        print(int(movieID))
        recomm,sim_indices,sim_distances = cf.return_similar_movie_euclidean(int(movieID))
        movieselected = items[int(movieID)]
        print(movieselected)
        print(sim_indices)
        items_closest = []
        distances_closest = []
        id_closest =[]
        for i in range(len(sim_indices)):
            id_closest.append(sim_indices[i])
            items_closest.append(items[sim_indices[i]])
            distances_closest.append(sim_distances[i])
        print(items_closest)
        return render_template("euclidean.html",items = items_closest, distances = distances_closest, id = id_closest, movieselected = movieselected, show_details = show_details)
    else:
        items_closest = []
        id_closest= []
        distances_closest=[]
        movieselected=""
        return render_template("euclidean.html",items = items_closest, distances = distances_closest, id = id_closest, movieselected = movieselected, show_details = show_details)

@app.route('/euclidean_predictions')
def show_euclidean_predictions():
    # return "this is the ratings predictions page"
    print(np.where(np.array(rating_list) > 0))
    print(len(rating_list))
    cf.addUser(rating_list)
    # display(cf.final_ratings)
    cf.CF_engine_euclidean(611,5,cf.pred_ratings)
    sorted_movies = cf.print_recommendations(611,10,cf.pred_ratings)
    sorted_movie_names = [i[0] for i in sorted_movies]
    sorted_movie_ratings = [i[1] for i in sorted_movies]
    sorted_movie_ids = [i[2] for i in sorted_movies]
    sorted_movie_items = []
    clear()
    return render_template("euclidean_predictions.html",items = sorted_movie_names,ratings = sorted_movie_ratings,id = sorted_movie_ids)

@app.route('/predict_euclidean',methods = ["GET","POST"])
def show_predict_euclidean():
    if request.method == "POST":
        movieID=request.form["movieID"]
        rating=request.form["rating"]
        items_selected.append(items[int(movieID)])
        id_selected.append(int(movieID))
        # display(cf.final_ratings)
        print(movieID)
        print(rating)
        print("items = ",items_selected)
        rating_list[int(movieID)]=float(rating)
        print("value is = ",rating_list[int(movieID)])
        return redirect("/predict_euclidean")
    else: 
        return render_template("euclidean_ratings.html",items= items_selected, rating_list = rating_list,id = id_selected)

if __name__ == "__main__":
    app.run(debug=True)
