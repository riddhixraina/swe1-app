from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    paginate_by = 5  # Add this line to enable pagination

    def get_queryset(self):
        # Return all questions, ordered by publication date
        return Question.objects.order_by("-pub_date")


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()

        # Find the previous question
        context["previous_question"] = (
            Question.objects.filter(pub_date__lt=question.pub_date)
            .order_by("-pub_date")
            .first()
        )

        # Find the next question
        context["next_question"] = (
            Question.objects.filter(pub_date__gt=question.pub_date)
            .order_by("pub_date")
            .first()
        )

        return context


def vote(request, question_id):
    """Handle voting for a question."""
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            # Show the same question page again with an error message
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "You didn't select a valid choice.",
                },
            )
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    else:
        # If someone tries to GET this URL directly, show the question with an error
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
