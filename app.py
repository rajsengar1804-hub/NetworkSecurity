import os ,sys
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from Network_Security.pipeline.training_pipeline import Training_pipeline
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.utils.main.utils import load_object
from Network_Security.utils.ml_utils.model.estimator import Network_model

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")
app=FastAPI()
origins=["*"]

app.add_middleware(
     CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")
@app.get('/train')
async def train_route():
    try :
        logging.info("training is start")
        training=Training_pipeline()
        training.run_pipeline()
        logging.info("training is done")
        return Response("training is sucessfull")
    except Exception as ex :
        raise NetworkSecurityException(ex,sys)
@app.post('/predict')
async def predict_route(request:Request,file :UploadFile=File(...)):
    try :
        logging.info("prediction is start")
        df=pd.read_csv(file.file)
        preprocessor=load_object("final_model/preprocessor.pkl")
        model=load_object("final_model/model.pkl")
        network=Network_model(model=model,preprocessor=preprocessor)
        y_pred=network.predict(X=df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        logging.info(f"prediction is done ={len(y_pred)}")
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as ex :
        raise NetworkSecurityException(ex,sys)
    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)