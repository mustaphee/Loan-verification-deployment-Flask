import requests

url = 'http://localhost:5009/predict_api'
r = requests.post(url,json={'Age':23, 'No_of_Dependents':2, 'Available_balance':100000, 'Ledger_balance':20000,
       'Gender':F, 'Occupation':Business,  'Marital_Status':Married,
       'Employment_Status':Employed, 'Education_Status':Graduate, 'Income':50000, 'Credit_score':500 , 'Loan_Amount':400000})

print(r.json())
