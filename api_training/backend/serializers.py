from rest_framework import serializers
from .models import User, Product, LessonWatch


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
        read_only_fields = ("id",)


class SerializerLessonWatch(serializers.ModelSerializer):
    class Meta:
        model = LessonWatch
        fields = "__all__"


class ProductStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "user", "lessons")
        read_only_fields = fields
