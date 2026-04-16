import os
import boto3
import joblib
import pandas as pd
import xgboost as xgb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="Fraud Detection API")

# Configuration from your Terraform/S3 setup
BUCKET_NAME = "fraud-detection-ml-data-20260416135324109200000004"
MODEL_KEY = "v1/model.ubj"
ENCODER_PATH = "v1/encoders/"
THRESHOLD_KEY = "v1/threshold.txt"

# Global variables to hold our "Brain"
model = None
encoders = {}
threshold = 0.5
model_features = []

def download_s3_artifacts():
    global model, encoders, threshold, model_features
    s3 = boto3.client('s3')
    
    print("--- Downloading Artifacts from S3 ---")
    
    # 1. Load Model
    s3.download_file(BUCKET_NAME, MODEL_KEY, "model.ubj")
    model = xgb.XGBClassifier()
    model.load_model("model.ubj")
    model_features = model.get_booster().feature_names
    
    # 2. Load Threshold
    s3.download_file(BUCKET_NAME, THRESHOLD_KEY, "threshold.txt")
    with open("threshold.txt", "r") as f:
        threshold = float(f.read().strip())
        
    # 3. Load the 5 Encoders
    encoder_files = [
        "encoder_card4.pkl", "encoder_card6.pkl", "encoder_M6.pkl",
        "encoder_P_emaildomain.pkl", "encoder_ProductCD.pkl"
    ]
    
    for enc_file in encoder_files:
        local_path = f"enc_{enc_file}"
        s3.download_file(BUCKET_NAME, f"{ENCODER_PATH}{enc_file}", local_path)
        # Mapping the file name to the column name it handles
        col_name = enc_file.replace("encoder_", "").replace(".pkl", "")
        encoders[col_name] = joblib.load(local_path)
    
    print("--- All Systems Nominal: Model Ready ---")

@app.on_event("startup")
async def startup_event():
    download_s3_artifacts()

class Transaction(BaseModel):
    # This should match the raw data fields before preprocessing
    data: Dict[str, Any]

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
async def predict(transaction: Transaction):
    try:
        # 1. Convert input to DataFrame
        df = pd.DataFrame([transaction.data])
        
        # 2. Preprocessing: Apply the pre-saved encoders
        for col, encoder in encoders.items():
            if col in df.columns:
                # Use .transform(), NOT .fit_transform()
                # Handle unknown values by converting to string first
                df[col] = encoder.transform(df[col].astype(str))
        
        # 3. Handle Missing Values (using median fallback or 0)
        # In a pro setup, you'd pull medians from S3 too. 
        # For now, we align with model features and fill 0
        df = df.reindex(columns=model_features, fill_value=0)
        
        # 4. Inference
        prob = float(model.predict_proba(df)[0][1])
        prediction = 1 if prob >= threshold else 0
        
        return {
            "is_fraud": bool(prediction),
            "confidence": round(prob * 100, 2),
            "threshold_used": threshold
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))