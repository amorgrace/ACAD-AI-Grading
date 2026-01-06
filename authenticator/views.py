
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import generics, permissions
from .serializers import RegisterUserSerializer, UserSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    @swagger_auto_schema(
        operation_description=(
            "💡 Tester Note: The access token is exposed in the response "
            "only for easier testing in Swagger. I will NEVER expose access_token in PRODUCTION. Use this token with the "
            "Authorize button to access protected endpoints."

            "To access endpoints as a logged-in user,"
            " copy the Access Token from the login response. Click the"
            " padlock (Authorize), enter it as Bearer <access_token>,"
            " and then click Authorize. You will now be authenticated for testing."
        ))

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        response = Response({
            "detail": "Login is successful",
            "access_token": access,
        }, status=200)

        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=access,
            max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
            httponly=True,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            path="/",
        )

        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
            value=str(refresh),
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
            httponly=True,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            path="/",
        )

        return response
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass 

        response = Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])

        return response


class GetUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        operation_description=(
            "💡 Tester Note: To access endpoints as a logged-in user,"
            " copy the Access Token from the login response. Click the"
            " padlock (Authorize), enter it as Bearer <access_token>,"
            " and then click Authorize. You will now be authenticated for testing."
        ))
    def get(self, request, student_id):
        try:
            user = User.objects.get(student_id=student_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="💡 Tester Note: When registering make sure to choose between physics or chemistry as course."
        " These are the only course exams available for testing.",
        responses={201: "User created successfully"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)