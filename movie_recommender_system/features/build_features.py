import ast
import nltk
from nltk.stem import PorterStemmer
import pandas as pd

def extract_data_from_dict_string(string_dict, key) -> list:
    value_list = []
    for item in ast.literal_eval(string_dict):
        value_list.append(item[key])
    return value_list

def extract_cast(string_dict: str, key: str, count: int) -> list:
    value_list = []
    counter = 0
    for item in ast.literal_eval(string_dict):
        if counter == count:
            break
        else:
            value_list.append(item[key])
            counter += 1
    return value_list

def extract_crew(string_dict: str, key: str, crew_jobs: list) -> list:
    value_list = []
    for item in ast.literal_eval(string_dict):
        if item['job'] in crew_jobs:
            value_list.append(item[key])
    return value_list

def remove_space(string_list: list) -> list:
    return [x.replace(" ", "") for x in string_list]

def stems(text):
    ps = PorterStemmer()
    T = []
    for i in text.split():
        T.append(ps.stem(i))
    
    return " ".join(T)

from typing import List

def processing_features(df: pd.DataFrame,
                        str_columns: List[str] = ["overview, ""original_title", "original_language", "release_date"],
                        list_dict_columns: List[str] = ["genres", "keywords", "production_companies", "production_countries"],
                        cast_count: int = 3,
                        crew_jobs_list: List[str] = None) -> pd.DataFrame:
    df = df.copy()
    df = df.dropna()

    columns_base = ['movie_id', 'title']
    columns_processed = []
    
    if str_columns is not None:
        for str_columns in str_columns:
            df[str_columns] = df[str_columns].apply(lambda x: x.split())
            columns_processed.append(str_columns)

    # list string columns
    for column in list_dict_columns:
        df[column] = df[column].apply(lambda x: extract_data_from_dict_string(x, "name"))
        df[column] = df[column].apply(lambda x: remove_space(x))
        columns_processed.append(column)

    if cast_count > 0:
        df.loc[:, 'cast'] = df['cast'].apply(lambda x: extract_cast(x, 'name', cast_count))
        df.loc[:, 'cast'] = df['cast'].apply(lambda x: remove_space(x))
        columns_processed.append('cast')
    
    if crew_jobs_list is not None:
        df.loc[:, 'crew'] = df['crew'].apply(lambda x: extract_crew(x, 'name', crew_jobs_list))
        df.loc[:, 'crew'] = df['crew'].apply(lambda x: remove_space(x))
        columns_processed.append('crew')

  

    # Create tags column
    df.loc[:, 'tags'] = df['overview'].apply(lambda x: [])
    for column in columns_processed:
        df["tags"] = df["tags"] + df[column]
    df["tags"] = df["tags"].apply(lambda x: " ".join(x).lower())
    df["tags"] = df["tags"].apply(stems)

    df = df[columns_base + ['tags']]
    return df
