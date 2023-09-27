from backend.views import (
    LessonsList,
    RegisterAccount,
    LoginAccount,
    ProductLessonsListView,
    ProductStatsView,
)
from django.urls import path


urlpatterns = [
    path("register/", RegisterAccount.as_view()),
    path("login/", LoginAccount.as_view()),
    path("lessons/", LessonsList.as_view()),
    path("products/<int:product_id>/", ProductLessonsListView.as_view()),
    path("product-stats/", ProductStatsView.as_view()),
]
