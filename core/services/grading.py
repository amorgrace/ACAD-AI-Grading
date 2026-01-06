# core/services/grading.py
import re
from typing import Tuple
from ..models import ExamAttempt

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class GradingService:

    @staticmethod
    def normalize(text: str) -> str:
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def calculate_score(attempt: ExamAttempt) -> Tuple[int, int]:
        if not attempt.is_completed:
            return 0, 0

        total_score = 0
        max_possible = 0

        answers = attempt.answers.select_related("question")

        for answer in answers:
            question = answer.question
            max_possible += question.points

            if question.question_type != "SHORT":
                continue

            student_text = GradingService.normalize(answer.text_answer)
            if not student_text:
                continue

            # ---------- KEYWORD MATCHING ----------
            if question.keywords:
                expected_keywords = {
                    GradingService.normalize(k)
                    for k in question.keywords
                }

                student_words = set(student_text.split())

                if expected_keywords:
                    matched = student_words & expected_keywords
                    match_ratio = len(matched) / len(expected_keywords)

                    if match_ratio >= 0.7:
                        total_score += question.points
                        continue

            # ---------- TF-IDF SIMILARITY ----------
            if SKLEARN_AVAILABLE and question.expected_answer:
                model_text = GradingService.normalize(question.expected_answer)

                try:
                    vectorizer = TfidfVectorizer()
                    vectors = vectorizer.fit_transform([student_text, model_text])
                    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

                    if similarity >= 0.7:
                        total_score += question.points
                except Exception:
                    pass

        return total_score, max_possible

    @staticmethod
    def update_attempt_score(attempt: ExamAttempt) -> int:
        score, max_possible = GradingService.calculate_score(attempt)
        attempt.score = score
        attempt.max_possible = max_possible
        attempt.save(update_fields=["score", "max_possible"])
        return score
