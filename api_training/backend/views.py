from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Product, LessonWatch
from .serializers import SerializerLessonWatch, UserSerializer, ProductStatsSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Max, Count, Sum, F, ExpressionWrapper, FloatField


class RegisterAccount(APIView):
    """
    Для регистрации пользователей
    """

    def post(self, request, *args, **kwargs):
        if {"password", "username"}.issubset(request.data):
            errors = {}
            try:
                validate_password(request.data["password"])
            except Exception as password_error:
                error_array = []

                for item in password_error:
                    error_array.append(item)
                return JsonResponse({"error": {"password": error_array}})
            else:
                request.data.update({})
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    user.set_password(request.data["password"])
                    user.save()
                    return JsonResponse({"Status": True})
                else:
                    return JsonResponse({"error": user_serializer.errors})
        return JsonResponse({"error": "Не указаны все необходимые аргументы"})


class LoginAccount(APIView):
    """
    Класс для авторизации пользователей
    """

    def post(self, request, *args, **kwargs):
        if {"username", "password"}.issubset(request.data):
            user = authenticate(
                request,
                username=request.data["username"],
                password=request.data["password"],
            )

            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse(
                    {"Status": True, "Token": token.key, "user_id": user.id}
                )

            return JsonResponse({"Status": False, "Errors": "Не удалось авторизовать"})

        return JsonResponse(
            {"Status": False, "Errors": "Не указаны все необходимые аргументы"}
        )


class LessonsList(ListAPIView):
    """
    Класс для выведения списка
    всех уроков по всем продуктам
    к которым пользователь имеет доступ,
    с выведением информации о статусе и времени просмотра.
    """

    serializer_class = SerializerLessonWatch
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return LessonWatch.objects.filter(user=user)


class ProductLessonsListView(ListAPIView):
    """
    Класс для выведением списка уроков
    по конкретному продукту к которому
    пользователь имеет доступ, с выведением
    информации о статусе и времени просмотра,
    а также датой последнего просмотра ролика.
    """

    serializer_class = SerializerLessonWatch
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs["product_id"]

        queryset = LessonWatch.objects.filter(
            user=user, lesson__products__id=product_id
        )

        queryset = queryset.annotate(last_watched=Max("end_time"))

        return queryset


class ProductStatsView(ListAPIView):
    """
    Класс для отображения статистики по продуктам.
    """

    serializer_class = ProductStatsSerializer

    def get_queryset(self):
        products = Product.objects.all()

        products = products.annotate(
            total_lessons_watched=Count("lessons__lessonwatch", distinct=True),
            total_watch_time=Sum(
                ExpressionWrapper(
                    F("lessons__lessonwatch__end_time")
                    - F("lessons__lessonwatch__start_time"),
                    output_field=FloatField(),
                ),
                distinct=True,
            ),
            total_students=Count("lessons__lessonwatch__user", distinct=True),
        )

        return products
