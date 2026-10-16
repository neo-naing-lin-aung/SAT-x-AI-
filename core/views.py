from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from google import genai
from google.genai import types
import json 
import os 
from .models import Question, PracticeRecord, QuestionRecord
from .forms import PracticeSetupForm
from .services import calculate_accuracy, finish_practice, calculate_time_used, get_subject_questions_total_and_correct, get_domain_questions_total_and_correct


def index(request):
    """Render the home page."""
    return render(request, "core/index.html")


def about(request):
    """Render the about page."""
    return render(request, "core/about.html")


def study_tools(request):
    """Render the study tools page."""
    return render(request, 'core/tools.html')


def credit(request):
    """Render the credit source page."""
    return render(request, 'core/credit.html')


def ai_assistant(request):
    """Render the AI Assistant Page."""
    return render(request, 'core/ai_assistant.html')

@login_required
def profile(request):
    """Render the profile page."""
    return render(request, 'core/profile.html')


@login_required
def practice(request):
    """Set up practice session."""
    if request.method == "POST":
        # Process form data
        form = PracticeSetupForm(request.POST)

        if form.is_valid():
            # Get cleaned data
            subject = form.cleaned_data["subject"]
            domain = form.cleaned_data["domain"]
            skill = form.cleaned_data["skill"]
            num_questions = form.cleaned_data["num_questions"]
            timer = form.cleaned_data["timer"]

            # Get questions already answered by this user
            answered_questions = QuestionRecord.objects.filter(
                user=request.user
            ).exclude(
                Q(user_answer__isnull=True) | Q(user_answer="")
            ).values_list(
                "question_id",
                flat=True
            )

            # Get available unanswered questions
            available_questions = Question.objects.filter(
                subject=subject,
                domain=domain,
                skill=skill,
            ).exclude(
                id__in=answered_questions
            )

            # Check if there are enough questions
            if available_questions.count() < num_questions:
                messages.error(request, "Sorry, we don't have enough unanswered questions for your request.")
                return redirect("core:practice")

            # Create a practice session
            practice = PracticeRecord.objects.create(
                user=request.user,
                number_of_question=num_questions,
                timer=timer,
            )

            # Select random unanswered questions
            questions = available_questions.order_by("?")[:num_questions]

            # Create QuestionRecords for this practice session
            for index, question in enumerate(questions, start=1):
                QuestionRecord.objects.create(
                    user=request.user,
                    question=question,
                    practice_record=practice,
                    order=index,
                )

            # Go to the first question
            return redirect(
                "core:question",
                practice_id=practice.id,
                question_number=1,
            )

    else:
        # Display blank form
        form = PracticeSetupForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "core/practice.html",
        context,
    )


@login_required
def question(request, practice_id, question_number):
    """Render each question from a practice session."""

    # Get practice record
    practice = get_object_or_404(
        PracticeRecord,
        id=practice_id,
        user=request.user,
    )

    # Get question record
    question_record = get_object_or_404(
        QuestionRecord,
        practice_record=practice,
        user=request.user,
        order=question_number,
    )

    # Get question
    question = question_record.question

    # Calculate remaining time
    elapsed = timezone.now() - practice.started_at

    total_seconds = practice.timer * 60

    remaining_seconds = max(
        0,
        total_seconds - int(elapsed.total_seconds())
    )

    # If time has already expired
    if remaining_seconds <= 0:
        return redirect(
            "core:practice_result",
            practice_id=practice.id,
        )

    if request.method == "POST":

        # Get user's answer
        user_answer = request.POST.get("answer", "").strip()

        # Store user's answer
        question_record.user_answer = user_answer

        # Check answer
        if question.question_type == "mc":
            question_record.is_correct = (
                user_answer == question.answer
            )

        elif question.question_type == "fb":
            question_record.is_correct = (
                user_answer.lower() == question.answer.lower()
            )

        question_record.save()

        # Check time again after processing the answer
        elapsed = timezone.now() - practice.started_at

        remaining_seconds = max(
            0,
            total_seconds - int(elapsed.total_seconds())
        )

        if remaining_seconds <= 0:
            return redirect(
                "core:practice_result",
                practice_id=practice.id,
            )

        # Go to next question
        if question_number < practice.number_of_question:
            return redirect(
                "core:question",
                practice_id=practice.id,
                question_number=question_number + 1,
            )

        # Update question practice date
        question_record.practice_at = timezone.localdate()
        question_record.save()

        # Update practice end time 
        finish_practice(practice)

        # Practice finished
        return redirect(
            "core:practice_result",
            practice_id=practice.id,
        )

    context = {
        "practice": practice,
        "question_record": question_record,
        "question": question,
        "question_number": question_number,
        "total_questions": practice.number_of_question,
        "remaining_seconds": remaining_seconds,
    }

    return render(
        request,
        "core/question.html",
        context,
    )


