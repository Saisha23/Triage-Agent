from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.graph import graph
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import get_db
from app.models import Email, TriageRecord

from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel

from app.models import Email, TriageRecord


app = FastAPI(
    title="AI Email Triage API",
    version="1.0.0"
)


class EmailRequest(BaseModel):
    subject: str = Field(min_length=1)
    email: str = Field(min_length=1)

class ReviewRequest(BaseModel):
    email_id: UUID
    status: str
    reviewer_note: str | None = None


@app.get("/")
def home():
    return {
        "message": "AI Email Triage API is running"
    }


@app.post("/triage")
def triage_email(request: EmailRequest):
    result = graph.invoke({
        "subject": request.subject,
        "email": request.email
    })

    triage_result = result.get("triage_result")
    validation_result = result.get("validation_result")

    return {
        "category": triage_result.category,
        "priority": triage_result.priority,
        "summary": triage_result.summary,
        "confidence": triage_result.confidence,
        "needs_human_review": triage_result.needs_human_review,
        "validation_passed": validation_result.passed,
        "route": validation_result.route,
        "review_reason": validation_result.review_reason
    }

@app.get("/emails")
def get_emails(db: Session = Depends(get_db)):
    emails = db.query(Email).order_by(
        Email.received_at.desc()
    ).all()

    results = []

    for email in emails:
        triage = email.triage_result

        results.append({
            "id": str(email.id),
            "message_id": email.message_id,
            "subject": email.subject,
            "body": email.body,
            "received_at": email.received_at,
            "category": triage.category if triage else None,
            "priority": triage.priority if triage else None,
            "summary": triage.summary if triage else None,
            "confidence": triage.confidence if triage else None,
            "route": triage.route if triage else None,
            "needs_human_review": (
                triage.needs_human_review
                if triage else None
            )
        })

    return {
        "count": len(results),
        "emails": results
    }

@app.get("/review-queue")
def get_review_queue(db: Session = Depends(get_db)):
    emails = (
        db.query(Email)
        .join(Email.triage_result)
        .filter(TriageRecord.route == "human_review",
                TriageRecord.review_status == "pending")
        .order_by(Email.received_at.desc())
        .all()
    )

    results = []

    for email in emails:
        triage = email.triage_result

        results.append({
            "id": str(email.id),
            "subject": email.subject,
            "body": email.body,
            "category": triage.category,
            "priority": triage.priority,
            "summary": triage.summary,
            "confidence": triage.confidence,
            "review_reason": (
                "Requires human review"
                if triage.needs_human_review
                else "Validation rule triggered"
            ),
        })

    return {
        "count": len(results),
        "review_queue": results,
    }

@app.post("/review")
def review_email(
    request: ReviewRequest,
    db: Session = Depends(get_db)
):
    if request.status not in ["approved", "rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be 'approved' or 'rejected'."
        )

    email = db.query(Email).filter(
        Email.id == str(request.email_id)
    ).first()

    if email is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found."
        )

    triage = email.triage_result

    if triage is None:
        raise HTTPException(
            status_code=404,
            detail="Triage record not found."
        )

    if triage.route != "human_review":
        raise HTTPException(
            status_code=400,
            detail="Only emails in human review can be reviewed."
        )

    triage.review_status = request.status
    triage.reviewer_note = request.reviewer_note

    db.commit()
    db.refresh(triage)

    return {
        "message": "Review updated successfully.",
        "email_id": str(email.id),
        "review_status": triage.review_status,
        "reviewer_note": triage.reviewer_note
    }