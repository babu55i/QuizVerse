from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .forms import (
    QuizForm,
    QuestionForm,
    AnswerForm,
    CommentForm
)
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from .models import (
    Quiz,
    Question,
    Answer,
    QuizResult,
    CATEGORY_CHOICES,
    QuizLike,
    Comment,
    Favorite,
    QuizReport
)
@login_required
def create_quiz(request):

    if request.method == "POST":

        form = QuizForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            quiz = form.save(commit=False)

            quiz.author = request.user

            quiz.save()

            return redirect("index")

    else:

        form = QuizForm()

    return render(
        request,
        "quizzes/create_quiz.html",
        {
            "form": form
        }
    )


def quiz_list(request):

    quizzes = Quiz.objects.exclude(
        category="none"
    ).annotate(
        likes_total=Count("likes")
    ).order_by(
        "-likes_total",
        "-created_at"
    )

    search_query = request.GET.get(
        "q"
    )

    if search_query:
        quizzes = quizzes.filter(
            title__icontains=search_query
        )

    selected_category = request.GET.get(
        "category"
    )

    if selected_category:
        quizzes = quizzes.filter(
            category=selected_category
        )

    week_start = timezone.now() - timedelta(days=7)

    top_week = (
        QuizResult.objects.filter(
            is_perfect=True,
            created_at__gte=week_start
        )
        .values(
            "user__username"
        )
        .annotate(
            perfect_count=Count("id")
        )
        .order_by(
            "-perfect_count"
        )[:10]
    )

    month_start = timezone.now() - timedelta(days=30)

    top_month = (
        QuizResult.objects.filter(
            is_perfect=True,
            created_at__gte=month_start
        )
        .values(
            "user__username"
        )
        .annotate(
            perfect_count=Count("id")
        )
        .order_by(
            "-perfect_count"
        )[:10]
    )

    popular_quizzes = Quiz.objects.annotate(
        likes_total=Count("likes")
    ).order_by(
        "-likes_total"
    )[:5]

    paginator = Paginator(
        quizzes,
        12
    )

    page_number = request.GET.get(
        "page"
    )

    quizzes = paginator.get_page(
        page_number
    )

    return render(
        request,
        "quizzes/list.html",
        {
            "quizzes": quizzes,
            "top_week": top_week,
            "top_month": top_month,
            "search_query": search_query,
            "selected_category": selected_category,
            "CATEGORY_CHOICES": CATEGORY_CHOICES,
            "popular_quizzes": popular_quizzes
        }
    )


def quiz_detail(request, quiz_id):

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id
    )

    comment_form = CommentForm()

    if request.method == "POST":

        if request.user.is_authenticated:

            comment_form = CommentForm(
                request.POST
            )

            if comment_form.is_valid():
                comment = comment_form.save(
                    commit=False
                )

                comment.author = request.user

                comment.quiz = quiz

                comment.save()

                return redirect(
                    "quiz_detail",
                    quiz.id
                )

    likes_count = quiz.likes.count()

    user_liked = False

    if request.user.is_authenticated:
        user_liked = QuizLike.objects.filter(
            user=request.user,
            quiz=quiz
        ).exists()

    user_favorited = False

    if request.user.is_authenticated:
        user_favorited = Favorite.objects.filter(
            user=request.user,
            quiz=quiz
        ).exists()

    return render(
        request,
        "quizzes/detail.html",
        {
            "quiz": quiz,
            "likes_count": likes_count,
            "user_liked": user_liked,
            "comment_form": comment_form,
            "user_favorited": user_favorited,
        }
    )


@login_required
def add_question(request, quiz_id):

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id
    )

    if request.method == "POST":

        form = QuestionForm(
            request.POST
        )

        if form.is_valid():

            question = form.save(
                commit=False
            )

            question.quiz = quiz

            question.save()

            return redirect(
                "quiz_detail",
                quiz.id
            )

    else:

        form = QuestionForm()

    return render(
        request,
        "quizzes/add_question.html",
        {
            "quiz": quiz,
            "form": form
        }
    )