@login_required
def practice_result(request, practice_id):
    """Show the result of a completed practice session."""

    # Get practice record
    practice = get_object_or_404(
        PracticeRecord,
        id=practice_id,
        user=request.user,
    )

    # Get all question records for this practice
    question_records = QuestionRecord.objects.filter(
        practice_record=practice,
        user=request.user,
    ).select_related("question").order_by("order")

    # Calculate results
    total = question_records.count()

    correct = question_records.filter(
        is_correct=True
    ).count()

    unanswered = question_records.filter(
        user_answer__isnull=True
    ).count()

    # Also count empty-string answers as unanswered
    unanswered += question_records.filter(
        user_answer=""
    ).count()

    incorrect = total - correct - unanswered

    # Calculate accuracy
    accuracy = calculate_accuracy(total, correct)

    # Calculate time used
    time_used_display = calculate_time_used(practice.started_at, practice.end_at)

    # Get subject/domain/difficulty from the first question
    first_question = question_records.first()

    if first_question:
        subject = first_question.question.get_subject_display()
        domain = first_question.question.get_domain_display()
        difficulty = first_question.question.get_skill_display()
    else:
        subject = "-"
        domain = "-"
        difficulty = "-"

    context = {
        "practice": practice,
        "question_records": question_records,

        "correct": correct,
        "incorrect": incorrect,
        "unanswered": unanswered,
        "total": total,
        "accuracy": accuracy,

        "subject": subject,
        "domain": domain,
        "difficulty": difficulty,
        "time_used": time_used_display,
    }

    return render(
        request,
        "core/practice_result.html",
        context,
    )

@login_required
def progress(request):
    """Show the user's progress."""
    # Get all answered questions 
    answered = QuestionRecord.objects.filter(
        user=request.user,
    )

    # Get all correct questions 
    correct = answered.filter(
        is_correct=True,
    ).count()

    # Get all incorrect including unanswered questions 
    incorrect = answered.filter(
        is_correct=False,
    ).count()

    # Calculte accuarcy 
    total = answered.count()
    accuracy = calculate_accuracy(total, correct)

    # Get total practice
    total_practices = PracticeRecord.objects.filter(
        user=request.user,
    ).count()

    # Calculate reading and writing accuracy
    rw_total, rw_correct = get_subject_questions_total_and_correct(answered, 'rw')
    rw_accuracy = calculate_accuracy(rw_total, rw_correct)

    # Calculate Math accuracy
    math_total, math_correct = get_subject_questions_total_and_correct(answered, 'math')
    math_accuracy = calculate_accuracy(math_total, math_correct)

    # Calculate information accuracy
    info_total, info_correct = get_domain_questions_total_and_correct(answered, 'rw', 'information')
    information_accuracy = calculate_accuracy(info_total, info_correct)

    # Calculate craft accuracy
    craft_total, craft_correct = get_domain_questions_total_and_correct(answered, 'rw', 'craft')
    craft_accuracy = calculate_accuracy(craft_total, craft_correct)

    # Calculate expression accuracy
    expression_total, expression_correct = get_domain_questions_total_and_correct(answered, 'rw', 'expression')
    expression_accuracy = calculate_accuracy(expression_total, expression_correct)

    # Calculate sec accuracy
    sec_total, sec_correct = get_domain_questions_total_and_correct(answered, 'rw', 'sec')
    sec_accuracy = calculate_accuracy(sec_total, sec_correct)

    # Calculate algebra accuracy
    algebra_total, algebra_correct = get_domain_questions_total_and_correct(answered, 'math', 'algebra')
    algebra_accuracy = calculate_accuracy(algebra_total, algebra_correct)

    # Calculate advanced_math accuracy
    advanced_math_total, advanced_math_correct = get_domain_questions_total_and_correct(answered, 'math', 'advanced_math')
    advanced_math_accuracy = calculate_accuracy(advanced_math_total, advanced_math_correct)

    # Calculate psda accuracy
    psda_total, psda_correct = get_domain_questions_total_and_correct(answered, 'math', 'psda')
    psda_accuracy = calculate_accuracy(psda_total, psda_correct)

    # Calculate geometry accuracy
    geometry_total, geometry_correct = get_domain_questions_total_and_correct(answered, 'math', 'geometry')
    geometry_accuracy = calculate_accuracy(geometry_total, geometry_correct)

    # Get recent practices & their accuracies 
    recent_practices = PracticeRecord.objects.filter(
        user=request.user,
    ).annotate(
        total=Count('questionrecord'),
        correct=Count(
            'questionrecord',
            filter=Q(questionrecord__is_correct=True),
        ),
    )

    for practice in recent_practices:
        practice.accuracy = calculate_accuracy(total, correct)

    context = {
        "answered": total,
        "correct": correct, 
        "incorrect": incorrect,
        "accuracy": accuracy,
        "total_practices": total_practices,
        "rw_accuracy": rw_accuracy,
        "math_accuracy": math_accuracy,
        "information_accuracy": information_accuracy,
        "craft_accuracy": craft_accuracy,
        "expression_accuracy": expression_accuracy,
        "sec_accuracy": sec_accuracy,
        "algebra_accuracy": algebra_accuracy,
        "advanced_math_accuracy": advanced_math_accuracy,
        "psda_accuracy": psda_accuracy,
        "geometry_accuracy": geometry_accuracy,
        'recent_practices': recent_practices,
    }

    # Render template
    return render(
        request,
        "core/progress.html",
        context,
        )


