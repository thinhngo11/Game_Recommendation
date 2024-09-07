import pandas as pd
import numpy as np
import random
import csv

def compute():
    """ to create training and test datasets from rating.csv 80/20% and retaining train users if existed in test """
    df_rating = pd.read_csv("rating.csv")
    user_rating = pd.read_csv("user_rating.csv")
    # user_rating.columns = ["ID", "User_ID","Game_id", "Game_name","Rating"]

    #full_df_rating = pd.concat([user_rating[["User_ID","Game_id","Game_name","Rating"]],df_rating[["User_ID","Game_id","Game_name","Rating"]]])
    full_df_rating = df_rating[["User_ID","Game_id","Game_name","Rating"]]
    len_df =len(full_df_rating)
    #print(full_df_rating)
    #print(type(full_df_rating))

    train_df_rating = full_df_rating.take(np.random.permutation(len_df)[:int(0.8 * len_df)]) #80% of rating.csv
    test_df_rating = pd.concat([full_df_rating,train_df_rating]).drop_duplicates(keep=False) #the remaining 20%
    #print(train_df_rating["User_ID"], train_df_rating["Game_id"])

    #exclude users in the test dataset but not in train dataset
    train_users = train_df_rating["User_ID"].unique().tolist()
    
    mask = []
    for index, row in test_df_rating.iterrows():
        #print(f'index: {index}')
        #print(row["User_ID"])
        mask.append(False) if row["User_ID"] not in train_users else mask.append(True)
    print(len(mask))

    df_rating = test_df_rating[mask]

    train_df_rating.to_csv("train_df_rating.csv")
    df_rating.to_csv("test_df_rating.csv")
    quit()
    
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
    """