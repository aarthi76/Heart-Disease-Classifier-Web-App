# -*- coding: utf-8 -*-

import numpy as np
import pickle
from flask import Flask, request, render_template

import requests

# NOTe: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "8JP2BB-2ltyVKJZKGmMTNclmJSVFksALOtS_-JkB7jzB"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTe: manually define and pass the array(s) of values to be scored in the next line

# Load ML model
#model = pickle.load(open('model.pkl', 'rb')) 

# Create application
app = Flask(__name__)

# Bind home function to URL
@app.route('/')
def home():
    return render_template('Heart Disease Classifier.html')

# Bind predict function to URL
@app.route('/predict', methods =['POST'])
def predict():
    
    # Put all form entries values in a list 
    features = [float(i) for i in request.form.values()]
    # Convert features to array
    array_features = [np.array(features)]
    print(array_features)
    payload_scoring = {"input_data": [{"fields": [["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"]], "values": [features]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/3cc1bb84-6f82-4c57-a9f4-bed1a1a6fbcc/predictions?version=2022-11-24', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    prediction = response_scoring.json()
    print(prediction)
    # Predict features
    #prediction = model.predict(array_features)
    
    output = prediction['predictions'][0]['values'][0][0]
    
    # Check the output values and retrive the result with html tag based on the value
    if output == 1:
        return render_template('Heart Disease Classifier.html', 
                               result = 'The patient is not likely to have heart disease!')
    else:
        return render_template('Heart Disease Classifier.html', 
                               result = 'The patient is likely to have heart disease!')


if __name__ == '__main__':
#Run the application
    app.run()