def review(request, practice_id, question_number):
    """Render each question's review."""

    # Get practice record 
    practice = get_object_or_404(
        PracticeRecord,
        id=practice_id,
        user=request.user,
    )

    # Get question record 
    question_record = get_object_or_404(
        QuestionRecord,
        practice_record=practice,
        user=request.user,
        order=question_number,
    )

    # Get the question number 
    question_number = question_record.order

    # Get the question model
    question_model = question_record.question

    # Get the question 
    question = question_model.question

    # Get the choices
    choice_a = choice_b = choice_c = choice_d = ''
    if question_model.question_type == 'mc':
        choice_a = question_model.choice_a
        choice_b = question_model.choice_b
        choice_c = question_model.choice_c
        choice_d = question_model.choice_d

    # Get the answer
    answer = question_model.answer

    # Get the user answer 
    user_answer = question_record.user_answer

    # Get total questions 
    total_questions = practice.number_of_question 

    context = {
        'practice': practice,
        'question_number': question_number,
        'question': question, 
        'choice_a': choice_a,
        'choice_b': choice_b,
        'choice_c': choice_c,
        'choice_d': choice_d,
        'answer': answer,
        'user_answer': user_answer,
        'total_questions': total_questions,
    }

    return render(
        request,
        'core/review.html',
        context,
        )


@login_required
@require_POST
def ai_chat(request):
    """Define AI chat function for SAT review questions."""
    try: 
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        correct_answer = data.get('correct_answer', '').strip()
        choice_a = data.get('choice_a', '').strip()
        choice_b = data.get('choice_b', '').strip()
        choice_c = data.get('choice_c', '').strip()
        choice_d = data.get('choice_d', '').strip()
        user_answer = data.get('user_answer', '').strip()
        message = data.get('message', '').strip()

        if not message:
            return JsonResponse(
                {'error': 'Plese enter a message'},
                status=400,
            )

        api_key = os.getenv('GEMINI_API_KEY')

        if not api_key:
            return JsonResponse(
                {'error': "Gemini API key is not configured."},
                status=500,
            )

        client = genai.Client(api_key=api_key)


        system_instruction = r"""
    You are a friendly SAT tutor for the SAT × AI learning platform.

    Explain concepts simply and clearly. Help students understand the
    reasoning instead of just giving the answer.

    Give a clear, step-by-step explanation appropriate for an SAT student.

        MATH FORMATTING RULES:
        - Use \\( ... \\) for inline mathematical expressions.
        - Use \\[ ... \\] for display equations.
        - Never wrap mathematical expressions in ordinary parentheses
        as a substitute for math delimiters.
        - Never use single square brackets [ ... ] as math delimiters.
        - Write fractions using standard LaTeX, for example:
        \\(\\frac{7x^2+14x}{x}\\)
        - Keep all LaTeX commands valid.
        """


        prompt = f"""

    SAT question:
    {question or "Not provided"}

    Correct answer:
    {correct_answer or "Not provided"}

    Choice A:
    {choice_a or 'Not Provided'}

    Choice B:
    {choice_b or 'Not Provided'}

    Choice C:
    {choice_c or 'Not Provided'}

    Choice D:
    {choice_d or 'Not Provided'}

    Student's answer:
    {user_answer or "Not provided"}

    Student's request:
    {message} 

"""
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            ),
            contents=prompt,
        )

        reply_text = response.text 
        if not reply_text:
            reply_text = "Sorry, I couldn't generate an explanation."

        return JsonResponse({"reply": reply_text})


    except json.JSONDecodeError:
        return JsonResponse(
            {'error': "Invalid request data."},
            status=400,
        )

    except Exception as e:
        return JsonResponse(
            {'error': "The AI tutor is temporarily unavailable. Please try again."},
            status=503,
        )