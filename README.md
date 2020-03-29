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
- Compute the inversion array between a given user U<sub>i</sub> and every user. The score is based on the magnitude of difference between U<sub>i</sub> and other users.
- Create a similarity array between a given user U<sub>i</sub> and every other user. A more similar user to you has fewer inversions. 
- Find items that users with high similarity to the given user have reviewed. Retrieve all items and remove all items that you, the given user, have reviewed
- Return that list of reviewed items
