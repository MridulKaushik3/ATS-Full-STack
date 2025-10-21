from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import ResumeRecord
from .serializers import ResumeRecordSerializer
from .gemini_evaluator import evaluate_resume
import re

class ResumeEvaluationAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        resume = request.FILES['resume_file']
        jd = request.data['job_description']
        prompt = """
You are an expert in Resume Evaluation and ATS (Applicant Tracking System) matching.

Your task is to:
1. Carefully compare the resume content (provided as images) with the job description.
2. Identify matching and missing skills, technologies, and keywords relevant to the job.
3. Provide a score out of 100 that reflects how well the resume aligns with the job description.
4. List the most important missing keywords or skills from the resume that are required by the job.
5. Conclude with final thoughts, highlighting strengths and suggesting improvements if any.

Your response should follow this exact structure:

Score: <score in %>

Missing Keywords:
- <keyword 1>
- <keyword 2>
...

Final Thoughts:
<Write a short paragraph (3–5 lines) about the resume’s strengths and what can be improved.>

Begin analysis now.
"""


        result = evaluate_resume(resume, jd, prompt)

        lines = result.strip().split('\n')
        
        # Try to extract a line like "85%" using regex
        score = 0
        for line in lines:
            match = re.search(r'(\d+)\s*%', line)
            if match:
                score = int(match.group(1))
                break

        keywords = "\n".join([line for line in lines if 'missing' in line.lower()])
        thoughts = lines[-1] if lines else ""

        record = ResumeRecord.objects.create(
            job_description=jd,
            resume_file=resume,
            score=score,
            keywords_missing=keywords,
            final_thoughts=thoughts
        )

        return Response(ResumeRecordSerializer(record).data)
