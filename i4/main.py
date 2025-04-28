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

    Pros: Consistent across many datasources. Easy to understand and use, especially once you're familiar with it. Lightweight and good at handling many small requestss
    Cons: can be challenging to manage larger requests, especially with asynchronous or long-running endpoints. depending on API design it's often hard to handle things in bulk. Handling API keys and auth methods is tricky
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

    Pros: Fast iteration time, once the data is downloaded it's much faster to load into a script or analysis tool. Everything is handled locally which removes certain barriers to troubleshooting as well. 
    Cons: Storing data locally often leads to challenges with scaling when dealing with bigger datasets. Also it can be hard to enforce syntax rules and consistency across multiple files
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    library_path = os.path.join(script_dir, "Seattle_Public_Library_5863745812754529831.csv")
    with open(library_path, "r") as file:
        df = pd.read_csv(file)
    return df

def get_bigquery_data():
    """
    Pros: Robust set of features to perform complex analysis and nuanced queries, fast query processing time and, once set up, easy access to large amounts of data
    Cons: challenging to set up and use at a small scale, slow iteration time for systems changes, steep learning curve. Costs money 
    """
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
