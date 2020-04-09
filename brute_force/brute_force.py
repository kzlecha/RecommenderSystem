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

def get_similarity_matrix(data, index):
    '''
    @param data: matrix of n users by m items
    @param index: int index of the given user
    ---
    return the sorted list of similarities of all users to the given
    less inversions is more simialar
    '''
    # create list of similaities
    similarity_series = pd.Series(0, index=data.index)
    for i in df.index:
        if(i != index):
            a=get_user_array(data, i)
            sim = 0
            sim = compareInv(user_array, a)
            similarity_series.loc[i] = sim

    # sort the list
    similarity_series.sort_values(ascending=True)
    return similarity_series

def recommend_items(data, index, similarity_series):
    '''
    @param data: matrix of n users by m items
    @param index: int index of the given user
    ---
    return the items according to the most similar users's preferences
    '''
    already_reviewed = get_user_array(data, index)

    list_items = []
    for user_id in similarity_series.index:
        # get the items the user has reviewed
        user_items = data.loc[user_id]
        for item in user_items:
            if item not in list_items and item not in already_reviewed:
                list_items.append(item)

    return list_items