@login_required
def add_answer(request, question_id):

    question = get_object_or_404(
        Question,
        id=question_id
    )

    if question.answers.count() >= 4:
        return redirect(
            "quiz_detail",
            question.quiz.id
        )

    if request.method == "POST":

        form = AnswerForm(
            request.POST
        )

        if form.is_valid():

            answer = form.save(
                commit=False
            )

            answer.question = question

            answer.save()

            return redirect(
                "quiz_detail",
                question.quiz.id
            )

    else:

        form = AnswerForm()

    return render(
        request,
        "quizzes/add_answer.html",
        {
            "question": question,
            "form": form
        }
    )

def take_quiz(request, quiz_id):

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id
    )

    if request.method == "POST":

        score = 0

        total_questions = quiz.questions.count()

        for question in quiz.questions.all():

            selected_answer = request.POST.get(
                f"question_{question.id}"
            )

            if selected_answer:

                answer = Answer.objects.get(
                    id=selected_answer
                )

                if answer.is_correct:

                    score += 1

        percentage = 0

        if total_questions > 0:
            percentage = int(
                score / total_questions * 100
            )

        if percentage >= 80:

            message = "Отлично!"

        elif percentage >= 50:

            message = "Хороший результат!"

        else:

            message = "Попробуйте еще раз!"

        if request.user.is_authenticated:
            QuizResult.objects.create(

                user=request.user,

                quiz=quiz,

                score=score,

                total_questions=total_questions,

                is_perfect=(
                        score == total_questions
                )

            )

        return render(
            request,
            "quizzes/result.html",
            {
                "quiz": quiz,
                "score": score,
                "total_questions": total_questions,
                "percentage": percentage,
                "message": message
            }
        )

    return render(
        request,
        "quizzes/take_quiz.html",
        {
            "quiz": quiz
        }
    )

@login_required
def my_quizzes(request):

    quizzes = Quiz.objects.filter(
        author=request.user
    )

    return render(
        request,
        "quizzes/my_quizzes.html",
        {
            "quizzes": quizzes
        }
    )

@login_required
def edit_quiz(request, quiz_id):

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        author=request.user
    )

    if request.method == "POST":

        form = QuizForm(
            request.POST,
            request.FILES,
            instance=quiz
        )

        if form.is_valid():

            form.save()

            return redirect(
                "quiz_detail",
                quiz.id
            )

    else:

        form = QuizForm(
            instance=quiz
        )

    return render(
        request,
        "quizzes/edit_quiz.html",
        {
            "form": form,
            "quiz": quiz
        }
    )

@login_required
def delete_quiz(request, quiz_id):

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        author=request.user
    )

    if request.method == "POST":

        quiz.delete()

        return redirect(
            "my_quizzes"
        )

    return render(
        request,
        "quizzes/delete_quiz.html",
        {
            "quiz": quiz
        }
    )

@login_required
def profile(request):

    quizzes_count = Quiz.objects.filter(
        author=request.user
    ).count()

    completed_quizzes = QuizResult.objects.filter(
        user=request.user
    ).count()

    perfect_quizzes = QuizResult.objects.filter(
        user=request.user,
        is_perfect=True
    ).count()

    likes_received = 0

    for quiz in Quiz.objects.filter(
        author=request.user
    ):
        likes_received += quiz.likes.count()

    favorites_count = Favorite.objects.filter(
        user=request.user
    ).count()

    return render(
        request,
        "quizzes/profile.html",
        {
            "quizzes_count": quizzes_count,
            "completed_quizzes": completed_quizzes,
            "perfect_quizzes": perfect_quizzes,
            "likes_received": likes_received,
            "favorites_count": favorites_count,
        }
    )

