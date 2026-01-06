# 📝 Mini Assessment Engine (DRF)

A backend-driven **exam and assessment system** built with **Django Rest Framework**, designed to handle user registration, exam attempts, theory-based questions, and automatic grading using **text similarity algorithms**.

This project is intentionally structured to be **test-friendly via Swagger** while following **real-world backend best practices**.

---

## 🚀 Features

- User registration with course-based access control  
- JWT authentication (cookies in production, token exposed for testing)  
- Course-specific exams (Physics & Chemistry)  
- Exam attempt lifecycle (start → answer → submit → grade)  
- Theory questions (non-MCQ)  
- Automatic grading using cosine similarity & text matching  
- Swagger & Redoc API documentation  
- Secure separation of concerns (questions not exposed with exams)

---

## 🧠 Available Courses

Only the following courses are supported:

- **physics**
- **chemistry**

⚠️ A user **must select one of these courses during registration**.  
Exams shown to a user are filtered strictly by their registered course.

---

## 🔐 Authentication Notes

- Authentication uses **JWT**
- For **testing purposes only**, the **access token is exposed in the login response**
- In **production**, tokens are stored in **HttpOnly cookies** and are **never exposed**

---

## 🧪 Recommended API Testing Flow

### 1️⃣ Login
Authenticate and obtain an access token.

- Copy the `access_token` from the response
- Click **Authorize (🔒)** in Swagger
- Enter:

```
Bearer <access_token>
```

---

### 2️⃣ Register
**POST /core/register/**

You **must include a course** during registration.

```json
{
  "email": "tester@example.com",
  "password": "StrongPassword123",
  "course": "physics"
}
```

Valid courses:
- `physics`
- `chemistry`

---

### 3️⃣ Get Available Exams
**GET /core/exams/**

- Returns exams available **only for the user’s registered course**
- Includes `exam_id`, title, duration, etc.
- Questions are **not exposed** here

---

### 4️⃣ Start an Exam
**POST /core/exam-attempts/**

```json
{
  "exam": "<exam_id>"
}
```

- Generates an **exam attempt**
- Returns `attempt_id` and exam metadata
- This step initializes the exam session

---

### 5️⃣ Get Exam Questions
**GET /core/exams/{exam_id}/questions/**

- Returns question IDs and question text only
- No answers, keywords, or grading data are exposed

---

### 6️⃣ Submit Exam
**POST /core/exam-attempts/{attempt_id}/submit/**

```json
{
  "answers": [
    {
      "question": "<question_id>",
      "text_answer": "Your answer here"
    }
  ]
}
```

- Answers are graded automatically
- Grading uses cosine similarity and text matching

---

### 7️⃣ View Submitted Exam
**GET /core/exam-attempts/{attempt_id}/**

- View submitted answers
- See completion status and final score

---

## 📘 API Documentation

- Swagger UI: `/swagger/`
- Redoc UI: `/redoc/`

---

## ⚠️ Important Notes

- Follow the flow strictly:

  **Login → Register → Get Exams → Start Exam → Get Questions → Submit Exam → View Attempt**

- Tokens are exposed **only for testing**
- Production setup uses secure cookie-based authentication

---

## 📄 License

This project is for educational and assessment purposes.
