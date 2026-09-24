from app.database import SessionLocal
from app.models import Email, TriageRecord


db = SessionLocal()

try:
    emails = db.query(Email).order_by(
        Email.received_at.desc()
    ).limit(5).all()

    print(f"Found {len(emails)} email(s).\n")

    for email in emails:
        print("=" * 50)
        print("Email ID:", email.id)
        print("Message ID:", email.message_id)
        print("Subject:", email.subject)
        print("Body:", email.body)

        if email.triage_result:
            result = email.triage_result

            print("\nTriage Result:")
            print("Category:", result.category)
            print("Priority:", result.priority)
            print("Summary:", result.summary)
            print("Confidence:", result.confidence)
            print("Human Review:", result.needs_human_review)
            print("Validation Passed:", result.validation_passed)
            print("Route:", result.route)

finally:
    db.close()