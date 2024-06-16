import xgboost as xgb
from abc import ABC, abstractmethod
from s3fs.core import S3FileSystem
import xgboost as xgb



class dataTransformer:
    @abstractmethod
    def transform(self, data, model_type):
        pass

class XGboostDataTransformer(dataTransformer):
    def transform(self, data, model_type):
        if model_type == 'xgboost':
            client_ids = []
            features = []
            for client in data:
                features.append(list(client.values())[1:])
                client_ids.append(client["client_id"])
        else:
            raise ValueError('Model type not supported')
        return features, client_ids

class InferencePipeline:
    def __init__(self, model):
        self.model = model

    def get_inferecne(self, data):
        return self.model.infer_model(data)
    

class Model:
    @abstractmethod
    def load_model(self):
        pass
    @abstractmethod
    def infer_model(self, data):
        pass


class XGboostModel(Model):
    def __init__(self, model_path, location='s3'):
        # self.model_name = model_name
        self.model_path = model_path
        self.location = location
        
    def load_model(self):
        model = xgb.XGBClassifier()
        if self.location == 's3':
            fs = S3FileSystem()
            with fs.open(self.model_path, mode='rb') as f:
                model.load_model(bytearray(f.read()))
        elif self.location == 'local':
            model.load_model(self.model_path)
        else:
            raise ValueError('Location not supported')
        return model

    # inference output  from xgboost model
    def infer_model(self, data):
        model = self.load_model()
        return model.predict(data)      



