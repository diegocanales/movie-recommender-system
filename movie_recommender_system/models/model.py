from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender(BaseEstimator, TransformerMixin):
    def __init__(self, max_features=5000, stop_words='english'):
        self.max_features = max_features
        self.stop_words = stop_words
        self.cv = CountVectorizer(max_features=self.max_features, stop_words=self.stop_words)
        self.vector = None
        self.similarity = None
        self.X = None

    def fit(self, X, y=None):
        self.X = X
        self.vector = self.cv.fit_transform(X['tags']).toarray()
        self.similarity = cosine_similarity(self.vector)
        return self

    def predict(self, movie, n=5):
        index = self.X[self.X['title'] == movie].index[0]
        distances = sorted(list(enumerate(self.similarity[index])), reverse=True, key = lambda x: x[1])
        recommended_movies = []
        for i in distances[1:n+1]:
            recommended_movies.append(self.X.iloc[i[0]].title)
        return recommended_movies
