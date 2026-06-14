from django.db import models

from django.contrib.auth.models import User

CATEGORY_CHOICES = [

    ("none", "Без категории"),

    ("anime", "Аниме"),

    ("games", "Игры"),

    ("movies", "Фильмы"),

    ("series", "Сериалы"),

    ("manga", "Манга"),

    ("books", "Книги"),

    ("comics", "Комиксы"),

    ("music", "Музыка"),

    ("other", "Другое"),

]
class Quiz(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    category = models.CharField(

        max_length=20,

        choices=CATEGORY_CHOICES,

        default="none"

    )
    image = models.ImageField(
        upload_to="quiz_images/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title

class QuizLike(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "user",
            "quiz"
        )


class QuizResult(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE
    )

    score = models.IntegerField()

    total_questions = models.IntegerField()

    is_perfect = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.quiz.title}"
        )

class Question(models.Model):

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    text = models.CharField(
        max_length=500
    )

    def __str__(self):
        return self.text


class Answer(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    text = models.CharField(
        max_length=300
    )

    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.text

class Comment(models.Model):

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.author.username

class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "user",
            "quiz"
        )

    def __str__(self):

        return f"{self.user} -> {self.quiz}"

class QuizReport(models.Model):

    REASONS = [

        ("spam", "Спам"),

        ("offensive", "Оскорбительный контент"),

        ("copyright", "Нарушение авторских прав"),

        ("other", "Другое"),

    ]

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="reports"
    )

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    reason = models.CharField(
        max_length=50,
        choices=REASONS
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "quiz",
            "reporter"
        )

    def __str__(self):

        return f"{self.reporter} -> {self.quiz}"
