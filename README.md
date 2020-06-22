# RecommenderSystem
A search engine that searches for similarities and dissimilarities among users to recommend a list of products

Our topic is to design an algorithm to recommend items based on the likes and dislikes of a user and their similarities to other users.

## Contributors
The following algorithm was created by:
* **Cameron Chong** - [camcamchong](https://github.com/camcamchong)
* **Kathryn Lecha** - [kzlecha](https://github.com/kzlecha)
* **Emily Medema** - [emedema](https://github.com/emedema)
* **Lauren St.Clair** - [laurenstclair](https://github.com/laurenstclair)

## Problem Formulation
### Input
Given a set of users U = {u<sub>1</sub>, u<sub>2</sub>, …, u<sub>i</sub>, …,u<sub>n</sub>},  Each user U<sub>i</sub> has a set of likes L<sub>i</sub> and dislikes D<sub>i</sub>.
### Output
A list of recommended items for User U<sub>i</sub> based on the likes and dislikes of Users similar to U<sub>i</sub>. 
### Similarity Calculation
We will calculate the similarity between users via:

s(U<sub>1</sub>, U<sub>2</sub>) = (|L<sub>1</sub> ∩ L<sub>2</sub>| + |D<sub>1</sub> ∩ D<sub>2</sub>| - |L<sub>1</sub> ∩ D<sub>2</sub>| - |D<sub>1</sub> ∩ L<sub>2</sub>|) / (L<sub>1</sub> ∪ L<sub>2</sub> ∪ D<sub>1</sub> ∪ D<sub>2</sub> )

For a given user U<sub>i</sub>, we will find the users similar to U<sub>i</sub>. 
Then, from the set of all items X, we will remove the items the given user U<sub>i</sub> has ‘reviewed’.

X - (L<sub>i</sub> ∩ D<sub>i</sub>), then we will recommend the items in similar user U<sub>i</sub> list L<sub>i</sub> ∈ X

## Algorithm

We implemented the following two algorithms to produce a recommendation. We furthermore proved the correctness for both algorithms in our project documentation, which is included in this repository.

### Brute Force
- Compute the inversion array between a given user U<sub>i</sub> and every user. The score is based on the magnitude of difference between U<sub>i</sub> and other users.
- Create a similarity array between a given user U<sub>i</sub> and every other user. A more similar user to you has fewer inversions. 
- Find items that users with high similarity to the given user have reviewed. Retrieve all items and remove all items that you, the given user, have reviewed
- Return that list of reviewed items

### Similarity Calculation

#### Description
An easy way to improve the run-time of the algorithm would be to change the method of counting inversions. This way it would be O(n*logn) instead of O(n<sup>2). 

However, this is really hard to adapt for our ranking and two arrays. Therefore, we decided to switch to calculating similarity via the Jaccard Index. This follows the aforementioned equation :

s(U<sub>1</sub>, U<sub>2</sub>) = (|L<sub>1</sub> ∩ L<sub>2</sub>| + |D<sub>1</sub> ∩ D<sub>2</sub>| - |L<sub>1</sub> ∩ D<sub>2</sub>| - |D<sub>1</sub> ∩ L<sub>2</sub>|) / (L<sub>1</sub> ∪ L<sub>2</sub> ∪ D<sub>1</sub> ∪ D<sub>2</sub> )

This will also allow us to use sets, which are much faster than matrices and arrays. For example, a set will let us check if an item is already in a set in O(1) time rather than iterating through an array.

When implemented with a combination of sets and series (similar to hash tables) the time complexity is O(nm).

#### Algorithm
- Compute the inversion array between a given user U<sub>i</sub> and every user. The score is based on the similarity calculation between U<sub>i</sub> and other users.
- Create a similarity array/hashtable between a given user U<sub>i</sub> and every other user. A more similar user to you has fewer inversions. 
- Find items that users with high similarity to the given user have reviewed. Retrieve all items and remove all items that you, the given user, have reviewed
- Return that list of reviewed items

### Other Discussed Algorithms

We discussed a number of other possible implementations:
- Machine Learning for Similarity Calculation and Sparsity of Data
- Counting Inversions
- representing the data via a tripartite graph
- priority queues to avoid sorting

These will be discussed more in the Data Structure section of the Discussion of Implementation below.

## Discussion of Implementation

Below is a short discussion behind many of the decisions made in the implementation. This is covered in detail in our Project Documentation.

### Dataset
Originally we were using the MovieLens dataset, however, it was very hard to work with as the brute-force method took hours to run. Therefore, we created our own dataset which is much smaller. Our implementations would still work for any dataset (if you have the time to run it), provided you format the data in the correct way from the dataset

### Data Structures

#### Currently implemented DataStructure
Currently, we implemented a dataframe (which is similar to a matrix). This is not the most efficent data structure for us as we are iterating through the matrix in order to compare users and find recommended items. If we pick a better data structure we could greatly improve the runtime. However, since a dataframe is indexed, it can also act as a dictionary (hashmap) of lists. In this way, the runtime is greatly improved over the matrix, as the indices created faster lookup times. Both implementations use dataframes.

Because we decided to target the step causing the most complexity outside of the inversions and reduce it, we decided to implement a hash-table (or similar) so that we would not have to iterate over the given user’s items every time. This would reduce that complexity to O(nm).

Also we considered sets, which are much faster than matrices and arrays. For example, a set will let us check if an item is already in a set in O(1) time rather than iterating through an array.

We eventually decided to use a combination of sets and series (similar to hash tables) reducing our complexity down to O(nm).

#### Other discussed Structures

One data structure we could use is graphs. Since we are focused on user-item relationships, if we initialized a graph G(V, E) where each node is either an item or a user. When a user ‘likes’ an item a directed edge is formed with a weight representing the rank of the item. When two users are compared an bi-directed edge is formed with the weight representing the similarity. 

However, the way that our data is presented is that each user has a ranking of movie items. This is hard to represent in a graph. According to [this source](https://arxiv.org/pdf/1604.03147.pdf), a tripartite graph would be more efficient, however, it does not work with the problem formulation and data that we have.

Another possible data structure we considered was priority queues. If we stored the users and sorted by similarity we could avoid sorting, which would reduce complexity. However, this would still make us not able to use the aforementioned hash-table method, which would create more complexity comparatively.


### Concerns
It should be noted that the “Algorithm B”, using set operations, is listed as running in almost the same time or slower than counting inversions. However, as set operations scale faster than matrix, as the input grows asymptotically, the set operations method will operate faster than the matrix, according to their big O notations discussed in the next section.

One major concern in implementation was the time that it takes to run and to implement. Because of this, we shrunk the dataset, so implementation testing could be done in a timely manner. Each member of the group had a large number of other  responsibilities to address in the same timeframe, so development of an algorithm was stunted by that. We discussed the required output and determined the best one for us accordingly. 
