import os,sys
import numpy as np 
from Network_Security.entity.config_entity import ModelTrainerConfig
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.entity.artifact_config import ModelTrainerArtifact,ClassificationMetricArtifact,DataTranformationArtifact
from Network_Security.utils.main.utils import load_numpy_array,load_object,save_object,evaluate_model
from Network_Security.utils.ml_utils.metric.classifiaction_report import get_classification_report
from Network_Security.utils.ml_utils.model.estimator import Network_model
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    RandomForestClassifier,
    GradientBoostingClassifier
)
import mlflow
import dagshub
dagshub.init(repo_owner='rajsengar1804', repo_name='NetworkSecurity', mlflow=True)

class ModelTrainer:
    def __init__(self,datatransformationartifact:DataTranformationArtifact
                 ,modeltrainerconfig:ModelTrainerConfig):
        try :
            self.datatransformationartifact=datatransformationartifact
            self.modeltrainerconfig=modeltrainerconfig
        except Exception as ex :
            raise NetworkSecurityException(ex,sys)
    def track_mlflow(self,best_model,classificationmetric):
        with mlflow.start_run() :
            f1_score=classificationmetric.f1_score
            precision_score=classificationmetric.precision_score
            recall_score=classificationmetric.recall_score
            mlflow.log_metric("fl_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model, artifact_path="model")

        
    def trainmodel(self,x_train,y_train,x_test,y_test):
          try :
            models = {
                    "Random Forest": RandomForestClassifier(verbose=1),
                    "Decision Tree": DecisionTreeClassifier(),
                    "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                    "Logistic Regression": LogisticRegression(verbose=1),
                    "AdaBoost": AdaBoostClassifier(),
                }
            params={
                "Random Forest":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,256]
                },
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Gradient Boosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,64,128,256]
                }
            }
            model_report:dict =evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,
                                                models=models,params=params)
            logging.info(f"evaluation is done  {model_report}")
            best_models=max(sorted(model_report.values()))
            best_models_name=list(model_report.keys())[
                list(model_report.values()).index(best_models)
            ]
            model=models[best_models_name]
            model.fit(x_train,y_train)
            y_train_pred=model.predict(x_train)

            classifiaction_report_train=get_classification_report(y_true=y_train,y_pred=y_train_pred)
            self.track_mlflow(best_model=best_models,classificationmetric=classifiaction_report_train)
            logging.info("mlflow track for training is done")

            y_test_pred=model.predict(x_test)
            classifiaction_report_test=get_classification_report(y_true=y_test,y_pred=y_test_pred)
            self.track_mlflow(best_model=best_models,classificationmetric=classifiaction_report_train)
            logging.info("mlflow track  for test is done")
            preprocessor=load_object(filepath=self.datatransformationartifact.preprocessor_pickle_filepath)
            network_obj=Network_model(model=model,preprocessor=preprocessor)
            dir_path=os.path.dirname(self.modeltrainerconfig.modeltrainer_trained_filepath)
            os.makedirs(dir_path,exist_ok=True)
            save_object(file_path=self.modeltrainerconfig.modeltrainer_trained_filepath,obj=network_obj)
            #model pusher
            save_object("final_model/model.pkl", network_obj)
            return ModelTrainerArtifact(
                trained_model_file_path=self.modeltrainerconfig.modeltrainer_trained_filepath,
                train_metric_artifact=classifiaction_report_train,
                test_metric_artifact=classifiaction_report_test
            )
          except Exception as ex :
              raise NetworkSecurityException(ex,sys)
    

    def intiate_model_trainer(self):
        try :
            train_arr_filepath=self.datatransformationartifact.train_numpy_array_filepath
            test_arr_filepath=self.datatransformationartifact.test_numpy_array_filepath
            train_arr=load_numpy_array(filepath=train_arr_filepath)
            test_arr=load_numpy_array(filepath=test_arr_filepath)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )
            modeltrainerartifacts=self.trainmodel(x_train,y_train,x_test,y_test)

            return modeltrainerartifacts
                
        except Exception as ex :
            raise NetworkSecurityException(ex,sys)
    


