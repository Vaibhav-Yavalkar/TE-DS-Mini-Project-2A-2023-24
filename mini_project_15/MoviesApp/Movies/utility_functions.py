import pandas as pd
import ast
def preprocess(dataset):
        #Removing Duplicates record.This will remove row which is repeated more than once
        dataset.drop_duplicates(inplace=True)
        #Reseting index of dataframe. This will remove the old index and add new index in sorted form
        dataset.reset_index(drop=True, inplace=True)
        return dataset
       
def drop_columns(dataset,columns):
         #Removing columns which are not useful for recommendation
        dataset.drop(columns=[columns],inplace=True)
        return dataset
        
def jason_to_list(dataset,column):
        dataset[column]=dataset[column].apply(ast.literal_eval)
        return dataset

def first_data(value):
  try:
    return value[0]['name']
  except:
    return ""
        
#This function return the name of the crew where job is director. if not exist return empty string
def top_crew_f(value):
    for data in value:
      try:
        if data['job']=='Director':
          return data['name']
          break
      except:
        return ""
        

#This function will covert id into integer if it is in string or in any other formate
def clean_id(value):
  if isinstance(value,str):
    cleaned_value=value.replace("'","")
    if cleaned_value.isdigit():
      return int(cleaned_value)
    else:
      return -1
  else:
    return value
        
def clean_id_f(value,ex):
  if isinstance(value,str):
    value=value.replace(ex,"")
    if value.isdigit():
      return int(value)
    else:
      return -1
  else:
    return  value