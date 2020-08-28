from flask import Flask,request, url_for, redirect, render_template, jsonify
from pycaret.classification import *
import pandas as pd
import pickle
import numpy as np
import jinja2


app = Flask(__name__)

model = load_model('Final_modell')
cols = ['Age', 'No_of_Dependents', 'Available_balance', 'Ledger_balance',
       'Gender', 'Occupation', 'Location', 'Marital_Status',
       'Employment_Status', 'Education_Status', 'Houseownership',
       'CarOwnership', 'Income', 'Coapplicant_Income', 'Credit_score']

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict',methods=['POST'])
def predict():
    int_features = [x for x in request.form.values()]
    final = np.array(int_features)
    data_unseen = pd.DataFrame([final], columns = cols)
    prediction = predict_model(model, data=data_unseen)
    prediction = int(prediction.Label[0])
    return render_template('home.html',prediction_text='THE OUTPUT is {}'.format(prediction))


@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    data_unseen = pd.DataFrame([data])
    prediction = predict_model(model, data=data_unseen)
    output = prediction.Label[0]
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True ,port = 5001)