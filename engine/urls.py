"""
URL configuration for engine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response

schema_view = get_schema_view(
    openapi.Info(
        title="Mini Assesment Engine",
        default_version="v1",
            description="""
                ### 📌 Tester/Student Testing Flow Guide

                    This is a simple, secure API for managing and taking **short-answer exams** (text-based responses only).  
                    The system supports automatic grading using a combination of **keyword matching** and **cosine similarity with TF-IDF** (powered by scikit-learn).

                    This API is designed for testing a simple exam system (Physics & Chemistry only).

                    **Important notes:**
                    - Login endpoint returns `access_token` directly in the response **only for testing convenience**
                    - In real production this token would be stored in HttpOnly cookie and **never** exposed in body

                    ### Step-by-step Testing Process

                    1. **Registration**  
                    `POST /auth/register/`  
                    Required fields include (among others):
                    ```json
                    {
                        "first_name": "...",
                        "last_name": "...",
                        "email": "...",
                        "password": "...",
                        "course": "physics" or "chemistry" - mandatory field!
                    }
                    #### 1️⃣ Login
                        - Endpoint: POST /auth/login/
                        - Purpose: Authenticate and obtain an access token.
                        - Notes:
                        - The access token is exposed **only for testing**.
                        - In production, tokens are stored in HttpOnly cookies.
                        - Steps:
                        1. Copy the `access_token` from login response.
                        2. Click **Authorize (🔒)** in Swagger.
                        3. Enter: `Bearer <access_token>` (replace `<access_token>`).
                        4. Click **Authorize** to authenticate.

                    ### START EXAM
                     1. A candidate can begin an exam by submitting a POST request to /core/exam-attempts/ with the exam ID. This initializes the attempt and returns its unique metadata and attempt_id.
                     2. To retrieve the exam questions, send a GET request to /core/exams/{exam_id}/questions/.
                     3. Once completed, submit the answers by sending a POST request to /core/exam-attempts/{attempt_id}/submit/ with a JSON body containing an array of answers.
                     4. Each answer must include the question ID and the candidate's text_answer.
                     5. Upon submission, answers are automatically graded using a text-matching algorithm based on cosine similarity. The graded results are immediately returned in the response.
                     6. To review a submitted attempt, send a GET request to /core/exam-attempts/{attempt_id}/
        """
    ),
    public=True,
    permission_classes=[AllowAny],
)
@api_view(['GET'])
def root_info(request):
    return Response({
        "message": "Welcome to Mini Assessment Engine API! 📝",
        "instructions": "Please visit /swagger/ to explore and test all endpoints."
    })

urlpatterns = [
    path('', root_info, name='root-info'),
    path('admin/', admin.site.urls),
    path('core/', include("core.urls")),
    path('auth/', include("authenticator.urls")),

    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
]
