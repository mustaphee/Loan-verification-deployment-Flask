from typing import Optional
import os

from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel, validator, Field
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, HTMLResponse
from . import model


PASSWORD = '322e3df8cuvjvrjgdhxccecqwefctcgfsadfwe34gvr'

app = FastAPI(
    title="Touchcore: Loan Score Prediction Engine",
    description="This is the loan prediction engine based on model X",
    version="1.0.0")


class PredictionSchema(BaseModel):
    salary: float = Field(..., ge=1, le=1000000,
                          description='`salary` can only be between 1 and 1000000')
    total_debit: float = Field(
        0, ge=0, le=1500000, description='`total_debit` can only be between 0 and 1500000')
    loan_amount: float = Field(..., ge=500, le=2000000,
                               description='`loan_amount` can only be between 500 and 2000000')
    industry: str = Field(..., description='Allowed values are A..to..E')
    years_employed: int = Field(..., ge=0,
                                description='`year_employed` cannot be negative')
    job_position: str = Field(
        ..., description="Allowed value are 'Senior', 'Midlevel', 'Junior', 'Intern'")
    property: str = Field(..., description='Allowed values are M..to..P')

    hr_confirmation: bool = Field(..., description='true or false')
    no_of_dependents: int = Field(..., ge=0, lt=6,
                                  description='`no_of_dependents` can only be between 0 and 5')

    @validator('job_position')
    def job_position_(cls, val):
        allowed_position = ['Senior', 'Midlevel', 'Junior', 'Intern']
        assert val in allowed_position, '`job_position`must be one of ' + \
            ' '.join(allowed_position)
        return val

    @validator('industry')
    def industry_(cls, val):
        allowed_industry = ['A', 'B', 'C', 'D', 'E']
        assert val in allowed_industry, '`industry` can only be A, B, C, D or E'
        return val

    @validator('property')
    def property_(cls, val):
        allowed_property = ['M', 'N', 'O', 'P']
        assert val in allowed_property, '`property` can only be M, N, O, P'
        return val

    @validator('hr_confirmation')
    def hr_(cls, val):
        assert type(val) is bool, '`hr_confirmation` can only be true or false'
        return 'Yes' if val else 'No'

    class Config:
        title: 'Predict Loan Score'
        description: 'Predicts loan score from input data'
        schema_extra = {
            "example": {
                "salary": 1000000,
                "total_debit": 1000000,
                "loan_amount": 50000,
                "industry": "A",
                "years_employed": 5,
                "job_position": "Senior",
                "property": "M",
                "hr_confirmation": True,
                "no_of_dependents": 0
            },
        }


class ResponseData(BaseModel):
    prediction_score: int
    raw_output: dict


class BaseResponseSchema(BaseModel):
    status: str = 'success'
    data: dict
    message: str = 'Welcome Home'


class PredictionResponseSchema(BaseResponseSchema):
    status: str = 'success'
    data: ResponseData
    message: str = 'Prediction successful'

#  Override FASTAPI default error handler to match TC's response format


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(exc)
    error_content = exc.errors()
    error_msg = error_content[0]['msg']
    error_loc = error_content[0]['loc'][1]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {'status': 'fail', 'error': error_content,
                'message': f'Validation error: `{error_loc}` -> {error_msg} '}
        )
    )


@ app.get('/', response_model=BaseResponseSchema)
def home():
    return {'status': 'success', 'message': 'Welcome Home', 'data': {}}


@ app.post('/api/v1/predict', response_model=PredictionResponseSchema)
def predict_loan_score(data: PredictionSchema):
    prediction = model.predict(data.dict())
    response = {"prediction_score": float(
        prediction.Label[0]), "raw_output": prediction.to_dict('records')[0]}
    return {'status': 'success', 'data': response, 'message': 'Prediction successful'}


@app.get("/upload")
async def upload_model():
    content = """
        <body>
            <form action="/files/" enctype="multipart/form-data" method="post">
                <label for"passwordField">Password</label>
                <input id="passwordField" name="password" type="text">
                <input id="fileField" name="file" type="file">
            <input type="submit">
            </form>
        </body>
    """
    return HTMLResponse(content=content)


@app.post("/files/")
async def setup_model_files(password: str = Form(...), file: UploadFile = File(...)):
    if password != PASSWORD:
        return {'status': 'fail', 'error': {'msg': 'AUTH_FAILED'}, 'message': 'Incorrect Password'}

    if file.filename.endswith('.pkl') is not True and file.content_type != 'application/octet-stream':
        return {'status': 'fail', 'error': {'msg': 'INVALID_FILE'}, 'message': 'You can only upload a valid pickle model'}

    content = await file.read()

    with open('trained_model.pkl', 'wb') as newmodel:
        newmodel.write(content)

    return {'status': 'success', 'data': {'file_size': str(file.spool_max_size/10000)+'mb',
                                          'file_name': file.filename}, 'message': 'Model uploaded successfully'}

    # TODO: Kill this current process with SIGINT and allow pm2 or the process manager to restart it and reload the new model
    # TODO: Or create the import model as a singleton object and reload it when a new model is uploaded
