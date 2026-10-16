from django.contrib import admin

from .models import Question, PracticeRecord, QuestionRecord

admin.site.register(Question)
admin.site.register(PracticeRecord)
admin.site.register(QuestionRecord)