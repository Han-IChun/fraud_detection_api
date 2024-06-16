## To use this repository, please follow the instructions below:
There three ways of test the inferecne API:
1. Run Flask API locally.
    1. Unzip the file and navigate to the extracted directory.
    2. install dependencies in requirements.txt 
    3. Run the `inference_api.py` file. This will launch a Flask API.
    4. You can test the API by sending requests to `http://127.0.0.1:5000` with an example payload.

2. If you prefer to use Docker, you can download the Docker files from a container registry. AWS ECR image URI: `891377000396.dkr.ecr.eu-west-2.amazonaws.com/flask-fraud_detecotr-xgb:latest`.
    1. Once you have the Docker image, run the container. Make sure to expose port 8000.
    2. You can test the API by sending requests to `http://127.0.0.1:8000` with an example payload. 
3. You can use the ready APIs I built with AWS Application Load Balancer and ECS. 
    1. API: `http://fraud-alb-1112019979.eu-west-2.elb.amazonaws.com/predict`
    2. You do not need any credential to access the API for the sake of test.
    3. Request the API with the example request format below. 



Please note that additional setup steps or dependencies may be required. 
## Example request and response
An example request body
```json
[
    { "client_id": "1",
      "number_of_open_accounts": 5,
      "total_credit_limit": 15000,
      "total_balance": 4532.75,
      "number_of_accounts_in_arrears": 1
    },
    {
      "client_id": "2",
      "number_of_open_accounts": 3,
      "total_credit_limit": 9000,
      "total_balance": 1200.50,
      "number_of_accounts_in_arrears": 0
    },
    {
      "client_id": "3",
      "number_of_open_accounts": 7,
      "total_credit_limit": 30000,
      "total_balance": 15789.95,
      "number_of_accounts_in_arrears": 2
    },
    {
      "client_id": "4",
      "number_of_open_accounts": 2,
      "total_credit_limit": 5000,
      "total_balance": 500.00,
      "number_of_accounts_in_arrears": 0
    },
    {
      "client_id": "5",
      "number_of_open_accounts": 6,
      "total_credit_limit": 20000,
      "total_balance": 10000.50,
      "number_of_accounts_in_arrears": 1
    }
  ]
  
```


An example response
```json
{
    "results": [
        {
            "client_id": "1",
            "prediction": 0.0
        },
        {
            "client_id": "2",
            "prediction": 0.0
        },
        {
            "client_id": "3",
            "prediction": 0.0
        },
        {
            "client_id": "4",
            "prediction": 0.0
        },
        {
            "client_id": "5",
            "prediction": 0.0
        }
    ]
}
```

## Ohter files
- `inference.py` ## inference.py

The `inference.py` file is a key part of our application. It contains the `InferencePipeline` and `Model` classes, which are used to load a trained machine learning model and make predictions with it.

The `Model` class is an abstract base class that defines the interface for a machine learning model. It includes methods for loading a model from a file and making predictions with the model.

The `InferencePipeline` class uses an instance of the `Model` class to make predictions. It takes in raw data, transforms it into the format expected by the model, passes it to the model for prediction, and then transforms the model's output into a more usable format.

In our application, we use a subclass of `Model` to load an XGBoost model and make predictions with it. This subclass, `XGBoostModel`, is defined in the same file. It overrides the `load_model` and `infer_model` methods of the `Model` class to load an XGBoost model from a file and make predictions with it, respectively.

The `inference.py` file is used by our Flask application to make predictions in response to HTTP requests. When the Flask application receives a POST request at the `/predict` endpoint, it uses the `InferencePipeline` and `XGBoostModel` classes to make a prediction and returns the prediction in the response.
- `unit_test.py` is to test if the model load and run correctly. You do not need it to run the API. 
- `inference_sagemaker.py` is a Python script to register and deloy a model to AWS SageMaker. The script is under development. It can not use it straight. It show case the high level process of it.
