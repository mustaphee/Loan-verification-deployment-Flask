from pycaret.regression import load_model, predict_model
import pandas as pd

model = load_model('trained_model')

model_columns = ['Salary', 'Total_Debit', 'Loan_Amount', 'Industry',
                 'Years_employed', 'Job_position', 'Property', 'HR_confirmation',
                 'No_of_dependents']


def predict(obj, model=model, columns=model_columns):
    # Convert the model object to a native list
    model_to_list = [field for field in obj.values()]

    # Load the list into a panda dataframe
    data_unseen = pd.DataFrame([model_to_list], columns=columns)
    prediction = predict_model(model, data=data_unseen)
    return prediction
