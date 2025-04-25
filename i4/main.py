import os
import requests
import json
import pandas as pd
from google.cloud import bigquery

def get_poetry_json(author):
    """
    Fetches poetry data from the PoetryDB API for a given author.
    
    Parameters:
        author (str): The name of the author to fetch poetry for.
        
    Returns:
        list: A list of dictionaries containing poetry data.
    """
    url = f"https://poetrydb.org/author,poemcount/{author};5"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {author}: {response.status_code}")
        return []
    
def load_library_csv():
    """
    Loads the library CSV file into a DataFrame.
    
    Returns:
        pd.DataFrame: A DataFrame containing the library data.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    library_path = os.path.join(script_dir, "Seattle_Public_Library_5863745812754529831.csv")
    with open(library_path, "r") as file:
        df = pd.read_csv(file)
    return df

def get_bigquery_data():
    client = bigquery.Client(project="erudite-canto-247700")
    query = "SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` LIMIT 10"
    query_job = client.query(query)
    results = query_job.result()
    return results.to_dataframe()

if __name__ == "__main__":
    # Example usage
    author = "Emily Dickinson"
    poetry_data = get_poetry_json(author)
    
    if poetry_data:
        print(json.dumps(poetry_data, indent=2))
    
    library_df = load_library_csv()
    print(library_df.head())
    
    bigquery_df = get_bigquery_data()
    print(bigquery_df.head())