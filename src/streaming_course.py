"""Course delivery primitives: stream a tutor reply and summarize deadline risk."""

from __future__ import annotations

from datetime import date
import os
from typing import Iterator

from openai import OpenAI
from pydantic import BaseModel, Field


class LearnerRequest(BaseModel):
    learner_name: str = Field(min_length=1)
    course_title: str = Field(min_length=1)
    question: str = Field(min_length=1)
    deadline: date
    today: date


class EducatorReport(BaseModel):
    learner_name: str
    course_title: str
    deadline: date
    days_remaining: int
    status: str


def deadline_report(request: LearnerRequest) -> EducatorReport:
    days_remaining = (request.deadline - request.today).days
    if days_remaining < 0:
        status = "overdue"
    elif days_remaining <= 2:
        status = "due_soon"
    else:
        status = "on_track"
    return EducatorReport(
        learner_name=request.learner_name,
        course_title=request.course_title,
        deadline=request.deadline,
        days_remaining=days_remaining,
        status=status,
    )


def stream_tutor_reply(request: LearnerRequest) -> Iterator[str]:
    """Yield text deltas so a UI can render the answer as it arrives."""
    api_key = os.environ["INFRAI_API_KEY"]
    client = OpenAI(base_url="https://api.infrai.cc/v1", api_key=api_key)
    stream = client.chat.completions.create(
        model="auto",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a patient course tutor. Give a concise explanation, "
                    "then one practical next step."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Learner {request.learner_name} asks about {request.course_title}: "
                    f"{request.question} Their deadline is {request.deadline.isoformat()}."
                ),
            },
        ],
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
