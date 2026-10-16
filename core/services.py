"""Define helper functions for core app."""
from django.utils import timezone


def finish_practice(practice):
    if practice.end_at is None:
        practice.end_at = timezone.now()
        practice.save(update_fields=["end_at"])


def calculate_accuracy(total, correct):
    if total > 0:
        accuracy = round((correct / total) * 100)
    else:
        accuracy = 0

    return accuracy


def calculate_time_used(start, end):
    time_used = end - start
    total_seconds = int(time_used.total_seconds())

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    time_used_display = f"{minutes}m {seconds}s"

    return time_used_display


def get_subject_questions_total_and_correct(answered, subject):
    questions = answered.filter(
        question__subject=subject,
    )
    total = questions.count()

    correct = questions.filter(
        is_correct=True,
    ).count()

    return total, correct


def get_domain_questions_total_and_correct(answered, subject, domain):
    questions = answered.filter(
        question__subject=subject,
        question__domain=domain,
    )
    total = questions.count()

    correct = questions.filter(
        is_correct=True
    ).count()

    return total, correct