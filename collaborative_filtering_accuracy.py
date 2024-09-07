import pandas as pd
import numpy as np
import random
import csv

""" ACCURACY for minimum curation of 50: 0% """ 
"""
CURRENT COLLABORATIVE FILTERING TECHNIQUE: FOR EACH USER (USER-BASED): 
SELECT 20 GAMES OF HIGHEST EST, USING THE SVD MODEL TRAINED ON THE RATING.CSV, FROM 100 LINES (USER-GAMES) OF TOP RATINGS IN STEAM_API.CSV FROM NEW GAMES
1.	TAKING 100 GAMES OF TOP RATINGS IN STEAM_API.CSV ?!?! MAY NOT BE REPRESENTATIVE OF THE WORLD OF GAMES; RANDOM PERCENTAGE OR ALL
2.	APPLYING SVD TO EACH GAME: ESTIMATE EST 
A.	USING SVD MODEL TRAINED ON THE RATING.CSV
B.	INPUTS: USER_ID AND GAME NAME; OUTPUT EST FOR EACH GAME
3.	SELECT 20 GAMES OF HIGHEST EST 

TO COMPUTE RECOMMENDATION ACCURACY:
1.	CREATE THE TEST DATASET = 20% OF RATING.CSV; RANDOMLY SELECT 1000
2.	CREATE USER-BASED TEST DATASET BY COLLECTING GAMES FOR EACH USER
3.	RANDOMLY SELECT 1000 LINES FROM STEAM_API.CSV AS USER GAME CANDIDATE POOL
4.	FOR EACH USER, SELECT 20 GAMES OF HIGHEST EST; TRAINING DATASET = 80%
A.	COMPUTE ACCURACY = % GAMES IN THE TEST DATASET EXIST IN THE SELECTED 20 GAMES OF HIGHEST EST
5.	COMPUTE THE AVERAGE ACCURACY 

1.	CREATE THE TEST DATASET
2.	FOR EACH USER, SELECT 20 GAMES OF HIGHEST EST 
3.	COMPUTE THE PERCENTAGE OF ACCURACY = 100% IF THE GAME IS IN THE SELECTED 20 GAMES OF HIGHEST EST
4.	COMPUTE THE AVERAGE ACCURACY 
"""
def compute ():
    from SVD import SVD

    df_train = pd.read_csv("train_df_rating.csv")

    # user game candidate pool
    max_candidates = 1000
    df_train_1000 = df_train.take(np.random.permutation(len(df_train))[:max_candidates]) 

    df_test = pd.read_csv("test_df_rating.csv")
    df_test["Rating"] = ((df_test["Rating"].fillna(0)).astype(int)).astype(str)

    # test user game candidate pool
    max_candidates = 1000 if len(df_test) > 1000 else len(df_test)
    df_test_1000 = df_test.take(np.random.permutation(len(df_test))[:max_candidates]) 
    sorted_df_test_1000 = df_test_1000.sort_values(by= "User_ID", ascending = False)

    #extract dictionary keys = users and values = list of games
    #user_games = {"User_ID":[]}
    user_games = dict()

    for index, row in sorted_df_test_1000.iterrows():
        #print(row["User_ID"])
        if row["User_ID"] not in user_games.keys():
            user_games[row["User_ID"]] = []
            #print("creating")
        user_games[row["User_ID"]].append(row["Game_id"])
        #print(user_games[row["User_ID"]])
    #print(len(user_games))

    accuracy = []
    for user, games in user_games.items():
        #print(f'user: {user} games: {games}')
        recommended_games = SVD(user, 20, 100, df_train_1000)['Game_index']
        #print(type(recommended_games))
    
        #print(f'recommended_games: {recommended_games}, user: {user}')
        for i in games:
            if i in recommended_games:
                accuracy.append(100)
            else:
                accuracy.append(0)
    #print(len(accuracy))
    #print(accuracy)
    collaborative_filtering_accuracy = sum(accuracy)/len(accuracy)
    #print(f'recommendation accuracy average = {collaborative_filtering_accuracy} %')
    #print(df_test)
    return collaborative_filtering_accuracy

