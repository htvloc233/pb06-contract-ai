"""AI service skeleton — W1-F01 ở mức staging: health-check + phiên bản.

Egress guard nằm cùng src/ và vào image cùng nhau: mọi call ra ngoài
sau này bắt buộc đi qua guarded_urlopen (Delegation R3, DoD-4).
"""
from fastapi import FastAPI

app = FastAPI(title="PB-06 AI Service", version="0.1.0-staging")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "pb06-ai-service",
        "version": "0.1.0-staging",
    }
