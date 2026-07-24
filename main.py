from fastapi import FastAPI, Request, HTTPException
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from app.limiter import limiter
from pydantic import BaseModel, HttpUrl
import requests
from bs4 import BeautifulSoup
from app.cache import cache
import time
from app.logger import logger
import uuid

app = FastAPI(
    title="Page Pulse Audit API",
    description="Production-ready URL Audit Service",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Request Model
class AuditRequest(BaseModel):
    url: HttpUrl

# Root Endpoint
@app.get("/")
def home():
    return {"message": "Page Pulse Audit API is running successfully!"}

# Audit Endpoint
@app.post("/audit")
@limiter.limit("10/minute")
def audit(request: Request, body: AuditRequest):

    request_id = str(uuid.uuid4())[:8]

    url = str(body.url)

    # Check cache first
    if url in cache:

        logger.info(
            f"RequestID={request_id} | URL={url} | Cached=True"
        )

        return {
            "cached": True,
            "data": cache[url]
        }

    start_time = time.time()

    try:
        response = requests.get(url, timeout=5)

        end_time = time.time()
        response_time = round(end_time - start_time, 3)

        soup = BeautifulSoup(response.text, "html.parser")

        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else "No Title Found"
        )

        result = {
            "url": url,
            "status_code": response.status_code,
            "title": title,
            "response_time_seconds": response_time,
            "content_length": len(response.text)
        }

        # Save to cache
        cache[url] = result

        logger.info(
            f"RequestID={request_id} | URL={url} | "
            f"Status={response.status_code} | "
            f"ResponseTime={response_time}s | Cached=False"
        )

        return {
            "cached": False,
            "data": result
        }

    except requests.exceptions.Timeout:
        logger.error(
            f"RequestID={request_id} | URL={url} | Timeout"
        )
        raise HTTPException(
            status_code=408,
            detail="Request timed out"
        )

    except requests.exceptions.RequestException as e:
        logger.error(
            f"RequestID={request_id} | URL={url} | Error={str(e)}"
        )
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )