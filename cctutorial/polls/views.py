import datetime
from dateutil import parser
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from polls.models import Choice, Question


def index(request):
    latest_question_qs = Question.objects.only('pk', 'pub_date', 'question_text').order_by('-pub_date')[:5]
    rendered = render(request, 'polls/index.html', {'questions': latest_question_qs})
    return rendered


def most_popular_choice(request):
    """
    After you have created a series of questions and choices,
    return the choice with the most votes of all choices. If there
    are multiples with the same number of votes, return al. For
    the choice, display the choice_text, number of votes and
    related Question id in the response below.
    """
    return HttpResponse("")


def choices(request, pk=None):
    """
    If a primary key is passed in, return only that choice object.
    If no primary key is passed in, return all choices ordered by highest number of votes first.

    Show the related question in both instances
    """
    questions = {}

    if pk:
        choice = get_object_or_404(Choice, pk=pk)
        questions = {choice.question: [choice]}
    else:
        choices = Choice.objects.all().order_by('pk').select_related('question')
        for choice in choices:
            questions.setdefault(choice.question, []).append(choice)


    rendered = render(request, 'polls/choices.html', {'questions': questions})
    return rendered


def question(request, pub_date=None):
    """
    If a primary key is passed in, return only that choice object.
    If no primary key is passed in, return all choices ordered by highest number of votes first.

    Show the related question in both instances
    """
    if pub_date is None:
        pub_date = datetime.date.today()
    else:
        pub_date = parser.parse(pub_date).date()

    # I'm a little confused about the goal for this method. I'm assuming we're
    # actually interested in the questions published either before or after some
    # date. I'm going to work under the assumption we want all questions created
    # before some date.
    questions = Question.objects.filter(pub_date__lte=pub_date)

    rendered = render(request,
                      'polls/questions.html',
                      {'questions': questions, 'pub_date': pub_date.isoformat()})
    return rendered
