# polls 폴더에 urls.py가 업어서 새로 생성

from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('question/new/', views.QuestionCreateView.as_view(), name='question_new'),
    path('question/<int:pk>/choice/new/', views.ChoiceCreateView.as_view(), name='choice_new'),
    path('question/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('choice/<int:pk>/update/', views.ChoiceUpdateView.as_view(), name='choice_update'),
    path('question/<int:pk>/delete/',views.QuestionDeleteView.as_view(), name='question_delete'),
]