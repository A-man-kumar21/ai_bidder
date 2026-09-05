from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .scoring import ADAPTERS, evaluate_bidder

app = FastAPI(title="GeM Bid Compliance AI Engine", version="0.1.0")


class ComplianceRequest(BaseModel):
    bidder_id: str = Field(min_length=1, examples=["BIDDER-ALPHA"])
    required_checks: list[str] = Field(min_length=1, examples=[["udyam", "gstn", "pan_it", "epfo_esic", "digilocker", "blacklist"]])


@app.get("/health")
def health() -> dict:
    return {"service": "ai-engine", "status": "ready"}


@app.post("/verify-compliance")
def verify_compliance(request: ComplianceRequest) -> dict:
    unknown_sources = sorted(set(request.required_checks) - set(ADAPTERS))
    if unknown_sources:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported required checks: {', '.join(unknown_sources)}",
        )
    return evaluate_bidder(request.bidder_id, request.required_checks)
