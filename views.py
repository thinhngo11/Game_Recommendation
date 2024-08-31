from flask import Flask, Blueprint, redirect, url_for, render_template, request, redirect, session
import pandas as pd
import numpy as np
from content_based import content_based_recommend
# from SVD import SVD, hybrid
from models import User, Rating
from init import db
import random
import csv
import matplotlib 
#import seaborn as sns

views = Blueprint('views', __name__)

""" to create training and test datasets from rating.csv 
df_rating = pd.read_csv("rating.csv")
user_rating = pd.read_csv("user_rating.csv")
# user_rating.columns = ["ID", "User_ID","Game_id", "Game_name","Rating"]

full_df_rating = pd.concat([user_rating[["User_ID","Game_id","Game_name","Rating"]],df_rating[["User_ID","Game_id","Game_name","Rating"]]])
len_df =len(full_df_rating)
train_df_rating = full_df_rating.take(np.random.permutation(len_df)[:int(0.8 * len_df)]) #80% of rating.csv
test_df_rating = pd.concat([full_df_rating,train_df_rating]).drop_duplicates(keep=False) #the remaining 20%

train_df_rating.to_csv("train_df_rating.csv")
test_df_rating.to_csv("test_df_rating.csv")
accuracy = 0.2%
quit()
"""
""" to create training and test datasets from rating.csv 
retain users with at least 5 games
retain games with at least 5 users 

df_rating = pd.read_csv("rating.csv")
user_rating = pd.read_csv("user_rating.csv")
# user_rating.columns = ["ID", "User_ID","Game_id", "Game_name","Rating"]

full_df_rating = pd.concat([user_rating[["User_ID","Game_id","Game_name","Rating"]],df_rating[["User_ID","Game_id","Game_name","Rating"]]])

sorted_df = full_df_rating.sort_values(by= "User_ID", ascending = False)
print(f'len_sorted_df: {len(sorted_df)}')
df_test = dict()

for index, row in sorted_df.iterrows():
    #print(row["User_ID"])
    if row["User_ID"] not in df_test.keys():
        df_test[row["User_ID"]] = []
        #print("creating")
    df_test[row["User_ID"]].append(row["Game_id"])
    #print(df_test[row["User_ID"]])
print(f'len_df_test: {len(df_test)}')

keep_users = []
for user, games in df_test.items():
    if len(games) >= 50:
        keep_users.append(user)
print(f'len_keep_user {len(keep_users)}')

mask = []
for index, row in sorted_df.iterrows():
    #print(f'index: {index}')
    #print(row["User_ID"])
    if row["User_ID"] not in keep_users:
        mask.append(False)
    else:
        mask.append(True)
print(len(mask))

df_rating = sorted_df[mask]

#retain games with at least 10 users 
sorted_df = df_rating.sort_values(by= "Game_id", ascending = False)
print(f'len_sorted_df: {len(sorted_df)}')
df_test = dict()

for index, row in sorted_df.iterrows():
    #print(row["User_ID"])
    if row["Game_id"] not in df_test.keys():
        df_test[row["Game_id"]] = []
        #print("creating")
    df_test[row["Game_id"]].append(row["User_ID"])
    #print(df_test[row["User_ID"]])
print(f'len_df_test: {len(df_test)}')

keep_games = []
for game, users in df_test.items():
    if len(users) >= 50:
        keep_games.append(game)
print(f'len_keep_game {len(keep_games)}')

mask = []
for index, row in sorted_df.iterrows():
    #print(f'index: {index}')
    #print(row["User_ID"])
    if row["Game_id"] not in keep_games:
        mask.append(False)
    else:
        mask.append(True)
print(len(mask))

df_rating = sorted_df[mask]

len_df = len(df_rating)
print(f'len_df {len_df}')

train_df_rating = df_rating.take(np.random.permutation(len_df)[:int(0.8 * len_df)]) #80% of rating.csv
test_df_rating = pd.concat([df_rating,train_df_rating]).drop_duplicates(keep=False) #the remaining 20%
test_df_rating1 = test_df_rating.take(np.random.permutation(len(test_df_rating))) #randomize it
train_df_rating.to_csv("train_df_rating.csv")
test_df_rating1.to_csv("test_df_rating.csv")

quit()

"""
from SVD import SVD
"""
full_df_rating = pd.read_csv("rating.csv")
#user_rating = pd.read_csv("user_rating.csv")
# user_rating.columns = ["ID", "User_ID","Game_id", "Game_name","Rating"]

#full_df_rating = pd.concat([user_rating[["User_ID","Game_name","Rating"]],df_rating[["User_ID","Game_name","Rating"]]])
print(full_df_rating.shape[0])
user_df_rating = pd.DataFrame(columns = ["User_ID","Game_name","Rating"])

grouped = full_df_rating.groupby(["User_ID"])
#print(type(grouped))
#print(grouped.count())
for User_ID, group in grouped:
    #print(type(group))
    #print(group)
    
    if group.shape[0] >= 6:
        #print(group)
        user_df_rating = pd.concat([user_df_rating,group], axis=1, copy=False)
        print(user_df_rating.shape[0])
        

user_df_rating.to_csv("user_df_rating.csv")
quit()
clean_df_rating = pd.DataFrame()
grouped = user_df_rating.groupby(["Game_name"])
for game, group in grouped:
    if group.size == 6:
        clean_df_rating.join(group)

clean_df_rating.to_csv("user_df.rating.csv")
quit()
"""
df = pd.read_csv("steam_api.csv")
df["Rating"] = ((df["Rating"].fillna(0)).astype(int)).astype(str)

