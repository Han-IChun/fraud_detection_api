from flask import Flask, request
from inference import InferencePipeline, XGboostModel, XGboostDataTransformor


app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    if not isinstance(data, list) or not all(isinstance(i, dict) for i in data):
        return {"error": "Input data should be a list of dictionaries."}, 400
    
    
    features, client_ids = XGboostDataTransformor().transform(data, 'xgboost')
    model_path = "./models/xgboost.json"
    # model_path = 'fraudsters-detect-models/xgboost.json'
    # it should fetche the log db and decide the model path in the future
    model = XGboostModel(model_path, location='local')  # replace with your model file path
    inference_pipeline = InferencePipeline(model)
    predictions = inference_pipeline.get_inferecne(features)

    # create dictionary of client_id and prediction
    results = [{"client_id": client_id, "prediction": float(prediction)} for client_id, prediction in zip(client_ids, predictions)]
    print(results)
    return {"results": results}, 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)