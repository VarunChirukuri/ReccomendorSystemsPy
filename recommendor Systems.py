import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
dict1 = {'Nancy Pollock': {'Lawrence of Arabia': 2.5, 'Gravity': 3.5,
 'The Godfather': 3.0, 'Prometheus': 3.5, 'For a Few Dollars More': 2.5, 
 'The Guns of Navarone': 3.0},
'Jack Holmes': {'Lawrence of Arabia': 3.0, 'Gravity': 3.5, 
 'The Godfather': 1.5, 'Prometheus': 5.0, 'The Guns of Navarone': 3.0, 
 'For a Few Dollars More': 3.5}, 
'Mary Doyle': {'Lawrence of Arabia': 2.5, 'Gravity': 3.0,
 'Prometheus': 3.5, 'The Guns of Navarone': 4.0},
'Doug Redpath': {'Gravity': 3.5, 'The Godfather': 3.0, 'The Guns of Navarone': 4.5, 'Prometheus': 4.0, 'For a Few Dollars More': 2.5},
'Jill Brown': {'Lawrence of Arabia': 3.0, 'Gravity': 4.0,  'The Godfather': 2.0, 'Prometheus': 3.0, 'The Guns of Navarone': 3.0, 'For a Few Dollars More': 2.0}, 'Trevor Chappell': {'Lawrence of Arabia': 3.0, 'Gravity': 4.0,
 'The Guns of Navarone': 3.0, 'Prometheus': 5.0, 'For a Few Dollars More': 3.5},
'Allan Lamb': {'Gravity':4.5,'For a Few Dollars More':4.0,'Prometheus':4.0}, 
"Viv Richards": {'The Jungle Book': 5.0, 'The Guns of Navarone': 2.0, 'For a Few Dollars More': 5.0, 'Gravity': 5.0}}
reviewer1_movies = dict1['Nancy Pollock']
#print(reviewer1_movies)ß

def get_common_review_scores(reviewer1, reviewer2, reviews):
    reviewer1_movies = dict1[reviewer1]
    reviewer2_movies = dict1[reviewer2]
    reviewer1_scores = []
    reviewer2_scores = []
    for movie in reviewer1_movies:
        if movie in reviewer2_movies:
            reviewer1_scores.append(reviewer1_movies[movie])
            reviewer2_scores.append(reviewer2_movies[movie])
    return reviewer1_scores, reviewer2_scores

def get_similarity(reviewer1, reviewer2, reviews, similarity_function = euclidean_distances):
    reviewer1_scores, reviewer2_scores = get_common_review_scores(reviewer1, reviewer2, reviews)
    if len(reviewer1_scores) == 0:
        return 0 #no common reviews
    
    return similarity_function([reviewer1_scores], [reviewer2_scores])

x=get_common_review_scores('Nancy Pollock',  'Jack Holmes', dict1)
print(x)

y = get_similarity('Nancy Pollock', 'Jack Holmes', dict1)
print(y)

def get_most_similar_to(reviewer, reviews, similarity_function = euclidean_distances, n = 3):
    similarity_scores = []
    for r in dict1:
        if r != reviewer:
            score = get_similarity(reviewer, r, dict1, similarity_function) 
            similarity_scores.append((score, r))
    similarity_scores.sort(reverse=True)
    return similarity_scores[:n]

z = get_most_similar_to('Nancy Pollock', dict1, similarity_function = euclidean_distances, n=3)
print(z)

#function to get recommendations for a user
def get_recommendations(reviewer, dict1 ):
    movie_scores = []
    similarities = {}
    #get list of movies seen by reviewer
    movies_seen = list(dict1[reviewer].keys())
    df = pd.DataFrame(dict1)
    all_movies = list(df.index)
    #set difference gives us movies not seen
    movies_not_seen = list(set(all_movies) - (set(movies_seen)))
    for other in dict1: #other refers to other reviewers
        if other == reviewer:
            continue
        score = get_similarity(reviewer, other, dict1)
        similarities[other] = score
    for movie in movies_not_seen:
        score = 0.0
        total = 0.0
        for r in dict1:
            if r == reviewer: continue
            if movie in dict1[r]:
                score += (similarities[r] * dict1[r][movie])
                total += similarities[r]
        if total > 0:
            movie_scores.append((score / total, movie))
    
    if movie_scores:
        movie_scores.sort(reverse=True)
    return movie_scores

print(get_recommendations('Nancy Pollock', dict1))
df = pd.DataFrame(dict1)
print(df)
df1 = df.transpose()
df2 = df1.to_dict()
print(df2)

