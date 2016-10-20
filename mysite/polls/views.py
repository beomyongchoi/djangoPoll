from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/Index.html'
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        (미래에 발행할 설문은 제외하고) 가장 최근에 발행된 설문 5개를 반환합니다
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        # return Question.objects.all()

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        아직 발행하지 않은 설문을 제외합니다
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 설문 폼을 다시 표시합니다.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # POST 데이터를 성공적으로 처리한 후에는 항상 HttpResponseRedirect를
        # 반환합니다. 그래야 사용자가 뒤로가가(Back) 버튼을 클릭했을 때 폼이
        # 두 번 제출되는 현상이 생기지 않습니다.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
