"""Run the terminal version of the streaming course workflow."""

from datetime import date

from src.streaming_course import LearnerRequest, deadline_report, stream_tutor_reply


def main() -> None:
    request = LearnerRequest(
        learner_name="Mina",
        course_title="Intro to retrieval augmented generation",
        question="Why do we retrieve passages before asking the model?",
        deadline=date(2026, 9, 15),
        today=date(2026, 9, 9),
    )
    report = deadline_report(request)
    print(f"{report.learner_name}: {report.status} ({report.days_remaining} days left)")
    print("Tutor:", end=" ", flush=True)
    for piece in stream_tutor_reply(request):
        print(piece, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
