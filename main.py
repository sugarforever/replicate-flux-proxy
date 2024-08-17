from fastapi import FastAPI, HTTPException, Depends, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import httpx
from dotenv import load_dotenv

load_dotenv()

import os
REPLICATE_API_TOKEN = os.environ['REPLICATE_API_TOKEN'] 

app = FastAPI(
    title="Replicate API Proxy",
    version="1.0.0",
    servers=[{"url": "http://host.docker.internal:8000", "description": "Docker host"}]
)

security = HTTPBearer()

REPLICATE_API_BASE_URL = "https://api.replicate.com/v1"

class PredictionRequest(BaseModel):
    prompt: str = Field(..., description="The prompt for the prediction")
    output_quality: int = Field(..., ge=1, le=100, description="The output quality (1-100)")

async def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return credentials.credentials

@app.post("/predictions")
async def create_prediction(request: PredictionRequest):
    try:
        headers = {
            "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "input": {
                "prompt": request.prompt,
                "output_quality": request.output_quality
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{REPLICATE_API_BASE_URL}/models/black-forest-labs/flux-schnell/predictions",
                json=payload,
                headers=headers
            )

        return JSONResponse(content=response.json(), status_code=response.status_code)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predictions/{prediction_id}")
async def get_prediction(
    prediction_id: str = Path(..., description="The ID of the prediction to retrieve"),
):
    try:
        headers = {
            "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{REPLICATE_API_BASE_URL}/predictions/{prediction_id}",
                headers=headers
            )

        return JSONResponse(content=response.json(), status_code=response.status_code)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/openapi.json")
async def get_openapi_json():
    return JSONResponse(content=app.openapi())
