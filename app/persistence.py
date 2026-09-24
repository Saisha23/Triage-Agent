from app.database import SessionLocal
from app.models import Email, TriageRecord


def save_triage_result(
    message_id: str,
    subject: str,
    body: str,
    triage_result,
    validation_result,
):
    db = SessionLocal()

    try:
        # Create the email record
        email_record = Email(
            message_id=message_id,
            subject=subject,
            body=body,
        )

        db.add(email_record)
        db.flush()

        # Create the triage result record
        triage_record = TriageRecord(
            email_id=email_record.id,
            category=triage_result.category,
            priority=triage_result.priority,
            summary=triage_result.summary,
            confidence=triage_result.confidence,
            needs_human_review=triage_result.needs_human_review,
            validation_passed=validation_result.passed,
            route=validation_result.route,
        )

        db.add(triage_record)
        db.commit()

        print("Email and triage result saved successfully.")

        return email_record.id

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()