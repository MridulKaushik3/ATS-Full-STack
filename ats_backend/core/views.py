from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .hf_evaluator import evaluate_resume
from .utils.resume_parser import extract_text_from_pdf
import re

class ResumeEvaluationAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        resume_file = request.FILES['resume_file']
        jd = request.data['job_description']

        # Extract text from uploaded PDF
        resume_text = extract_text_from_pdf(resume_file)

        # Prepare prompt for AI evaluation
        prompt = """
You are an expert in Resume Evaluation and ATS (Applicant Tracking System) matching.

Your task is to:
1. Compare the resume with the job description.
2. Identify matching and missing skills.
3. Give an ATS score out of 100.
4. List missing keywords.
5. Provide final improvement suggestions.

Response format:

Score: <number>%

Missing Keywords:
- keyword1
- keyword2

Final Thoughts:
<short paragraph>
"""

        # Get AI evaluation result
        result = evaluate_resume(resume_text, jd, prompt)

        # Parse the result
        score = 0
        match = re.search(r'(\d+)\s*%', result)
        if match:
            score = int(match.group(1))

        keywords = "\n".join(
            line for line in result.splitlines()
            if line.strip().startswith("-")
        )

        thoughts_match = re.search(
            r'Final Thoughts:\s*(.*)', result, re.DOTALL
        )
        thoughts = thoughts_match.group(1).strip() if thoughts_match else ""

        # Return response directly without saving to database
        return Response({
            'score': score,
            'keywords_missing': keywords,
            'final_thoughts': thoughts
        })