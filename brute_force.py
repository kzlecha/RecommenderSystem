# from datetime import datetime

from pandas import DataFrame, Series, read_csv

def compareInv(A,B):
    '''
    @param A: list of rankings
    @param B: list of rankings
    ---
    Compare the lists and return the number of inversions
    '''
    numInv = 0
    for i in range(0, len(A)):
        for j in range(0, len(A)):
            if A[i] != B[j] and i != j:
                numInv = numInv + 1
    return numInv

def get_user_array(data, index):
    '''
    @param data: matrix of n users by m items
    @param index: int index of the given user
    ---
    return the ratings of the user
    '''
    return data.loc[index].values.tolist()

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
            sim = 0
            simLikes = 0
            simDislikes = 0
            simLikes = compareInv(given_user_likes, get_user_array(likes,i))
            simDislikes = compareInv(given_user_dislikes, get_user_array(dislikes,i))
            sim = simLikes + simDislikes
            similarity_series.loc[i] = sim

    # sort the list
    similarity_series.sort_values(ascending=True)
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
    already_reviewed.extend(get_user_array(dislikes, index))

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