from app.persistence import save_triage_result
from app.state import TriageResult, ValidationResult


triage_result = TriageResult(
    category="Feedback",
    priority="Low",
    summary="The customer suggested adding dark mode.",
    confidence=0.95,
    needs_human_review=False,
)


validation_result = ValidationResult(
    passed=True,
    errors=[],
    review_reason="",
    route="automatic_processing",
)


email_id = save_triage_result(
    message_id="test-message-001",
    subject="Product suggestion",
    body="It would be helpful if you added dark mode.",
    triage_result=triage_result,
    validation_result=validation_result,
)


print("Saved email ID:", email_id)