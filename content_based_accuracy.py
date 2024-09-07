from symbol import test_nocond, testlist_comp, testlist_star_expr
import pandas as pd
import numpy as np
import random
import csv


""" compute recommendation accuracy of the content-based recommendation """
""" 
FOR EACH USER (GAME-BASED): 
FOR EACH GAME, DETERMINE 20 CONTENT BASED RECOMMENDATION LIST 
1.	DERTERMINE GAMES IN THE TRAINING AND TESTING DATASETS
2.	REMOVE TEST DATASET GAMES FROM TRAINING DATASET GAMES
3.	CREATE A DICT OF USER&GAMES FROM THE TRAINING LIST
4.	DETERMINE THE CONTENT-BASED LIST FOR EACH USER IN THE TRAINING LIST
5.	COMPUTE ACCURACY = %GAMES OF EACH USER IN THE TEST DATASET IN THE LIST   
6.	FOR EACH GAME OF THE USER IN THE TRAINING LIST, DETERMINE THE LIST FROM ALL STEAM_API.CSV
7.	MERGE ALL LISTS
8.	DETERMINE THE MOST RECOMMENDED GAMES LIST
9.	ACCURACY = % GAMES IN THE TEST DATASET IN THE MOST RECOMMENDED GAME LIST
10.	COMPUTE THE AVERAGE ACCURACY FOR ALL USERS

determine games owned by every user in the training dataset,
compute the list of common or most recommended games for every user 
accuracy of every user = % games in the test dataset of the user IN the user's recommended list 
average accuracy of all users 
"""
"""
determine games owned by every user in the testing dataset and training dataset
 1. create a dict of user-games from the test dataset whose users are in the training dataset
 2. for each game of a user, find the list of content-based recommended games
 3. for every user, find the list of the most common recommended games
 4. compute accuracy for each game of every user: % games owned by a user in the test dataset IN the recommened list
 5. calculate the average accuracy
"""
def compute():
    from content_based import content_based_recommend

    df_train = pd.read_csv("train_df_rating.csv")

    # user game candidate pool
    #max_candidates = 1000
    #df_train_1000 = df_train.take(np.random.permutation(len(df_train))[:max_candidates]) 

    df_test = pd.read_csv("test_df_rating.csv")
    df_test["Rating"] = ((df_test["Rating"].fillna(0)).astype(int)).astype(str)

    # test user game candidate pool
    max_candidates = 1000 if len(df_test) > 1000 else len(df_test)
    #df_test_1000 = df_test.take(np.random.permutation(len(df_test))[:max_candidates]) 
    #sorted_df_test_1000 = df_test_1000.sort_values(by= "User_ID", ascending = False)
    #df_test = df_test.take(np.random.permutation(len(df_test))) 

    # 1. create a dict of user-games from the training dataset whose users are in the testing dataset
    print('len(df_train))' + str(len(df_train)))
    sorted_df_train = df_train.sort_values(by= "User_ID", ascending = False)
    print(f'len(sorted_df_train) {len(sorted_df_train)}')

    #extract dictionary keys = users and values = list of games in the train dataset 
    #whose users are also in the testing dataset
    #user_games = {"User_ID":[]}
    train_user_games = dict()
    df_test_user = df_test["User_ID"].unique().tolist()
    for index, row in sorted_df_train.iterrows():
        #print(row["User_ID"])
        if row["User_ID"] in df_test_user:
            if row["User_ID"] not in train_user_games.keys():
                train_user_games[row["User_ID"]] = []
                #print("creating")
            train_user_games[row["User_ID"]].append(row["Game_id"])
            #print(train_user_games[row["User_ID"]])
    print(f'len(train_user_games.keys()) {len(train_user_games.keys())}')
    #print(f'train_user_games {train_user_games}')
    #quit()
    #  2. for each game of a user in train_user_games, find the list of most content-based recommended games
    #  3. for every user, find the list of the most common recommended games

    #extract dictionary keys = users and values = list of games in the test dataset 
    sorted_df_test = df_test.sort_values(by= "User_ID", ascending = False)

    #test_user_games = {"User_ID":[]}
    test_user_games = dict()
    for index, row in sorted_df_test.iterrows():
        #print(row["User_ID"])
        if row["User_ID"] not in test_user_games.keys():
            test_user_games[row["User_ID"]] = []
            #print("creating")
        test_user_games[row["User_ID"]].append(row["Game_id"])
        #print(test_user_games[row["User_ID"]])
    print(len(test_user_games.keys()))
    #print(test_user_games)

    #extract dictionary keys = users in the testing dataset and 
    #values = list of recommended games of corresponding users the training dataset 
    most_recommended = {}
    user_most_recommended = {}
    for user in test_user_games.keys():
        most_recommended_list = []
        for game_index in train_user_games[user]:
            #print(f'game index: {game_index}')
            list_recommended = content_based_recommend(game_index, 20)
            #print(f'list_recommended {list_recommended}')
            for game_id in list_recommended:
                if game_id not in most_recommended:
                     most_recommended[game_id] = 1
                else:
                     most_recommended[game_id] += 1
        #print(most_recommended)
        #quit()
        #{k: v for k, v in sorted(most_recommended.items(), key=lambda item: item[1])}
        most_recommended_list = [k for k, v in sorted(most_recommended.items(), key=lambda x: x[1], reverse=True)[:20]]
        #print(most_recommended_list)
        user_most_recommended[user] = most_recommended_list
    print(f'len(user_most_recommended.keys()) {len(user_most_recommended.keys())}')
    #print(user_most_recommended)
    # 4. compute accuracy for each game of every user: % games owned by a user in the test dataset IN the recommened list
    # 5. calculate the average accuracy
    
    accuracy = []
    for user, games in test_user_games.items():
        #print(f'user: {user} games: {games}')  
        #print(user_most_recommended[user])
        #quit()
        for i in games:
            accuracy.append(100) if i in user_most_recommended[user] else accuracy.append(0)
                
    print(len(accuracy))
    print(accuracy)
    content_based_accuracy = sum(accuracy)/len(accuracy)
    #print(f'recommendation accuracy average = {collaborative_filtering_accuracy} %')
    return content_based_accuracy

