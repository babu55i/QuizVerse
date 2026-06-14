from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings

from django.conf.urls.static import static


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("users.urls")
    ),

    path(
        "quiz/",
        include("quizzes.urls")
    ),

]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

handler404 = "django.views.defaults.page_not_found"
handler403 = "django.views.defaults.permission_denied"
handler500 = "django.views.defaults.server_error"