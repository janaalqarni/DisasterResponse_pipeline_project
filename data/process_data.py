import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """
    this function load messages and categories dataset using the filepath
    
    inputs: message filepath, categories filepath: any valid string is acceptable
    
    outputs: datasets are merged
    """
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    
    df = messages.merge(categories, on = 'id')
    return df
    


def clean_data(df):
    """
    the function takes the dataframe and clean the incorrect rows
    
    inputs: dataframe
  
    outputs: a cleand dataframe
    """
    categories = df.categories.str.split(';', expand=True)
    row = categories.iloc[0,:]
    category_col_names = [i[:-2] for i in row]
    
    categories.columns = category_col_names
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].apply(lambda x: x[-1])

        # convert column from string to numeric
        categories[column] = categories[column].astype(int)
    
    df.drop('categories', axis = 1, inplace=True)
    
    df = pd.concat([df, categories], axis = 1)
    
    df['related'] = df['related'].map({0:0,1:1,2:1})
    
    # drop duplicates
    df.drop_duplicates(inplace= True)
    
    return df
    
def save_data(df, database_filename):
    """
    this function saves the dataframe in sql format
    
    inputs: dataframe
    
    outputs:name of the database that contains the dataframe
    """
    engine = create_engine('sqlite:///'+ database_filename)
    df.to_sql('DisRespo', engine, index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()