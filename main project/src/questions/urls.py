from django.urls import path
from . import views

urlpatterns = [
    #questions urls
    path('', views.list_questions, name="questions"),
    path('create/', views.create_question, name="question-create"),
    path('<int:pk>/', views.question_details, name="question-details"),
    path('update/<int:question_id>', views.update_question, name="update-question"),
    path('delete/<int:question_id>', views.delete_question, name="delete-question"),
    path('my-questions/', views.my_questions, name="my_questions"),

    # votes urls
    path('upvote/<int:answer_id>/<int:question_id>/', views.upvote, name="upvote"),
    path('downvote/<int:answer_id>/<int:question_id>/', views.downvote, name="downvote"),

    # answers urls
    path('add-answer/<int:question_id>', views.add_answer, name="add_answer"),
    path('update-answer/<int:answer_id>/<int:question_id>/', views.update_answer, name="update_answer"),
    path('delete-answer/<int:answer_id>/<int:question_id>/', views.delete_answer, name="delete_answer"),

    # search questions
    path('search/', views.search, name="questions-search"),
]
