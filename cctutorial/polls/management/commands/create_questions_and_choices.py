import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from polls.models import Question, Choice
from faker import Faker

QUESTION_COUNT = 4


fake = Faker()


class Command(BaseCommand):
    help = 'Create 4 Questions and 3-6 Choices for each of those Question objects'

    def handle(self, *args, **kwargs):
        choice_count = 0

        for i in range(QUESTION_COUNT):
            new_question = Question.objects.create(
                question_text=f'{" ".join(fake.words(nb=5, unique=True))}?',
                pub_date=timezone.now())

            for j in range(random.randint(3, 6)):
                Choice.objects.create(
                    question=new_question,
                    choice_text=fake.name(),
                    votes=random.randint(0, 10),
                )
                choice_count += 1

        self.stdout.write(
            f'Inserted {QUESTION_COUNT} Questions'
        )
        self.stdout.write(
            f'Inserted {choice_count} Choices'
        )
        self.stdout.write(
            self.style.SUCCESS('Done')
        )

        # use the Django API models to create four new questions in the
        # database as well as 3-6 Choices/Answers for those questions.
        # See "Playing with the API" in the Django Tutorial:
        # https://docs.djangoproject.com/en/3.2/intro/tutorial02/
        #
        # When creating your choices, assign a random number of votes to
        # that choice with a value between 0 and 10.
