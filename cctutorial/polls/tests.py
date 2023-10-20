import pytest
from datetime import date, timedelta

from faker import Faker
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from polls.models import Question, Choice
from polls import views


TODAY = date(2023, 10, 19)
fake = Faker()


class PollsTests(TestCase):
    """
    Simple tests for the polls app
    """
    def setUp(self):
        new_question = Question.objects.create(
            question_text='Who are you?',
            pub_date=timezone.now())

        for _ in range(3):
            Choice.objects.create(
                question=new_question,
                choice_text=fake.name())

    def test_choices(self):
        """Test the choices view"""

        response = self.client.get(reverse('polls:choices'))
        self.assertEqual(response.status_code, 200)

        # Add a test for a non-existant ID and test for the expected result

    def test_most_popular_choice(self):
        response = self.client.get(reverse('polls:most-popular-choice'))
        self.assertEqual(response.status_code, 200)


class SeedDataBase:
    @pytest.fixture(autouse=True)
    def _seed_data(self):
        for i in range(1, 4):
            new_question = Question.objects.create(
                question_text=fake.sentence(nb_words=3),
                pub_date=TODAY - timedelta(days=10 * i))

            for j in range(3):
                Choice.objects.create(
                    question=new_question,
                    choice_text=fake.name())



@pytest.mark.django_db
class TestIndex(SeedDataBase):
    # Throughout the tests below, I'm comparing sets of objects just as a quick
    # and dirty test. A more rigorous test would also comfirm proper ordering.

    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        self.render_spy = mocker.spy(views, 'render')
        self.url_name = 'polls:index'

    def test_with_data(self, client):
        latest_questions = [
            Question.objects.create(
                question_text=fake.sentence(nb_words=3),
                pub_date=timezone.now())
            for k in range(5)]
        assert Question.objects.count() == 8

        expected_questions = set(latest_questions)

        response = client.get(reverse(self.url_name))
        assert response.status_code == 200
        actual_questions = set(self.render_spy.call_args.args[2]['questions'])
        assert expected_questions == actual_questions


@pytest.mark.django_db
class TestMostPopularChoice(SeedDataBase):
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        self.render_spy = mocker.spy(views, 'render')
        self.url_name = 'polls:most-popular-choice'

    def test_degenerate_case(self, client):
        # No votes have been cast so all Questions and Choices should be returned.
        assert Question.objects.count() == 3
        assert Choice.objects.count() == 9

        expected_questions = set(Question.objects.all())

        response = client.get(reverse(self.url_name))
        assert response.status_code == 200
        actual_questions = set(self.render_spy.call_args.args[2]['questions'])
        assert expected_questions == actual_questions

    def test_most_voted_choice(self, client):
        assert Question.objects.count() == 3
        assert Choice.objects.count() == 9

        random_choice = Choice.objects.order_by('?').first()
        random_choice.votes = 10
        random_choice.save()

        expected_question = random_choice.question

        response = client.get(reverse(self.url_name))
        assert response.status_code == 200
        actual_questions = set(self.render_spy.call_args.args[2]['questions'])
        actual_question = actual_questions.pop()
        assert expected_question == actual_question

        assert (
            self.render_spy.call_args.args[2]['questions'][actual_question] ==
            [random_choice])

    def test_tied_vote_returns_multiple_choices(self, client):
        assert Question.objects.count() == 3
        assert Choice.objects.count() == 9

        random_choice = Choice.objects.order_by('?').first()
        random_choice.votes = 10
        random_choice.save()

        another_random_choice = Choice.objects.exclude(pk=random_choice.pk).order_by('?').first()
        another_random_choice.votes = 10
        another_random_choice.save()

        expected_questions = {random_choice.question, another_random_choice.question}

        response = client.get(reverse(self.url_name))
        assert response.status_code == 200
        actual_questions = set(self.render_spy.call_args.args[2]['questions'])
        assert expected_questions == actual_questions

        for choice in (random_choice,
                       another_random_choice):
            assert (
                choice in
                self.render_spy.call_args.args[2]['questions'][choice.question]
                )


@pytest.mark.django_db
class TestChoices(SeedDataBase):
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        self.render_spy = mocker.spy(views, 'render')
        self.url_name = 'polls:choices'

    def test_empty(self, client):
        Question.objects.all().delete()
        response = client.get(reverse(self.url_name))
        assert response.status_code == 200
        assert not self.render_spy.call_args.args[2]['questions']
        assert not self.render_spy.call_args.args[2]['choices']

    def test_non_existent_raises_404(self, client):
        max_id = Choice.objects.all().order_by('-pk').values_list('pk', flat=True)[0]
        response = client.get(reverse(self.url_name, kwargs=dict(pk=max_id + 1)))
        assert response.status_code == 404

    def test_get_single_choice(self, client):
        random_choice = Choice.objects.all().order_by('?').first()

        response = client.get(reverse(self.url_name, kwargs=dict(pk=random_choice.pk)))
        assert response.status_code == 200

        assert self.render_spy.call_args.args[2]['questions'] == {random_choice.question}
        assert self.render_spy.call_args.args[2]['choices'] == [random_choice]

    def test_get_all_choices(self, client):
        response = client.get(reverse(self.url_name))
        assert response.status_code == 200

        assert (
            set(self.render_spy.call_args.args[2]['choices']) ==
            set(Choice.objects.all())
        )
        assert (
            set(self.render_spy.call_args.args[2]['questions']) ==
            set(Question.objects.all())
        )
        # Make sure no duplicate Questions have been sent
        assert (
            len(self.render_spy.call_args.args[2]['questions']) ==
            Question.objects.count()
        )


@pytest.mark.django_db
class TestQuestion(SeedDataBase):
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        self.render_spy = mocker.spy(views, 'render')
        self.url_name = 'polls:question'

    def test_empty(self, client):
        Question.objects.all().delete()
        response = client.get(reverse(self.url_name))
        assert response.status_code == 200
        assert (
            set(self.render_spy.call_args.args[2]['questions']) ==
            set()
        )

    def test_no_data_for_given_pub_date(self, client):
        far_past = TODAY - timedelta(days=365)
        response = client.get(reverse(self.url_name, kwargs=dict(pub_date=far_past.isoformat())))
        assert response.status_code == 200
        assert (
            set(self.render_spy.call_args.args[2]['questions']) ==
            set()
        )

    def test_no_pub_date(self, client, mocker):
        mock_get_pub_date = mocker.patch('polls.views._get_pub_date')
        mock_get_pub_date.return_value = TODAY

        new_question = Question.objects.create(
            question_text=fake.sentence(nb_words=3),
            pub_date=TODAY + timedelta(days=1))

        expected_questions = set(Question.objects.exclude(pk=new_question.pk))

        response = client.get(reverse(self.url_name))
        assert response.status_code == 200
        assert (
            set(self.render_spy.call_args.args[2]['questions']) ==
            expected_questions
        )

    def test_with_data_for_pub_date(self, client):
        response = client.get(reverse(self.url_name, kwargs=dict(pub_date=TODAY.isoformat())))
        assert response.status_code == 200
        assert (
            set(self.render_spy.call_args.args[2]['questions']) ==
            set(Question.objects.all())
        )
