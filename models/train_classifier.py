import sys
import pandas as pd
from sqlalchemy import create_engine
import re
import nltk
nltk.download(['punkt', 'wordnet'])
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
import pickle


def load_data(database_filepath):    
    """
    This function takes the database file path as an attribute and 
    return messages and category names
    """
    engine = create_engine('sqlite:///' + database_filepath)
    df = pd.read_sql('DisRespo', engine)
    
    X = df['message']
    Y = df.drop(['id', 'message', 'original', 'genre'],axis=1)
    category_names = Y.columns
    return X, Y, category_names


def tokenize(text):
    """
    This function takes the text and process it into a list of cleand tokens
    
    inputs: the text that the user want to process
    
    outputs: list of tokens
    """
    text= re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    
    
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    
    
    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)
        
    return clean_tokens


def build_model():
    
    """
    this function generates a model after doing a pipeline for gridSearch
   
    """
    model = Pipeline([
    ('vect', CountVectorizer(tokenizer=tokenize)),
    ('tfidf', TfidfTransformer()),
    ('clf', MultiOutputClassifier(RandomForestClassifier())
    ])
    
    parameters = {
    'tfidf__norm':['l2','l1'],
    'clf__estimator__min_samples_split':[2,3],
    }
    
    cv = GridSearchCV(model, parameters, n_jobs=-1)
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    """
    this function print the classification report after predicting the categories of the messages
   
    """
    y_pred = model.predict(X_test)
    
    
    for i,column in enumerate(Y_test.columns):
        print('------------------------------------------------------\n')
        print('FEATURE: {}\n'.format(column))
        print(classification_report(Y_test.iloc[:,i],y_pred[:,i]))


def save_model(model, model_filepath):
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE:{}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()