import requests

url = 'http://localhost:5001/predict_api'
r = requests.post(url,json={'Age':23, 'No_of_Dependents':2, 'Available_balance':100000, 'Ledger_balance':20000,
       'Gender':1, 'Occupation':2, 'Location':1, 'Marital_Status':2,
       'Employment_Status':1, 'Education_Status':1, 'Houseownership':1,
       'CarOwnership':1, 'Income':1, 'Coapplicant_Income':1, 'Credit_score':1})

print(r.json())
