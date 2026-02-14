from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
import sys


class Network_model:
    def __init__(self,preprocessor,model):
        try :
            self.preprocessor=preprocessor
            self.model=model
        except Exception as ex :
            raise NetworkSecurityException(ex,sys)
        
    def predict(self,X):
        try :
            x_transform=self.preprocessor.transform(X)
            y_pred=self.model.predict(x_transform)

            return y_pred
        except Exception as ex :
            raise NetworkSecurityException(ex,sys)
        
    