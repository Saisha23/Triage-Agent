from typing import TypedDict, Literal

from pydantic import BaseModel, Field


class TriageResult(BaseModel):
    category: Literal[
        "Complaint",
        "Feedback",
        "Request",
        "Spam",
        "Other",
    ]

    priority: Literal[
        "Low",
        "Medium",
        "High",
        "Critical",
    ]

    summary: str = Field(
        min_length=1,
        max_length=500,
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    needs_human_review: bool


class ValidationResult(BaseModel):
    passed: bool

    errors: list[str] = Field(
        default_factory=list
    )

    review_reason: str = ""

    route: Literal[
        "human_review",
        "automatic_processing",
    ]


class TriageState(TypedDict, total=False):
    email: str
    triage_result: TriageResult
    validation_result: ValidationResult