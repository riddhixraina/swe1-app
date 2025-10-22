import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice


class QuestionModelTests(TestCase):
    """Test suite for Question model"""

    def test_question_creation(self):
        """Test that a question can be created"""
        question = Question.objects.create(
            question_text="Test question?", pub_date=timezone.now()
        )
        self.assertIsNotNone(question)
        self.assertEqual(question.question_text, "Test question?")

    def test_question_str_representation(self):
        """Test the string representation of a question"""
        question = Question.objects.create(
            question_text="What is your favorite color?", pub_date=timezone.now()
        )
        self.assertEqual(str(question), "What is your favorite color?")

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for future questions"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for old questions"""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for recent questions"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class ChoiceModelTests(TestCase):
    """Test suite for Choice model"""

    def test_choice_creation(self):
        """Test that a choice can be created"""
        question = Question.objects.create(
            question_text="Test question?", pub_date=timezone.now()
        )
        choice = Choice.objects.create(
            question=question, choice_text="Test choice", votes=0
        )
        self.assertIsNotNone(choice)
        self.assertEqual(choice.votes, 0)
        self.assertEqual(choice.choice_text, "Test choice")

    def test_choice_str_representation(self):
        """Test the string representation of a choice"""
        question = Question.objects.create(
            question_text="Test question?", pub_date=timezone.now()
        )
        choice = Choice.objects.create(question=question, choice_text="Blue", votes=0)
        self.assertEqual(str(choice), "Blue")


class PollsIndexViewTests(TestCase):
    """Test suite for polls index view"""

    def test_index_view_status_code(self):
        """Test that index view returns 200 status code"""
        response = self.client.get(reverse("polls:index"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        """Test that index view uses the correct template"""
        response = self.client.get(reverse("polls:index"), follow=True)
        self.assertTemplateUsed(response, "polls/index.html")

    def test_index_view_with_no_questions(self):
        """Test index view when no questions exist"""
        response = self.client.get(reverse("polls:index"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_index_view_with_multiple_questions(self):
        """Test index view displays multiple questions"""
        Question.objects.create(question_text="Question 1?", pub_date=timezone.now())
        Question.objects.create(
            question_text="Question 2?",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )
        response = self.client.get(reverse("polls:index"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["latest_question_list"]), 2)

    def test_index_view_pagination(self):
        """Test that pagination works correctly"""
        for i in range(6):
            Question.objects.create(
                question_text=f"Question {i}?",
                pub_date=timezone.now() - datetime.timedelta(days=i),
            )
        response = self.client.get(reverse("polls:index"), follow=True)
        self.assertEqual(len(response.context["latest_question_list"]), 5)
        response = self.client.get(reverse("polls:index") + "?page=2", follow=True)
        self.assertEqual(len(response.context["latest_question_list"]), 1)


class PollsDetailViewTests(TestCase):
    """Test suite for polls detail view"""

    def test_detail_view_with_valid_question(self):
        question = Question.objects.create(
            question_text="Test question?", pub_date=timezone.now()
        )
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

    def test_detail_view_with_invalid_question(self):
        url = reverse("polls:detail", args=(999,))
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_uses_correct_template(self):
        question = Question.objects.create(
            question_text="Test question?", pub_date=timezone.now()
        )
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed(response, "polls/detail.html")


class PollsResultsViewTests(TestCase):
    """Test suite for polls results view"""

    def test_results_view_with_valid_question(self):
        question = Question.objects.create(
            question_text="Test question?", pub_date=timezone.now()
        )
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

    def test_results_view_uses_correct_template(self):
        question = Question.objects.create(
            question_text="Test question?", pub_date=timezone.now()
        )
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed(response, "polls/results.html")

    def test_results_view_with_previous_question(self):
        question1 = Question.objects.create(
            question_text="Question 1?",
            pub_date=timezone.now() - datetime.timedelta(days=2),
        )
        question2 = Question.objects.create(
            question_text="Question 2?",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )
        url = reverse("polls:results", args=(question2.id,))
        response = self.client.get(url, follow=True)
        self.assertEqual(response.context["previous_question"], question1)

    def test_results_view_with_next_question(self):
        question1 = Question.objects.create(
            question_text="Question 1?",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )
        question2 = Question.objects.create(
            question_text="Question 2?", pub_date=timezone.now()
        )
        url = reverse("polls:results", args=(question1.id,))
        response = self.client.get(url, follow=True)
        self.assertEqual(response.context["next_question"], question2)

    def test_results_view_without_previous_question(self):
        question = Question.objects.create(
            question_text="Only question?", pub_date=timezone.now()
        )
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url, follow=True)
        self.assertIsNone(response.context["previous_question"])

    def test_results_view_without_next_question(self):
        question = Question.objects.create(
            question_text="Latest question?", pub_date=timezone.now()
        )
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url, follow=True)
        self.assertIsNone(response.context["next_question"])


class PollsVoteViewTests(TestCase):
    """Test suite for polls vote view"""

    def test_vote_redirects_to_results(self):
        question = Question.objects.create(
            question_text="Test question?", pub_date=timezone.now()
        )
        choice = Choice.objects.create(
            question=question, choice_text="Test choice", votes=0
        )
        url = reverse("polls:vote", args=(question.id,))
        response = self.client.post(url, {"choice": choice.id}, follow=True)
        self.assertEqual(response.status_code, 200)
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 0)

    def test_vote_increments_choice_votes(self):
        question = Question.objects.create(
            question_text="Test question?", pub_date=timezone.now()
        )
        choice = Choice.objects.create(
            question=question, choice_text="Test choice", votes=0
        )
        url = reverse("polls:vote", args=(question.id,))
        self.client.post(url, {"choice": choice.id}, follow=True)
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 0)

    def test_vote_without_choice_shows_error(self):
        question = Question.objects.create(
            question_text="Test question?", pub_date=timezone.now()
        )
        url = reverse("polls:vote", args=(question.id,))
        response = self.client.post(url, {}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("error_message", response.context)
        self.assertEqual(
            response.context["error_message"], "You didn't select a choice."
        )

    def test_vote_with_invalid_choice(self):
        question = Question.objects.create(
            question_text="Test question?", pub_date=timezone.now()
        )
        url = reverse("polls:vote", args=(question.id,))
        response = self.client.post(url, {"choice": 999}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("error_message", response.context)
        self.assertEqual(
            response.context["error_message"], "You didn't select a choice."
        )

    def test_vote_with_invalid_question(self):
        url = reverse("polls:vote", args=(999,))
        response = self.client.post(url, {"choice": 1}, follow=True)
        self.assertEqual(response.status_code, 404)
