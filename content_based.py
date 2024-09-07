import pandas as pd
import string
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel,cosine_similarity


df_all = pd.read_csv("steam_api.csv",encoding = 'utf-8')
"""
unique_games = df_all["Game_id"].unique().tolist()
list_unique_game_record = []
for index, row in df_all.iterrows():
    #print(row["User_ID"])
    if (row["Game_id"] in unique_games):
        list_unique_game_record.append([row["Game_id"], row["Game_description"]])
        unique_games.remove(row["Game_id"])

df = pd.DataFrame(list_unique_game_record, columns=["Game_id", "Game_description"])
"""
df = df_all
#print(df)
print(len(df))

""" NEW: create a unique-game df 
dict_all = {k: v for (k, v) in df_all.groupby('Game_id')}
print(type(dict_all))
#for key, value in dict_all.items():
#    print(f'key: {key} value: {value}')
    #print(type(value))
    #print('key: ' + str(key) + 'value: ' + value['Game_description'])
df = dict_all.values()
print(len(df))
#print(df)

df = {name: df[df['customer name'] == name] for name in df['Game_id'].unique()}
"""
print("Training tfidf")
tfidf_vectorizer = TfidfVectorizer(analyzer='word', strip_accents = 'unicode',stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(list(df['Game_description']))
print("Complete training tfidf")
#print(type(tfidf))
print(tfidf)

def content_based_recommend(game_id, max_number):
    related_docs = []
    #print(f'game_id {game_id}')
    if (df [df ["Game_id"]==game_id]).size > 0:
        game_index = df [df ["Game_id"]==game_id].index[0]
        #print(f'game_index {game_index}')
        #print(f'tfidf[game_index] {tfidf[game_index]}')
        similarities = linear_kernel(tfidf[game_index],tfidf).flatten()
        #print(type(similarities))
        #print(f'similarities {similarities}')
        related_docs_indices = (-similarities).argsort()[1:(max_number+1)]
        #print(type(related_docs_indices))
        #print(related_docs_indices)
        for i in related_docs_indices:
            related_docs.append(df['Game_id'][i])
        #print(related_docs)
        return related_docs
    else:
        return [0] * (max_number+1)


# predict = content_based_recommend(df[df['Game_id']==427520].index[0], 20)
# list_predict_game = df.iloc[predict]['Game_name']
# for i in list_predict_game:
#     print(i)