from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
from dotenv import load_dotenv

from app.models import Drug, MOAResponse
from app.data import get_all_moas, get_drug_by_generic_name, DRUGS_DATABASE

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Drugs MOA Quiz API",
    description="API for drug mechanism of action quiz application",
    version="1.0.0"
)

# Configure CORS - Allow React frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development server
        "http://127.0.0.1:3000",
        os.getenv("FRONTEND_URL", "http://localhost:3000")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Drugs MOA Quiz API is running",
        "endpoints": {
            "moas": "/api/drug/moa/",
            "drugs": "/api/drug/drugs/?generic=<drug_name>"
        }
    }


@app.get("/api/drug/moa/", response_model=List[MOAResponse])
def get_moas(format: Optional[str] = Query(None)):
    """
    Get all mechanisms of action

    Query Parameters:
    - format: Optional format parameter (for compatibility, not used)

    Returns:
    - List of MOA objects with id and moa fields
    """
    try:
        moas = get_all_moas()
        return moas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving MOAs: {str(e)}")


@app.get("/api/drug/drugs/", response_model=List[Drug])
def get_drugs(
    generic: Optional[str] = Query(None, description="Generic name of the drug"),
    format: Optional[str] = Query(None, description="Response format (for compatibility)")
):
    """
    Get drug information by generic name

    Query Parameters:
    - generic: Generic name of the drug (required)
    - format: Optional format parameter (for compatibility, not used)

    Returns:
    - List containing the matching drug with its MOA
    """
    if not generic:
        raise HTTPException(
            status_code=400,
            detail="Query parameter 'generic' is required"
        )

    try:
        drug = get_drug_by_generic_name(generic)

        if not drug:
            # Return empty list if drug not found (matches Django REST Framework behavior)
            return []

        # Return as list to match expected frontend format
        return [drug]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving drug information: {str(e)}"
        )


@app.get("/api/drug/drugs/all", response_model=List[Drug])
def get_all_drugs():
    """
    Get all drugs in the database

    Returns:
    - List of all drugs with their MOAs
    """
    try:
        return DRUGS_DATABASE
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving drugs: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
