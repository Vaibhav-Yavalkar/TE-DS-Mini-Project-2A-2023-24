#Importing pandas to create DatFrame
import pandas as pd
import utility_functions
import joblib
class preprocess2:
    def __init__(self):
        #rating dataframe
        self.ratings=pd.read_csv('Movies\\static\\dataset\\ratings.csv')  
        #linker dataset. This will be used to add title column into the Rating dataframe. Sice movieid column is common
        self.link=pd.read_csv('Movies\static\dataset\links.csv')
        self.movies=pd.read_csv('Movies\static\dataset\movies_metadata.csv')
    def operation(self):
        self.movies['imdb_id']=self.movies['imdb_id'].apply(utility_functions.clean_id_f,ex="tt0")
        self.link['imdbId']=self.link['imdbId'].apply(utility_functions.clean_id_f,ex="")
        #renaming imdbId column
        self.link.rename(columns={'imdbId':'imdb_id'},inplace=True)
        self.link_df=self.link.merge(self.movies[['imdb_id','title']],on='imdb_id',how='inner')
        self.ratings_df=self.ratings.merge(self.link_df[['movieId','title','imdb_id']],on='movieId',how='inner')
        self.ratings_df['total_vote_count']=self.ratings_df.groupby('title')['rating'].transform('count')
        #Therefore select only those movies which has more than 8000 votes. Basically we selecting 60%  of all the movies which has highest votes
        threshold=int(self.ratings_df['total_vote_count'].quantile(0.60))
        self.movies_after_threshold=self.ratings_df[self.ratings_df['total_vote_count']>threshold]
        self.movies_after_threshold.drop_duplicates(inplace=True)
        self.movies_after_threshold['title'].fillna('')
        #This is a 2d matrix which contains movies name as index and all the userid votes as columns
        self.matrix=self.movies_after_threshold.pivot_table(index='title',columns='userId',values='rating').fillna(0)
        return self.matrix
    def reverse_indices(self):
        movies_series=pd.Series(self.movies_after_threshold['title'].unique())
        joblib.dump(movies_series,"movies_data_col.pkl")
        self.movies_after_threshold.reset_index(drop=True)
        indices_rating=pd.Series(movies_series.index,index=movies_series)
        return indices_rating


inc=preprocess2()

matrix=inc.operation()
joblib.dump(matrix,"matrix.pkl")

from scipy.sparse import csr_matrix
#Compressing the matrix into csr_matrix which will improve the boost the calculation speed
sparse_matrix=csr_matrix(matrix)

from sklearn.neighbors import NearestNeighbors
#Creatings the object of nearestneighbor class
model_knn=NearestNeighbors(metric='cosine',algorithm='brute')
#it calculates the cosine similary for every movie
model_knn.fit(sparse_matrix)

joblib.dump(model_knn,"model_knn.pkl")
joblib.dump(inc.reverse_indices(),"indices_col.pkl")
