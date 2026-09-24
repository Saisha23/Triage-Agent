
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    message_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    triage_result: Mapped["TriageRecord | None"] = relationship(
        back_populates="email",
        uselist=False,
        cascade="all, delete-orphan",
    )


class TriageRecord(Base):
    __tablename__ = "triage_results"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    email_id: Mapped[str] = mapped_column(
        ForeignKey("emails.id"),
        unique=True,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    needs_human_review: Mapped[bool] = mapped_column(
        nullable=False,
    )

    validation_passed: Mapped[bool] = mapped_column(
        nullable=False,
    )

    route: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    email: Mapped[Email] = relationship(
        back_populates="triage_result",
    )

    review_status = Column(
    String(20),
    default="pending",
    nullable=False
    )

    reviewer_note = Column(
        Text,
        nullable=True
    )