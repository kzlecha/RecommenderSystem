# from datetime import datetime

from pandas import DataFrame, Series, read_csv

def sim(L1, L2, D1, D2):
    '''
    @param L1: list of user1 liked
    @param L2: list of user2 liked
    @param D1: list of user1 disliked
    @param D2: list of user2 disliked
    ---
    Compare the lists and return the set similarity

    Similarity Calculation:
    s(u1, u2) = (|L1 intersection L2| + |D1 intersection D2| -
                |L1 intersection D2| - |L2 intersection D1|) / 
                |L1 union L2 union D1 union D2|
    '''
    num = 0;
    initial = len((L1.intersection(L2))) + len((D1.intersection(D2))) - len((L1.intersection(D2))) - len((L2.intersection(D1)))
    divisor = len((L1.union(L2, D1, D2)))
    num = initial/divisor
    return num

def get_user_array(data, index):
    '''
    @param data: matrix of n users by m items
    @param index: int index of the given user
    ---
    return the set of ratings from the user
    '''
    return set(data.loc[index])

def get_similarity_series(likes, dislikes, index):
    '''
    @param likes: matrix of n users by m items likes
    @param dislikes: matrix of n users by m items dislikes
    @param index: int index of the given user
    ---
    return the sorted list of similarities of all users to the given
    less inversions is more simialar
    '''
    given_user_likes = get_user_array(likes, index)
    given_user_dislikes = get_user_array(dislikes, index)
    # create list of similaities
    similarity_series = Series(0, index=likes.index)
    for i in likes.index: 
        if(i != index):
            user_likes = get_user_array(likes, i)
            user_dislikes = get_user_array(dislikes, i)
            num = sim(given_user_likes, user_likes, given_user_dislikes, user_dislikes)
            similarity_series.loc[i] = num

    # sort the list
    similarity_series.sort_values(ascending=False)
    return similarity_series

def recommend_items(likes, dislikes, index, similarity_series):
    '''
    @param data: matrix of n users by m items
    @param index: int index of the given user
    ---
    return the items according to the most similar users's preferences
    '''
    # everything the user has reviewed is in their likes and dislikes
    already_reviewed = get_user_array(likes, index)
    already_reviewed.update(get_user_array(dislikes, index))

    list_items = []
    for user_id in similarity_series.index:
        # get the items the user has reviewed and liked
        user_items = get_user_array(likes, user_id)
        for item in user_items:
            if item not in list_items and item not in already_reviewed:
                list_items.append(item)

    return list_items


# read in data
movies = read_csv('../data/movies.csv')
df_likes = read_csv('../data/users_likes.csv', index_col="User ID")
df_dislikes = read_csv('../data/users_dislikes.csv', index_col = "User ID")

# select user
user = 6925

# get the similarity matrix for the user
sim_series = get_similarity_series(df_likes, df_dislikes, user)
list_items = recommend_items(df_likes, df_dislikes, user, sim_series)
print(list_items)
