from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from src.streaming_course import LearnerRequest, deadline_report, stream_tutor_reply


def test_deadline_report_marks_two_day_window_due_soon() -> None:
    request = LearnerRequest(
        learner_name="Ari",
        course_title="Data literacy",
        question="How should I check a chart?",
        deadline=date(2026, 9, 11),
        today=date(2026, 9, 9),
    )

    report = deadline_report(request)

    assert report.status == "due_soon"
    assert report.days_remaining == 2


def test_stream_tutor_reply_skips_chunks_without_choices() -> None:
    request = LearnerRequest(
        learner_name="Ari",
        course_title="Data literacy",
        question="How should I check a chart?",
        deadline=date(2026, 9, 11),
        today=date(2026, 9, 9),
    )
    chunks = [
        SimpleNamespace(choices=[]),
        SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="Check axes."))]),
    ]
    with patch.dict("os.environ", {"INFRAI_API_KEY": "test-key"}), patch(
        "src.streaming_course.OpenAI"
    ) as client:
        client.return_value.chat.completions.create.return_value = iter(chunks)
        assert list(stream_tutor_reply(request)) == ["Check axes."]