@login_required
def edit_question(request, question_id):

    question = get_object_or_404(
        Question,
        id=question_id
    )

    if question.quiz.author != request.user:

        return redirect(
            "quiz_detail",
            question.quiz.id
        )

    if request.method == "POST":

        form = QuestionForm(
            request.POST,
            instance=question
        )

        if form.is_valid():

            form.save()

            return redirect(
                "quiz_detail",
                question.quiz.id
            )

    else:

        form = QuestionForm(
            instance=question
        )

    return render(
        request,
        "quizzes/edit_question.html",
        {
            "form": form,
            "question": question
        }
    )


@login_required
def edit_answer(request, answer_id):

    answer = get_object_or_404(
        Answer,
        id=answer_id
    )

    if answer.question.quiz.author != request.user:

        return redirect(
            "quiz_detail",
            answer.question.quiz.id
        )

    if request.method == "POST":

        form = AnswerForm(
            request.POST,
            instance=answer
        )

        if form.is_valid():

            form.save()

            return redirect(
                "quiz_detail",
                answer.question.quiz.id
            )

    else:

        form = AnswerForm(
            instance=answer
        )

    return render(
        request,
        "quizzes/edit_answer.html",
        {
            "form": form,
            "answer": answer
        }
    )

@login_required
def delete_answer(request, answer_id):

    answer = get_object_or_404(
        Answer,
        id=answer_id
    )

    if answer.question.quiz.author != request.user:

        return redirect(
            "quiz_detail",
            answer.question.quiz.id
        )

    if request.method == "POST":

        quiz_id = answer.question.quiz.id

        answer.delete()

        return redirect(
            "quiz_detail",
            quiz_id
        )

    return render(
        request,
        "quizzes/delete_answer.html",
        {
            "answer": answer
        }
    )

@login_required
def delete_question(request, question_id):

    question = get_object_or_404(
        Question,
        id=question_id
    )

    if question.quiz.author != request.user:

        return redirect(
            "quiz_detail",
            question.quiz.id
        )

    if request.method == "POST":

        quiz_id = question.quiz.id

        question.delete()

        return redirect(
            "quiz_detail",
            quiz_id
        )

    return render(
        request,
        "quizzes/delete_question.html",
        {
            "question": question
        }
    )


@login_required
def toggle_like(request, quiz_id):

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id
    )

    if quiz.author == request.user:
        return redirect(
            "quiz_detail",
            quiz.id
        )

    like = QuizLike.objects.filter(
        user=request.user,
        quiz=quiz
    ).first()

    if like:

        like.delete()

    else:

        QuizLike.objects.create(
            user=request.user,
            quiz=quiz
        )

    return redirect(
        "quiz_detail",
        quiz.id
    )

@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    if (
        request.user == comment.author
        or
        request.user.is_staff
    ):

        quiz_id = comment.quiz.id

        comment.delete()

        return redirect(
            "quiz_detail",
            quiz_id
        )

    return redirect(
        "quiz_detail",
        comment.quiz.id
    )

@login_required
def toggle_favorite(request, quiz_id):

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id
    )

    favorite = Favorite.objects.filter(
        user=request.user,
        quiz=quiz
    ).first()

    if favorite:

        favorite.delete()

    else:

        Favorite.objects.create(
            user=request.user,
            quiz=quiz
        )

    return redirect(
        "quiz_detail",
        quiz.id
    )

@login_required
def favorite_quizzes(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related(
        "quiz"
    )

    return render(
        request,
        "quizzes/favorites.html",
        {
            "favorites": favorites
        }
    )

@login_required
def report_quiz(request, quiz_id):

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id
    )

    if request.user == quiz.author:

        return redirect(
            "quiz_detail",
            quiz.id
        )

    QuizReport.objects.get_or_create(
        quiz=quiz,
        reporter=request.user,
        defaults={
            "reason": "other"
        }
    )

    return redirect(
        "quiz_detail",
        quiz.id
    )