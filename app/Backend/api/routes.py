from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select, text
from sqlalchemy.orm import Session

try:
    from ..db import Submission, get_db
except ImportError:
    from db import Submission, get_db


router = APIRouter(prefix="/api", tags=["api"])


class SubmissionCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=180)
    message: str = Field(min_length=2, max_length=1000)


class SubmissionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    email: str | None = Field(default=None, min_length=5, max_length=180)
    message: str | None = Field(default=None, min_length=2, max_length=1000)


class SubmissionRead(BaseModel):
    id: int
    name: str
    email: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/health")
def health_check(db: Session = Depends(get_db)) -> dict:
    db.execute(text("SELECT 1"))
    return {
        "status": "ok",
        "service": "fastapi",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.post("/submissions", response_model=SubmissionRead, status_code=status.HTTP_201_CREATED)
def create_submission(payload: SubmissionCreate, db: Session = Depends(get_db)) -> Submission:
    submission = Submission(**payload.model_dump())
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@router.get("/submissions", response_model=list[SubmissionRead])
def list_submissions(db: Session = Depends(get_db)) -> list[Submission]:
    statement = select(Submission).order_by(Submission.id.desc())
    return list(db.execute(statement).scalars().all())


@router.get("/submissions/{submission_id}", response_model=SubmissionRead)
def get_submission(submission_id: int, db: Session = Depends(get_db)) -> Submission:
    submission = db.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission


@router.put("/submissions/{submission_id}", response_model=SubmissionRead)
def update_submission(
    submission_id: int,
    payload: SubmissionUpdate,
    db: Session = Depends(get_db),
) -> Submission:
    submission = db.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(submission, key, value)

    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@router.delete("/submissions/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_submission(submission_id: int, db: Session = Depends(get_db)) -> None:
    submission = db.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    db.delete(submission)
    db.commit()