df_train = pd.read_csv("train_df_rating.csv")

# user game candidate pool
max_candidates = 1000
df_cand = df.take(np.random.permutation(len(df))[:max_candidates]) 

df = pd.read_csv("test_df_rating.csv")
df["Rating"] = ((df["Rating"].fillna(0)).astype(int)).astype(str)

# test user game candidate pool
max_candidates = 1000 if len(df) > 1000 else len(df)
test_df = df.take(np.random.permutation(len(df))[:max_candidates]) 
sorted_test_df = test_df.sort_values(by= "User_ID", ascending = False)

#reformat test_df into dictionary keys = users and values = list of games
#df_test = {"User_ID":[]}
df_test = dict()

for index, row in sorted_test_df.iterrows():
    #print(row["User_ID"])
    if (row["User_ID"] in df_train.values):
        if row["User_ID"] not in df_test.keys():
            df_test[row["User_ID"]] = []
            #print("creating")
        df_test[row["User_ID"]].append(row["Game_id"])
        #print(df_test[row["User_ID"]])
print(len(df_test))

accuracy = []
for user, games in df_test.items():
    #print(f'user: {user} games: {games}')
    recommended_games = SVD(user, 20, 100, df_cand)['Game_index']
    #print(type(recommended_games))
    
    #print(f'recommended_games: {recommended_games}, user: {user}')
    for i in games:
        if i in recommended_games:
            accuracy.append(100)
        else:
            accuracy.append(0)
print(len(accuracy))
print(accuracy)
print(f'recommendation accuracy average = {sum(accuracy)/len(accuracy)} %')
#print(df_test)
quit()
# Home Page
@views.route("/", methods = ['GET','POST'])
def index():
    print("index")
    if session.get('logged_in'):
        print("session")
        with open(r'user_rating.csv','w') as f:
            header = ["ID", "User_ID","Game_id", "Game_name","Rating"]
            users = db.session.query(Rating.id, Rating.user_id, Rating.game_id,Rating.game_name,Rating.rating)
            #print(type(users))
            #print(len(users))
            csv_out = csv.writer(f)
            csv_out.writerow(header)
            #print("header")
            for user in users:
                csv_out.writerow(user)
                #print("user")
        #print("user done")
        #quit()
            
        from SVD import SVD
        user_name = session.get("username")
        top_Rating = df.sort_values(by = "Rating", ascending = False)[:100]
        top_forever = df.sort_values(by = "average_forever", ascending = False)[:100]
        top_positive = df.sort_values(by=['positive','negative'], ascending = False)[:100]
        user_recommend = df.iloc[SVD(session.get('user_id'),20, 100,top_Rating)['Game_index']]
        # if request.method =='POST':
        #     from SVD import SVD
        #     print('Return the HomePage')
        #     user_recommend1 = df.iloc[SVD(session.get('user_id'),20, 100,top_Rating)['Game_index']]
        #     return render_template("home.html", top_Rating= top_Rating, user_recommend = user_recommend1, top_forever=top_forever, top_positive= top_positive, user_name = user_name)
        # # list2 = random.sample(range(19233), 20)
        # else:
        return render_template("home.html", top_Rating= top_Rating, user_recommend = user_recommend, top_forever=top_forever, top_positive= top_positive, user_name = user_name)
    else:
        return render_template("index.html")

#Register Page
@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('views.login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')

#Login Page
@views.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'GET':
        return render_template('login.html')
     else:
        print("login")
        session['logged_in'] = True
        #session["user_id"] = data.id
        #session["username"] = data.username
        return redirect(url_for('views.index'))

        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            session["user_id"] = data.id
            session["username"] = data.username
            return redirect(url_for('views.index'))
        return render_template('index.html', message="Incorrect Details")

#Logout 
@views.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('views.index'))


#Detail Page
@views.route("/detail/<game_id>",methods=['GET', 'POST'])
def detail(game_id):
    from SVD import hybrid
    user_id = session.get('user_id')
    game_index = int(df[df["Game_id"]==int(game_id)].index[0])
    # list2 = random.sample(range(19233), 20)
    game_detail = df.loc[df["Game_id"]==int(game_id)].squeeze()
    game_name = str(game_detail["Game_name"])
    list_game_recommend = content_based_recommend(game_index, 20)
    list_game_hybrid = hybrid(user_id, game_index, game_name, 30, 20)['Game_index']

    if request.method == "POST":
        rating = request.form.get('rating')

        data = Rating.query.filter_by(user_id=user_id, game_id=game_id, game_name=game_name).first()
        if data is not None:
            data.rating = rating
            # Rating.query.filter_by(username='admin').update(dict(rating=rating))
            db.session.commit()
        else:
            db.session.add(Rating(user_id=user_id, game_id=game_id, game_name = game_name, rating = rating))
            db.session.commit()
        # print("Import done")

    return render_template("detail.html", game_detail=game_detail, df = df, list_game_recommend=list_game_recommend, list_game_hybrid=list_game_hybrid)