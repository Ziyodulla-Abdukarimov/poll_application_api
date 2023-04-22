from django.contrib import admin
from model.models import Question, Choice, OneChoice, MultiChoice


# Register your models here.

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(OneChoice)
admin.site.register(MultiChoice)
