# Loan-verification-deployment-Flask
The organization wishes to automatically monitor the eligibility of a loan on the basis of client information given when filling out an electronic application form. These are gender, marital status , employment status, number of dependents, income, credit score etc.  To automate this process, they have given a solution to identify the customers segments so that they can directly target these customers to simplify this process..

I used Logistic Regression algorithm to build the machine learning model and deployed it using flask and Heroku


Prerequisites
You must have pycaret and Pandas (for Machine Leraning Model) installed on jupyter notebook and Flask (for API) installed.

Project Structure
This project has five major parts :

PREPROCESSING-New.ipynb - This contains the jupyter notebook from which the model(final_modell.pki) was created to predict if a client would default or not based on training data in ('test.xlsx') file.
app.py - This contains Flask APIs that receives clients details through GUI or API calls, computes the precited value based on our model and returns it.
templates - This folder contains the HTML template to allow user to enter clents details and displays  customers eligibility for a loan.
static - This folder contains the style.css template to give a presentable user interface.
request.py - This uses requests module to call APIs already defined in app.py and displays the returned value.
Running the project
