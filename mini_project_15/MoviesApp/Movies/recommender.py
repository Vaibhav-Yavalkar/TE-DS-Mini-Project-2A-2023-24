
import joblib
sigmoid_similarity=joblib.load('sigmoid_kernel.pkl')
indices_col=joblib.load('indices_col.pkl')
movies_data_con=joblib.load('movies_data_con.pkl')

model_knn=joblib.load("model_knn.pkl")
indices_con=joblib.load("indices_con.pkl")
movies_data_col=joblib.load('movies_data_col.pkl')
matrix=joblib.load('matrix.pkl')


#Defining function for content_recommendation
def content_recommendation(title,):
  idx=indices_con[title]

  sim=list(enumerate(sigmoid_similarity[idx]))

  sorted_sim=sorted(sim,key=lambda x:x[1],reverse=True)

  selected_indices=sorted_sim[1:11]

  movie_indices=[i[0] for i in selected_indices]
  sim_score=[i[1] for i in selected_indices]
  #print(sim_score)

  return movies_data_con['title'].iloc[movie_indices].tolist()


def colaborative_recommedation(title):
  idx=indices_col[title]
  distance,index=model_knn.kneighbors(matrix.iloc[idx,:].values.reshape(1,-1),n_neighbors=11)
  index=index.flatten()
  list_1=movies_data_col[index].tolist()
  #return movies_data_con['imdb_id'].loc[list_1[1:]].tolist()
  return list_1[1:]


def hybrid_recommendation(title):
  list1=colaborative_recommedation(title)
  list2=content_recommendation(title)
  for i in list1:
    if i in list2:
      list1.remove(i)
  for i in range(len(list1)):
    list2.insert(i+2*i+2,list1[i])
  return list2
  #fileterd_df=movies_data_con[movies_data_con['title'].isin(list2)]
  #return fileterd_df['imdb_id'].tolist()