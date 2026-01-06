from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            email=attrs["email"],
            password=attrs["password"]
        )

        if not user:
            raise serializers.ValidationError(
                {"detail": "Invalid user credentials"}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"detail": "Account disabled"}
            )

        attrs["user"] = user
        return attrs

    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        required=True,
    )

    def validate_refresh(self, value):
        if not value:
            raise serializers.ValidationError("Refresh token is required")
        return value
    


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    courses = serializers.ChoiceField(
        choices=User.COURSE_CHOICES,
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "courses",
        )

    def validate(self, attrs):
        if attrs.get("password") != attrs.pop("confirm_password", None):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        return {
            "message": "Account created successfully!",
            "user": {
                "email": instance.email,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "courses": instance.courses
            }
        }
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "student_id",
            "first_name",
            "last_name",
            "email",
            "courses",
        ]