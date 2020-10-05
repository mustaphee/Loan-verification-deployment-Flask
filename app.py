from flask import Flask,request, url_for, redirect, render_template, jsonify
from pycaret.regression import load_model, predict_model
import pandas as pd
import pickle
import numpy as np
import jinja2

app = Flask(__name__)

model = load_model('Final_modelr')
cols = ['Salary', 'Total_Debit', 'Loan_Amount', 'Industry',
       'Years_employed', 'Job_position', 'Property', 'HR_confirmation',
       'No_of_dependents']



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
    #loan = ' Approved ' if prediction == True else ' Rejected '
    return render_template('home.html',prediction_text='Loan Percentage is {}'.format(prediction))

@app.route('/predict_api',methods=['POST'])

def predict_api():
    data = request.get_json(force=True)
    data_unseen = pd.DataFrame([data])
    prediction = predict_model(model, data=data_unseen)
    output = prediction.Label[0]
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True,port = 5009)
