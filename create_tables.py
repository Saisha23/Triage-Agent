from sqlalchemy import text

from app.database import Base, engine
from app import models
from app.models import TriageRecord




print("Creating database tables...")

Base.metadata.create_all(bind=engine)

# Get the actual table name from the SQLAlchemy model
table_name = TriageRecord.__table__.name

print(f"Updating table: {table_name}")

with engine.begin() as connection:
    connection.execute(
        text(f"""
            ALTER TABLE "{table_name}"
            ADD COLUMN IF NOT EXISTS review_status
            VARCHAR(20) NOT NULL DEFAULT 'pending';
        """)
    )

    connection.execute(
        text(f"""
            ALTER TABLE "{table_name}"
            ADD COLUMN IF NOT EXISTS reviewer_note
            TEXT;
        """)
    )

print("Database tables created/updated successfully.")