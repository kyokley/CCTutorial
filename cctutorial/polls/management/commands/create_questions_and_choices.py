from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create 4 Questions and 3-6 Choices for each of those Question objects'

    def handle(self, *args, **kwargs):
        pass
        # use the Django API models to create four new questions in the
        # database as well as 3-6 Choices/Answers for those questions.
        # See "Playing with the API" in the Django Tutorial:
        # https://docs.djangoproject.com/en/3.2/intro/tutorial02/
        #
        # When creating your choices, assign a random number of votes to
        # that choice with a value between 0 and 10.
