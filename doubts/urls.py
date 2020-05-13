from django.urls import path
from . import views
from .views import (
    UserIndexView,
     IndexView,
     QuestionDetailsView,
     QuestionCreateView,
     QuestionEditView,
     AnswerCreateView,
     AnswerEditView,
     AnswerDeleteView,
     QuestionUpvoteView,
     AnswerUpvoteView,
)
app_name = 'polls'
urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('<int:pk>/', QuestionDetailsView.as_view(), name = 'details'),
    path('user/<int:pk>/', UserIndexView.as_view(), name = 'user-index'),
    path('create/', QuestionCreateView.as_view(), name='create-question'),
    path('<int:pk>/edit/', QuestionEditView.as_view(), name='edit-question'),  #No delete functionality by choice
    path('<int:qid>/answer/', AnswerCreateView.as_view(), name='create-answer'),
    path('<int:qid>/edit-answer/<int:pk>', AnswerEditView.as_view(), name='edit-answer'),
    path('<int:qid>/delete-answer/<int:pk>', AnswerDeleteView.as_view(), name='delete-answer'),
    path('vote-ques/<int:pk>/<int:ud>', QuestionUpvoteView.as_view(), name = 'vote-question'),
    path('vote-ans/<int:pk>/<int:ud>', AnswerUpvoteView.as_view(), name = 'vote-answer'),

]
