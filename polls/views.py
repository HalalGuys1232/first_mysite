from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse, Http404, HttpResponseRedirect # HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.template import loader
from django.urls import reverse, reverse_lazy # reverse
from django.views import generic
from django.views.generic import UpdateView, DeleteView

class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'polls/question_confirm_delete.html'
    success_url = reverse_lazy('polls:index')

class ChoiceUpdateView(UpdateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_update_form.html'  # 새로운 템플릿 또는 기존 템플릿 지정

    def get_success_url(self):
        # 선택지가 업데이트된 후, 선택지가 속한 질문의 상세 페이지로 리다이렉션
        choice = self.object
        return reverse('polls:detail', kwargs={'question_id': choice.question.pk})

class QuestionUpdateView(generic.edit.UpdateView):
    model = Question
    fields = ['question_text']
    template_name = 'polls/question_update_form.html'  # 재사용하거나 적절한 템플릿 지정
    success_url = reverse_lazy('polls:index')  # 예시 URL, 실제 프로젝트에 맞게 수정 필요

class ChoiceCreateView(generic.edit.CreateView):
    model = Choice
    fields=['choice_text']
    template_name = 'polls/choice_form.html'
    def form_valid(self, form):
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('polls:detail', kwargs={'question_id': self.kwargs['pk']})



class QuestionCreateView(generic.edit.CreateView):
    model = Question
    fields = ['question_text']
    template_name = 'polls/question_form.html'
    success_url = reverse_lazy('polls:index')


# IndexView
class IndexView(generic.ListView):
    # [app_name]/[model_name]_list.html
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"    
    def get_queryset(self):
        """Return the last five published questions."""
        qs = Question.objects.all()
        return sorted(qs, key=lambda q : sum([ c.votes for c in q.choice_set.all()]), reverse=True)
    # 전체 퀘스쳔 가져오기
    # 각 퀘스쳔 별로 votes를 어떻게 구하지
    # 총합을 구하기    
    # 정렬은 어떻게 할까
class DetailView(generic.DetailView):
    model = Question
    # template_name = "polls/detail.html"
    def get_object(self):
        question_id = self.kwargs['question_id']
        question = get_object_or_404(Question, pk=question_id)
        return question        

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"  

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"likelion": latest_question_list}
    return render(request, "lion/index.html", context)




# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("polls/index.html")
#     context = {
#         "likelion": latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

# index1 을 만들고, index1.html을 만들어서 하나 동작시켜 보기

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "polls/detail.html", {"question": question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # choice_count = len(question.choice_set.all())
    # content_1 = question.choice_set.all()[0]
    question_list = Question.objects.all()
    context ={
        "question" : question, 
        "question_list" : question_list
    }
    # context ={
    #     "question" : question, 
    #     "ch_num" : choice_count,
    #     "content_1":content_1
    # }
    return render(request, "polls/detail.html", context)




def results(request, question_id):
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

from django.db.models import F
def vote(request, question_id):
    # choice 데이터에서 해당하는 값에 votes를 1 더하기

    # q = Question.objects.get(pk=question_id)
    # c = ....
    # c.votes +=1
    # c.save()


    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# question_id 말고 다른 이름으로 받아도 될까?
# 숫자가 아닌게 들어오면 어떻게 되지?
# 2개 다른 경로로 들어오고 question_id가 표시되는 view의 함수를 만들어 봅시다.
# 11:30까지