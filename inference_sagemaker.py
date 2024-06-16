import boto3
import sagemaker
from sagemaker import get_execution_role
import json

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()
role = 'arn:aws:iam::891377000396:role/SageMakerExecutionRole'
# role = get_execution_role()

# Define S3 path for the model
model_s3_path = 's3://fraudsters-detect-models/xgboost.tar.gz'

# Create a SageMaker model
model = sagemaker.model.Model(
    model_data=model_s3_path,
    role=role,
    image_uri='891377000396.dkr.ecr.eu-west-2.amazonaws.com/fruad-detect-models:latest',
    sagemaker_session=sagemaker_session
    
)

# Deploy the model
predictor = model.deploy(
    initial_instance_count=1,
    instance_type='ml.t2.medium',
    endpoint_name='xgboost-endpoint2'
)

# Example data for prediction
data = [
    { "client_id": "1", "number_of_open_accounts": 5, "total_credit_limit": 15000, "total_balance": 4532.75, "number_of_accounts_in_arrears": 1 },
    { "client_id": "2", "number_of_open_accounts": 3, "total_credit_limit": 9000, "total_balance": 1200.50, "number_of_accounts_in_arrears": 0 },
    { "client_id": "3", "number_of_open_accounts": 7, "total_credit_limit": 30000, "total_balance": 15789.95, "number_of_accounts_in_arrears": 2 },
    { "client_id": "4", "number_of_open_accounts": 2, "total_credit_limit": 5000, "total_balance": 500.00, "number_of_accounts_in_arrears": 0 },
    { "client_id": "5", "number_of_open_accounts": 6, "total_credit_limit": 20000, "total_balance": 10000.50, "number_of_accounts_in_arrears": 1 }
]

# Convert data to JSON format
payload = json.dumps(data)

# Invoke the endpoint
response = predictor.predict(payload)

# Print the response
print(response)

# Clean up (optional)
# predictor.delete_endpoint()



# ## Register the SageMaker endpoint with Application Auto Scaling
# import boto3

# client = boto3.client('application-autoscaling')

# # Register the SageMaker endpoint with Application Auto Scaling
# response = client.register_scalable_target(
#     ServiceNamespace='sagemaker',
#     ResourceId='endpoint/xgboost-endpoint/variant/AllTraffic',
#     ScalableDimension='sagemaker:variant:DesiredInstanceCount',
#     MinCapacity=1,
#     MaxCapacity=10
# )

# # Create a scaling policy
# response = client.put_scaling_policy(
#     PolicyName='InvocationsPerInstanceScalingPolicy',
#     ServiceNamespace='sagemaker',
#     ResourceId='endpoint/xgboost-endpoint/variant/AllTraffic',
#     ScalableDimension='sagemaker:variant:DesiredInstanceCount',
#     PolicyType='TargetTrackingScaling',
#     TargetTrackingScalingPolicyConfiguration={
#         'TargetValue': 50.0,  # Target number of invocations per instance
#         'PredefinedMetricSpecification': {
#             'PredefinedMetricType': 'SageMakerVariantInvocationsPerInstance'
#         },
#         'ScaleInCooldown': 300,
#         'ScaleOutCooldown': 300
#     }
# )
