from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import json
import os

app = FastAPI(title="Fraud Detection Routing API")

# Initialize the AWS SDK client for SageMaker
# It will automatically inherit permissions from the EKS cluster later
sagemaker_client = boto3.client('sagemaker-runtime', region_name='ap-south-1')

# Define the expected incoming transaction data structure
class TransactionData(BaseModel):
    amount: float
    time: int
    # Add other teammate's features here later (e.g., location_code: int)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running."}

@app.post("/predict")
def predict_fraud(transaction: TransactionData):
    try:
        # 1. Format the payload for the ML model (CSV is standard for XGBoost)
        payload = f"{transaction.amount},{transaction.time}"
        
        # We will pass the endpoint name as an environment variable in Kubernetes
        endpoint_name = os.getenv("SAGEMAKER_ENDPOINT_NAME", "fraud-detection-endpoint")

        # 2. Securely invoke the isolated SageMaker model
        response = sagemaker_client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='text/csv',
            Body=payload
        )

        # 3. Parse the prediction returned by the model
        result = json.loads(response['Body'].read().decode())
        prediction_score = float(result[0])
        
        # Categorize the transaction based on a 0.5 threshold
        is_fraud = bool(prediction_score > 0.5)

        return {
            "transaction_action": "BLOCKED" if is_fraud else "APPROVED",
            "fraud_probability_score": prediction_score
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))