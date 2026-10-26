
from typing import Literal

from pydantic import BaseModel, Field


Severity = Literal["critical", "high", "medium", "low", "info"]

Category = Literal[
    "bug",
    "security",
    "performance",
    "maintainability",
    "style",
    "other",
]


class ReviewFinding(BaseModel):
    """One issue discovered during code review."""

    severity: Severity
    category: Category
    title: str = Field(min_length=1, max_length=200)
    explanation: str = Field(min_length=1)
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)
    suggestion: str | None = None


class ReviewResult(BaseModel):
    """The complete result returned by the AI reviewer."""

    summary: str
    findings: list[ReviewFinding]


class CodeReviewRequest(BaseModel):
    """Input received by our API."""

    code: str = Field(min_length=1, max_length=30000)
    language: str = Field(default="python", min_length=1, max_length=50)
