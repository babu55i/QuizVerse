from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.quiz_list,
        name="quiz_list"
    ),

    path(
        "create/",
        views.create_quiz,
        name="create_quiz"
    ),

    path(
        "<int:quiz_id>/",
        views.quiz_detail,
        name="quiz_detail"
    ),

    path(
        "add-question/<int:quiz_id>/",
        views.add_question,
        name="add_question"
    ),

    path(
        "add-answer/<int:question_id>/",
        views.add_answer,
        name="add_answer"
),

    path(
        "take-quiz/<int:quiz_id>/",
        views.take_quiz,
        name="take_quiz"
),

    path(
        "my-quizzes/",
        views.my_quizzes,
        name="my_quizzes"
),

    path(
        "edit-quiz/<int:quiz_id>/",
        views.edit_quiz,
        name="edit_quiz"
),

    path(
        "delete-quiz/<int:quiz_id>/",
        views.delete_quiz,
        name="delete_quiz"
),

    path(
        "profile/",
        views.profile,
        name="profile"
),

    path(
        "edit-question/<int:question_id>/",
        views.edit_question,
        name="edit_question"
),

    path(
        "edit-answer/<int:answer_id>/",
        views.edit_answer,
        name="edit_answer"
),

    path(
        "delete-answer/<int:answer_id>/",
        views.delete_answer,
        name="delete_answer"
),

    path(
        "delete-question/<int:question_id>/",
        views.delete_question,
        name="delete_question"
),

    path(
        "quiz/<int:quiz_id>/like/",
        views.toggle_like,
        name="toggle_like"
),

    path(
        "comment/<int:comment_id>/delete/",
        views.delete_comment,
        name="delete_comment"
),

    path(
        "quiz/<int:quiz_id>/favorite/",
        views.toggle_favorite,
        name="toggle_favorite"
),

    path(
        "favorites/",
        views.favorite_quizzes,
        name="favorite_quizzes"
),


    path(
        "quiz/<int:quiz_id>/report/",
        views.report_quiz,
        name="report_quiz"
),

]