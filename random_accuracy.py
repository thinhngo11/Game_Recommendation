""" random recommendation accuracy
1. for each user in the test dataset:
    randomly recommend a list of games which are not owned by the user in the training dataset
        determine user-games in the train dataset
        find unique games in the train dataset

    compute recommendation accuracy based on matching of games of the user in the test dataset and the recommendation list
        determine user-games in the test dataset
        for each user in the test dataset, 
            determine unique games in the train dataset not owned by an user
            find the random recommendations from the list above
            compute accuracy of each game the user owns in the test dataset
        compute average accuracy for all games

        ACCURACY: 1.6% for all data (no minimum curation); 2.7% for minimum = 10; 50% for 50
"""
import pandas as pd
import numpy as np
import random
import csv
import itertools

def compute():

    df_train = pd.read_csv("train_df_rating.csv")
    df_test = pd.read_csv("test_df_rating.csv")

    sorted_df_train = df_train.sort_values(by= "User_ID", ascending = False)

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

    #unique games in the train dataset
    train_unique_games = set(itertools.chain.from_iterable(train_user_games.values()))
    print(f'train_unique_games {train_unique_games}')

    accuracy = []
    for user, games in test_user_games.items():
        print(f'user {user} games {games}')
        difference_games = train_unique_games - set(train_user_games[user])
        random.shuffle(list(difference_games))
        recommended_games = list(difference_games)[:20]
        print(f'recommended_games {recommended_games}')
        for i in games:
            accuracy.append(100) if i in recommended_games else accuracy.append(0)

         #print(len(accuracy))
        print(accuracy)
    random_recommendation_accuracy = sum(accuracy)/len(accuracy)
    #print(f'recommendation accuracy average = {random_recommendation_accuracy} %')
    return random_recommendation_accuracy
