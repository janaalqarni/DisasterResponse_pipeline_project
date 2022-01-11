# Disaster Respone Pipeline Project

# Project Summary
This project is to analyze messages for disaster respone according to the data that were givin by Figure Eight. This data was givin ti build an API classifire to classifiy disaster messages into 36 category. The goal is to classify new messages to the correct agency so they can take actions. This is a project for Udacity Data Scientist Naonodegree program.
# Components 
```
- app
| - template
| |- master.html  # main page of web app
| |- go.html  # classification result page of web app
|- run.py  # Flask file that runs app

- data
|- disaster_categories.csv  # categories data to process 
|- disaster_messages.csv  # messages data to process
|- process_data.py        # cleaning the data

- models
|- train_classifier.py # model


- README.md
```
# Results
![newplot](https://user-images.githubusercontent.com/63798019/148662726-47a5aea6-eea5-404a-8abd-6074490cb4f6.png)
We can see here the 36 categories that were classified using this model
![newplot (1)](https://user-images.githubusercontent.com/63798019/148662738-30a22fcb-3415-43ef-a60c-e3c8fad788e4.png)
and here the distribution of message genres

# How To Run The Web
1. Run the following commands in the project's root directory to set up your database and model.
      - To run ETL pipeline that cleans data and stores in database `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
      - To run ML pipeline that trains classifier and saves python `models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app. 
python run.py

3. Go to http://0.0.0.0:3001/

### Dependencies
  - Machine Learning Libraries: Numpy, Pandas, Sklearn
  - Natural Language Process Libraries: NLTK
  - SQLlite Database Libraries: SQLalchemy
  - Web App and Data Visualization: Flask, Plotly
