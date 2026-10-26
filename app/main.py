
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from app.reviewer import review_code
from app.schemas import CodeReviewRequest, ReviewResult


app = FastAPI(
    title="GitHub AI Code Review Bot",
    description="AI-powered code review using a local Ollama model.",
    version="0.1.0",
)


@app.get("/")
async def home():
    return {
        "message": "GitHub AI Code Review Bot is running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model": "qwen2.5:7b",
    }


@app.post("/review", response_model=ReviewResult)
async def review(request: CodeReviewRequest):
    try:
        return await review_code(
            code=request.code,
            language=request.language,
        )

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "Could not communicate with Ollama. "
                "Check that Ollama is running and the model is available."
            ),
        ) from exc

    except (ValidationError, KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="The AI returned an invalid review response.",
        ) from exc
