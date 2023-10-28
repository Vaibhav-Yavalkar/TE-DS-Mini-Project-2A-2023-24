#Importing pandas to create DatFrame
import pandas as pd
import utility_functions

class preprocess:
    def __init__(self):
        self.movies_df=pd.read_csv('C:\\Users\\sumit\\vscode\\MoviesApp\\Movies\\static\\dataset\\movies_metadata.csv')
       
    def operation(self):
        self.movies_df=utility_functions.preprocess(self.movies_df)
        self.movies_df=utility_functions.drop_columns(self.movies_df,columns=['poster_path','homepage','budget','status','video','release_date','spoken_languages'])
      
        #Since title has 6 missing data so taking out all records where title is not nan
        movies_df=self.movies_df[self.movies_df['title'].notna()]
    def column_operation(self):
        #importing new dataset named 'credits' which conatins the cast and crew information
        self.credits=pd.read_csv('C:\\Users\\sumit\\vscode\\MoviesApp\\Movies\\static\\dataset\\credits.csv')
        # Parse strings containing lists into actual lists using ast.literal_eval or json.loads
        self.movies_df=utility_functions.jason_to_list(self.movies_df,'genres')
        self.credits=utility_functions.jason_to_list(self.credits,'cast')
        self.credits=utility_functions.jason_to_list(self.credits,'crew')

        #This function will return the only first genre present in each each record. if genre  does not exist ,will return empty string
        self.movies_df['top_genre']=self.movies_df['genres'].apply(utility_functions.first_data)
        self.credits['top_cast']=self.credits['cast'].apply(utility_functions.first_data)

        #This function return the name of the crew where job is director. if not exist return empty string
        self.credits['top_crew']=self.credits['crew'].apply(utility_functions.top_crew_f)

        #This function will covert id into integer if it is in string or in any other formate
        self.movies_df['id']=self.movies_df['id'].apply(utility_functions.clean_id)
        self.credits['id']=self.credits['id'].apply(utility_functions.clean_id)
    def ddd_combined_text_column(self):
        #merging movies dataset with credits dataset based on the id
        self.movies_df_merge=self.movies_df.merge(self.credits[['id','top_cast','top_crew']],on='id',how='inner')
        # Combine the text from 'overview', 'top_cast', and 'top_crew' columns into a single column
        self.movies_df_merge['combined_text'] = self.movies_df_merge['overview'] + ' ' + self.movies_df_merge['top_cast'] + ' ' + self.movies_df_merge['top_crew'] +' '+ self.movies_df_merge['top_genre']
        
        #Since the count of combined text column is less than the title we fill remaining fields with empty string so that it matches
        self.movies_df_merge['combined_text'].fillna('', inplace=True)
        #Considering only those movies which has vote count greater than 50 for better recommendation
        self.movies_data=self.movies_df_merge[self.movies_df_merge['vote_count']>50]
        return self.movies_data
    def reverse_indices(self):
        self.movies_data.reset_index(drop=True,inplace=True)
        joblib.dump(self.movies_data,"movies_data_con.pkl")
        indices=pd.Series(movies_data.index,index=movies_data['title']) 
        return indices


    

ins=preprocess()
ins.column_operation()
movies_data=ins.ddd_combined_text_column()


    

# importing Tfidfvectorizer. Its a NLP tool to convert text into numerical values
from sklearn.feature_extraction.text import TfidfVectorizer
#creating an instance or object of tfidf class
tfidf=TfidfVectorizer(max_df=0.8,token_pattern=r"(?u)\b[a-zA-Z]{3,}\b",analyzer='word',stop_words='english',ngram_range=(1,3),strip_accents='unicode')
#applying the fit_transform method to calcluate the numerical values based on important terms
tfidf_matrix=tfidf.fit_transform(movies_data['combined_text'])
#importing sigmoid kernel algorithm to calculate the simlarity with respect to each movie
from sklearn.metrics.pairwise import sigmoid_kernel
sigmoid_similarity=sigmoid_kernel(tfidf_matrix,tfidf_matrix)

import joblib 
joblib.dump(sigmoid_similarity, 'sigmoid_kernel.pkl')
joblib.dump(ins.reverse_indices(),'indices_con.pkl')
    


    