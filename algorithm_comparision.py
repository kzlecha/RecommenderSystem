from datetime import datetime
from pandas import DataFrame, Series, read_csv

# HELPER METHODS
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
    num = 0
    initial = len((L1.intersection(L2))) + len((D1.intersection(D2))) - len((L1.intersection(D2))) - len((L2.intersection(D1)))
    divisor = len((L1.union(L2, D1, D2)))
    num = initial/divisor
    return num


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


# ALGORITHMS
def recommend_brute_force(likes, dislikes, index):
    '''
    @param likes: matrix of n users by m items likes
    @param dislikes: matrix of n users by m items dislikes
    @param index: int index of the given user
    ---
    return the list of recommended items via similarity inversion calculation
    '''
    # get the similarity series
    given_user_likes = likes.loc[index].values.tolist()
    given_user_dislikes = dislikes.loc[index].values.tolist()

    # create list of similaities
    similarity_series = Series(0, index=likes.index)
    for i in likes.index: 
        if(i != index):
            sim = 0
            simLikes = 0
            simDislikes = 0
            simLikes = compareInv(given_user_likes, likes.loc[i].values.tolist())
            simDislikes = compareInv(given_user_dislikes, dislikes.loc[index].values.tolist())
            sim = simLikes + simDislikes
            similarity_series.loc[i] = sim

    # sort the list
    similarity_series = similarity_series.sort_values(ascending=True)

    # everything the user has reviewed is in their likes and dislikes
    already_reviewed = given_user_likes
    already_reviewed.extend(given_user_dislikes)

    list_items = []
    for user_id in similarity_series.index:
        # get the items the user has reviewed and liked
        user_items = likes.loc[user_id].values.tolist()
        for item in user_items:
            if item not in list_items and item not in already_reviewed:
                list_items.append(item)

    return list_items


def recommend_set_operations(likes, dislikes, index):
    '''
    @param likes: matrix of n users by m items likes
    @param dislikes: matrix of n users by m items dislikes
    @param index: int index of the given user
    ---
    return the list of recommended items via similarity inversion calculation
    '''
    # get the similarity series
    given_user_likes = set(likes.loc[index])
    given_user_dislikes = set(dislikes.loc[index])

    # create list of similaities
    similarity_series = Series(0, index=likes.index)
    for i in likes.index: 
        if(i != index):
            user_likes = set(likes.loc[i])
            user_dislikes = set(dislikes.loc[i])
            num = sim(given_user_likes, user_likes, given_user_dislikes, user_dislikes)
            similarity_series.loc[i] = num

    # sort the list
    similarity_series = similarity_series.sort_values(ascending=False)

    # everything the user has reviewed is in their likes and dislikes
    already_reviewed = given_user_likes
    already_reviewed.update(given_user_dislikes)

    list_items = []
    for user_id in similarity_series.index:
        # get the items the user has reviewed and liked
        user_items = set(likes.loc[user_id])
        for item in user_items:
            if item not in list_items and item not in already_reviewed:
                list_items.append(item)

    return list_items


# read in data
movies = read_csv('data/movies.csv')
df_likes = read_csv('data/users_likes.csv', index_col="User ID")
df_dislikes = read_csv('data/users_dislikes.csv', index_col = "User ID")

# select user
user = 6925

start = datetime.now()
recommend_brute_force(df_likes, df_dislikes, user)
stop = datetime.now()

brute_force_time = stop - start
print("Time to calculate with inversions(brute force):", brute_force_time)

start = datetime.now()
recommend_set_operations(df_likes, df_dislikes, user)
stop = datetime.now()

set_op_time = stop - start
print("Time to calculate with set operations:", set_op_time)

difference = brute_force_time - set_op_time
print("Difference in runtime:", difference)
