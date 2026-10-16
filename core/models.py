from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    """Define Question model for SAT questions."""

    SUBJECT_CHOICES = [
        ("math", "Math"), 
        ("rw", "Reading and Writing"),
    ]
    subject = models.CharField(
        max_length=5,
        choices=SUBJECT_CHOICES
    )

    DOMAIN_CHOICES = [
        # Math 
        ("algebra", "Algebra"),
        ("advanced_math", "Advanced Math"),
        ("psda", "Problem-Solving and Data Analysis"),
        ("geometry", "Geometry and Trigonometry"),

        # R&W 
        ("information", "Information and Ideas"),
        ("craft", "Craft and Structure"),
        ("expression", "Expression of Ideas"),
        ("sec", "Standard English Conventions"),
    ]
    domain = models.CharField(
        max_length=15,
        choices=DOMAIN_CHOICES
    )

    SKILL_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("difficult", "Difficult"),
    ]
    skill = models.CharField(
        max_length=10,
        choices=SKILL_CHOICES
    )

    QUESTION_TYPE_CHOICES = [
        ("mc", "Multiple Choice"),
        ("fb", "Fill in the Blank"),
    ]
    question_type = models.CharField(
        max_length=3,
        choices=QUESTION_TYPE_CHOICES
    )

    question = models.TextField(blank=True)
    choice_a = models.TextField(blank=True)
    choice_b = models.TextField(blank=True)
    choice_c = models.TextField(blank=True)
    choice_d = models.TextField(blank=True)
    answer = models.CharField(max_length=100)
    explanation = models.TextField()

    def __str__(self):
        """Return a string representation of the Question model."""
        return self.question



class PracticeRecord(models.Model):
    """Define Practice Session model for a User."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_question = models.IntegerField()
    timer = models.IntegerField()    
    started_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """Return a string representation of the Practice Record model."""
        representation = f"{self.user.username} - Practice {self.id}"
        return representation
        

class QuestionRecord(models.Model):
    """Define Question Record model for a User."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    practice_record = models.ForeignKey(PracticeRecord, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=100, blank=True, null=True)
    is_correct = models.BooleanField(blank=True, null=True)
    practice_at = models.DateField(blank=True, null=True)
    order = models.PositiveIntegerField()

    def __str__(self):
        """Return a string reprensentation of the Question Record model."""
        representation = f"{self.user.username} - Question {self.question.id}"
        return representation


