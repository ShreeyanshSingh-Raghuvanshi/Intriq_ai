# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from engine import call_llama, generate_ai_response # Updated imports
# import json

# app = FastAPI()

# class ResumeData(BaseModel):
#     text: str

# class GenericPrompt(BaseModel):
#     prompt: str
#     system_prompt: str = "You are an AI Interview Career Coach."

# @app.post("/generate")
# async def generate(data: GenericPrompt):
#     """General purpose endpoint for any AI prompt from the backend."""
#     try:
#         result = generate_ai_response(data.prompt, data.system_prompt)
#         return json.loads(result) # Return as an actual JSON object
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/analyze-resume")
# async def analyze_resume(data: ResumeData):
#     prompt = f"Analyze this resume for ATS and career growth: {data.text}. Return JSON with score and tips."
#     result = call_llama(prompt, "You are an ATS Expert.")
#     return json.loads(result)

# # ... keep your other existing endpoints ...

# @app.post("/generate-questions")
# async def questions(data: dict):
#     prompt = f"Generate {data['count']} questions for {data['role']} type {data['type']}."
#     result = call_llama(prompt, "You are a Technical Recruiter.")
#     return json.loads(result)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)










# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from engine import call_llama, generate_ai_response
# import json

# app = FastAPI()

# class ResumeData(BaseModel):
#     text: str

# class QuestionRequest(BaseModel):
#     skills: list[str]
#     role: str
#     difficulty: int
#     history: list[dict] # Previous Q&A to avoid repetition and gauge context

# class AnswerAnalysisRequest(BaseModel):
#     question: str
#     answer: str
#     role: str

# @app.post("/generate-next-question")
# async def generate_next_question(data: QuestionRequest):
#     """
#     Generates a single question based on role, skills, and current difficulty (1-10).
#     Considers history to avoid repeats.
#     """
#     # Create a summary of history for the prompt
#     history_text = "\n".join([f"Q: {h['question']}" for h in data.history[-3:]]) # Keep last 3 for context
    
#     prompt = f"""
#     You are an expert Technical Interviewer for a {data.role} position.
#     Candidate Skills: {', '.join(data.skills)}.
#     Current Difficulty Level: {data.difficulty}/10.
    
#     Recent questions asked:
#     {history_text}
    
#     Generate ONE single interview question. 
#     If the difficulty is high (8-10), ask complex scenario-based or architectural questions.
#     If the difficulty is low (1-4), ask fundamental concept questions.
    
#     Return ONLY a JSON object: {{ "question": "The question text here", "type": "technical/behavioral" }}
#     """
    
#     try:
#         result = call_llama(prompt, "You are a strict but fair Interviewer.")
#         return json.loads(result)
#     except Exception as e:
#         # Fallback if JSON parsing fails
#         return {"question": f"Could you explain your experience with {data.skills[0] if data.skills else 'software'}?", "type": "fallback"}

# @app.post("/analyze-answer")
# async def analyze_answer(data: AnswerAnalysisRequest):
#     """
#     Analyzes an answer to decide if difficulty should increase, decrease, or stay same.
#     """
#     prompt = f"""
#     Role: {data.role}
#     Question: {data.question}
#     Candidate Answer: {data.answer}
    
#     Evaluate this answer. 
#     1. Give a score (0-100).
#     2. Suggest if next question difficulty should change (+1 for good, -1 for bad, 0 for neutral).
#     3. Provide brief feedback.
    
#     Return JSON: {{ "score": 85, "difficulty_adjustment": 1, "feedback": "Good explanation of..." }}
#     """
    
#     result = call_llama(prompt, "You are a Senior Technical Recruiter.")
#     return json.loads(result)

# # Keep existing endpoints
# @app.post("/analyze-resume")
# async def analyze_resume(data: ResumeData):
    
#     prompt = f"Analyze this resume for ATS and career growth: {data.text}. Return JSON with score and tips."
#     result = call_llama(prompt, "You are an ATS Expert.")
#     return json.loads(result)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
















# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from engine import call_llama
# import json

# app = FastAPI()

# class QuestionRequest(BaseModel):
#     skills: list[str] = []
#     role: str
#     interview_type: str  # "Technical", "HR", "Behavioral"
#     difficulty: int
#     history: list[dict] # Previous Q&A to avoid repetition
#     resume_text: str = "" # Optional extracted text from resume

# class AnswerAnalysisRequest(BaseModel):
#     question: str
#     answer: str
#     role: str
#     difficulty: int

# @app.post("/generate-next-question")
# async def generate_next_question(data: QuestionRequest):
#     """
#     Generates a single question based on role, interview type, and current difficulty (1-10).
#     """
#     # Create context from history
#     history_text = "\n".join([f"Q: {h['question']}" for h in data.history[-5:]]) 
    
#     system_prompt = f"You are an expert {data.interview_type} Interviewer for a {data.role} role."
    
#     prompt = f"""
#     Context:
#     - Role: {data.role}
#     - Interview Type: {data.interview_type}
#     - Skills: {', '.join(data.skills)}
#     - Current Difficulty: {data.difficulty}/10
    
#     Previous Questions asked (DO NOT REPEAT THESE):
#     {history_text}
    
#     Task:
#     Generate ONE {data.interview_type} interview question.
#     - If difficulty is 1-4: Ask fundamental/basic questions.
#     - If difficulty is 5-7: Ask intermediate/scenario-based questions.
#     - If difficulty is 8-10: Ask advanced architectural, trick, or deep-dive questions.
    
#     Return ONLY a raw JSON object (no markdown): 
#     {{ "question": "The question text", "type": "{data.interview_type}" }}
#     """
    
#     try:
#         result = call_llama(prompt, system_prompt)
#         return json.loads(result)
#     except Exception as e:
#         return {"question": f"Could you explain your core expertise in {data.role}?", "type": "fallback"}

# @app.post("/analyze-answer")
# async def analyze_answer(data: AnswerAnalysisRequest):
#     """
#     Analyzes an answer and suggests difficulty adjustment.
#     """
#     system_prompt = "You are a Senior Technical Recruiter and Subject Matter Expert."
    
#     prompt = f"""
#     Role: {data.role}
#     Current Difficulty: {data.difficulty}
#     Question: {data.question}
#     Candidate Answer: {data.answer}
    
#     Evaluate the answer:
#     1. Score (0-100).
#     2. Difficulty Adjustment: 
#        - If answer is excellent: +1 (increase difficulty)
#        - If answer is poor/wrong: -1 (decrease difficulty)
#        - If average: 0 (stay same)
#     3. Feedback: Brief, constructive tips.
    
#     Return ONLY a raw JSON object (no markdown): 
#     {{ "score": 85, "difficulty_adjustment": 1, "feedback": "Good explanation..." }}
#     """
    
#     try:
#         result = call_llama(prompt, system_prompt)
#         return json.loads(result)
#     except Exception as e:
#         return {"score": 0, "difficulty_adjustment": 0, "feedback": "Error analyzing response."}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)









# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from engine import call_llama
# import json

# app = FastAPI()

# class QuestionRequest(BaseModel):
#     skills: list[str] = []
#     role: str
#     interview_type: str = "Technical"
#     difficulty: int = 5
#     history: list[dict] = []
#     resume_text: str = ""

# class AnswerAnalysisRequest(BaseModel):
#     question: str
#     answer: str
#     role: str
#     difficulty: int = 5

# class RoadmapRequest(BaseModel):
#     skills: list[str]
#     role: str
#     goal: str = "Job Ready"

# @app.post("/generate-next-question")
# async def generate_next_question(data: QuestionRequest):
#     # Fix KeyError: Safe access to 'question' key
#     history_text = ""
#     if data.history:
#         history_lines = []
#         for h in data.history[-5:]:
#             q_text = h.get('question', 'Unknown Question')
#             history_lines.append(f"Q: {q_text}")
#         history_text = "\n".join(history_lines)
    
#     prompt = f"""
#     Context:
#     - Role: {data.role}
#     - Type: {data.interview_type}
#     - Skills: {', '.join(data.skills)}
#     - Difficulty: {data.difficulty}/10
    
#     Previous Questions (AVOID THESE):
#     {history_text}
    
#     Generate ONE interview question.
#     Return JSON: {{ "question": "Question text", "type": "{data.interview_type}" }}
#     """
    
#     result = call_llama(prompt, f"You are a {data.role} Interviewer.")
#     return json.loads(result)

# @app.post("/analyze-answer")
# async def analyze_answer(data: AnswerAnalysisRequest):
#     prompt = f"""
#     Question: {data.question}
#     Answer: {data.answer}
#     Role: {data.role}
    
#     Evaluate (0-100), adjust difficulty (+1/-1/0), and give feedback.
#     Return JSON: {{ "score": 80, "difficulty_adjustment": 1, "feedback": "..." }}
#     """
#     result = call_llama(prompt, "You are a Technical Recruiter.")
#     return json.loads(result)

# @app.post("/generate-roadmap")
# async def generate_roadmap(data: RoadmapRequest):
#     prompt = f"""
#     Create a 4-week learning roadmap for a {data.role}.
#     Current Skills: {', '.join(data.skills)}.
    
#     Return JSON: {{ "roadmap": [ {{"week": "Week 1", "topic": "...", "details": "..."}} ... ] }}
#     """
#     result = call_llama(prompt, "You are a Career Coach.")
#     return json.loads(result)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
















# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from engine import call_llama
# import json
# import random

# app = FastAPI()

# # --- Data Models ---
# class QuestionRequest(BaseModel):
#     skills: list[str] = []
#     role: str
#     interview_type: str = "Technical"
#     difficulty: int = 5
#     history: list[dict] = [] # List of {question: str, answer: str}

# class AnswerAnalysisRequest(BaseModel):
#     question: str
#     answer: str
#     role: str
#     difficulty: int = 5

# class PremiumRequest(BaseModel):
#     skills: list[str]
#     role: str
#     goal: str = "Job Ready"

# # --- Endpoints ---

# @app.post("/generate-next-question")
# async def generate_next_question(data: QuestionRequest):
#     # Format history to prevent repetition
#     history_text = ""
#     if data.history:
#         # Take last 10 questions to ensure variety
#         recent = data.history[-10:] 
#         history_text = "\n".join([f"- Q: {h.get('question', '')}" for h in recent])

#     prompt = f"""
#     Role: {data.role}
#     Interview Type: {data.interview_type}
#     Current Difficulty: {data.difficulty}/10
    
#     Previous Questions (DO NOT REPEAT):
#     {history_text}
    
#     Generate ONE {data.interview_type} interview question.
#     - If previous questions were about Topic A, switch to Topic B.
#     - Difficulty {data.difficulty}: { "Basic concepts" if data.difficulty < 4 else "Complex scenarios" }.
    
#     Return JSON: {{ "question": "Question text", "type": "{data.interview_type}" }}
#     """
    
#     result = call_llama(prompt, f"You are an expert {data.role} Interviewer.")
#     return json.loads(result)

# @app.post("/analyze-answer")
# async def analyze_answer(data: AnswerAnalysisRequest):
#     prompt = f"""
#     Question: {data.question}
#     Answer: {data.answer}
#     Role: {data.role}
    
#     1. Score (0-100).
#     2. Adjustment: +1 (Good), -1 (Bad), 0 (Average).
#     3. Feedback: Constructive criticism.
    
#     Return JSON: {{ "score": 85, "difficulty_adjustment": 1, "feedback": "..." }}
#     """
#     result = call_llama(prompt, "You are a Senior Recruiter.")
#     return json.loads(result)

# # --- Premium Features ---

# @app.post("/generate-flashcards")
# async def generate_flashcards(data: PremiumRequest):
#     prompt = f"""
#     Create 5 technical flashcards for a {data.role} with skills: {', '.join(data.skills)}.
#     Focus on hard interview questions.
    
#     Return JSON: {{ "flashcards": [ {{"front": "Question...", "back": "Answer..."}} ] }}
#     """
#     result = call_llama(prompt)
#     return json.loads(result)

# @app.post("/gap-analysis")
# async def gap_analysis(data: PremiumRequest):
#     prompt = f"""
#     Perform a gap analysis for a {data.role}.
#     User Skills: {', '.join(data.skills)}.
    
#     Identify 3 missing critical skills and how to learn them.
#     Return JSON: {{ "gaps": [ {{"skill": "Docker", "recommendation": "Learn containerization..."}} ] }}
#     """
#     result = call_llama(prompt)
#     return json.loads(result)

# @app.post("/career-guide")
# async def career_guide(data: PremiumRequest):
#     prompt = f"""
#     Create a career growth plan for a {data.role} aiming for {data.goal}.
#     Return JSON: {{ "steps": ["Step 1...", "Step 2..."], "salary_insight": "..." }}
#     """
#     result = call_llama(prompt)
#     return json.loads(result)

# @app.post("/generate-roadmap")
# async def generate_roadmap(data: PremiumRequest):
#     prompt = f"""
#     Create a 4-week learning roadmap for {data.role}.
#     Return JSON: {{ "roadmap": [ {{"week": "Week 1", "topic": "...", "details": "..."}} ] }}
#     """
#     result = call_llama(prompt)
#     return json.loads(result)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)













# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from engine import call_groq
# import json
# import random

# app = FastAPI()

# # --- Data Models ---
# class QuestionRequest(BaseModel):
#     skills: list[str] = []
#     role: str
#     interview_type: str = "Technical"
#     difficulty: int = 5
#     history: list[dict] = [] 

# class AnswerAnalysisRequest(BaseModel):
#     question: str
#     answer: str
#     role: str
#     difficulty: int = 5

# class MCQRequest(BaseModel):
#     skills: list[str]
#     role: str
#     difficulty: int = 5

# class PremiumRequest(BaseModel):
#     skills: list[str]
#     role: str
#     goal: str = "Job Ready"

# # --- Endpoints ---

# @app.post("/generate-next-question")
# async def generate_next_question(data: QuestionRequest):
#     # History context
#     history_context = ""
#     if data.history:
#         recent = data.history[-5:]
#         history_context = "\n".join([f"- Asked: {h.get('question', '')}" for h in recent])

#     prompt = f"""
#     You are interviewing a candidate for a {data.role} position.
#     Skills: {', '.join(data.skills)}.
#     Difficulty: {data.difficulty}/10.

#     History (DO NOT REPEAT):
#     {history_context}

#     Task: Generate ONE unique interview question.
#     CONSTRAINT: Keep the question SHORT and CONCISE (max 2 sentences).
    
#     Return ONLY JSON: {{ "question": "...", "type": "{data.interview_type}" }}
#     """
    
#     response = call_groq(prompt, f"You are a strict {data.role} interviewer.")
#     return json.loads(response)

# @app.post("/generate-mcq")
# async def generate_mcq(data: MCQRequest):
#     prompt = f"""
#     Generate ONE Multiple Choice Question (MCQ) for a {data.role}.
#     Skills: {', '.join(data.skills)}.
#     Difficulty: {data.difficulty}/10.

#     Return ONLY JSON:
#     {{
#       "question": "Question text here...",
#       "options": ["Option A", "Option B", "Option C", "Option D"],
#       "correct_answer": "Option A",
#       "explanation": "Brief explanation why."
#     }}
#     """
#     response = call_groq(prompt)
#     return json.loads(response)

# @app.post("/analyze-answer")
# async def analyze_answer(data: AnswerAnalysisRequest):
#     prompt = f"""
#     Role: {data.role}
#     Question: {data.question}
#     Candidate Answer: {data.answer}
    
#     Task: Evaluate strictly.
#     1. Score (0-100).
#     2. Difficulty Adjustment: +1 (Good), -1 (Bad), 0 (Average).
#     3. Feedback: Concise advice.
    
#     Return ONLY JSON: {{ "score": 85, "difficulty_adjustment": 1, "feedback": "..." }}
#     """
#     response = call_groq(prompt, "You are a Technical Recruiter.")
#     return json.loads(response)

# @app.post("/evaluate-voice")
# async def evaluate_voice(data: VoiceEvaluationRequest):
#     prompt = f"""
#     Role: {data.role}
#     Question: {data.question}
#     Voice Transcript: "{data.answer}"
    
#     Task: Analyze the candidate's spoken communication.
#     1. Check for clarity, confidence, and filler words.
#     2. Check technical accuracy.
    
#     Return ONLY JSON: 
#     {{ 
#         "score": 85, 
#         "feedback": "Your delivery was confident, but you missed...", 
#         "clarity_score": 90, 
#         "technical_accuracy": 80 
#     }}
#     """
#     response = call_groq(prompt, "You are a Voice & Communication Coach.")
#     return json.loads(response)

# @app.post("/generate-roadmap")
# async def generate_roadmap(data: PremiumRequest):
#     prompt = f"""
#     Create a personalized 4-week study roadmap for a {data.role}.
#     User Skills: {', '.join(data.skills)}.
#     Goal: {data.goal}.
    
#     Return ONLY JSON: 
#     {{ "roadmap": [ {{"week": 1, "topic": "...", "details": "...", "youtube_search_term": "..."}} ] }}
#     """
#     response = call_groq(prompt, "You are a Career Strategist.")
#     return json.loads(response)

# @app.post("/generate-flashcards")
# async def generate_flashcards(data: PremiumRequest):
#     prompt = f"""
#     Generate 5 advanced technical flashcards for a {data.role} expert.
#     Skills: {', '.join(data.skills)}.
    
#     Return ONLY JSON: {{ "flashcards": [ {{"front": "Question", "back": "Detailed Answer"}} ] }}
#     """
#     response = call_groq(prompt)
#     return json.loads(response)

# @app.post("/career-guide")
# async def career_guide(data: PremiumRequest):
#     prompt = f"""
#     Analyze career paths for a {data.role} with skills: {', '.join(data.skills)}.
#     Provide 3 distinct paths (e.g., IC, Management, Startup).
    
#     Return ONLY JSON: {{ "paths": [ {{"title": "...", "description": "...", "salary_range": "..."}} ] }}
#     """
#     response = call_groq(prompt)
#     return json.loads(response)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)







from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <--- Added this
from pydantic import BaseModel
from engine import call_groq
import json
import random

app = FastAPI()

# --- ADDED: Fix for Browser/CORS Errors ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change to specific URL in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- 1. Define All Data Models First ---

class QuestionRequest(BaseModel):
    skills: list[str] = []
    role: str
    interview_type: str = "Technical"
    difficulty: int = 5
    history: list[dict] = [] 

class AnswerAnalysisRequest(BaseModel):
    question: str
    answer: str
    role: str
    difficulty: int = 5

class VoiceEvaluationRequest(BaseModel):
    question: str
    answer: str
    role: str

class MCQRequest(BaseModel):
    skills: list[str] = []
    role: str
    difficulty: int = 5

class PremiumRequest(BaseModel):
    skills: list[str]
    role: str
    goal: str = "Job Ready"

# --- 2. Endpoints ---

@app.post("/generate-next-question")
async def generate_next_question(data: QuestionRequest):
    history_text = ""
    if data.history:
        recent = data.history[-5:]
        history_text = "\n".join([f"- Asked: {h.get('question', '')}" for h in recent])

    prompt = f"""
    You are interviewing a candidate for a {data.role} position.
    Skills: {', '.join(data.skills)}.
    Difficulty: {data.difficulty}/10.

    History (DO NOT REPEAT):
    {history_text}

    Task: Generate ONE unique interview question.
    CONSTRAINT: Keep the question SHORT (max 2 sentences).
    
    Return ONLY JSON: {{ "question": "...", "type": "{data.interview_type}" }}
    """
    
    response = call_groq(prompt, f"You are a strict {data.role} interviewer.")
    return json.loads(response)

@app.post("/generate-mcq")
async def generate_mcq(data: MCQRequest):
    prompt = f"""
    Generate ONE Multiple Choice Question (MCQ) for a {data.role}.
    Skills: {', '.join(data.skills)}.
    Difficulty: {data.difficulty}/10.

    Return ONLY JSON:
    {{
      "question": "Question text here...",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Brief explanation why."
    }}
    """
    response = call_groq(prompt)
    return json.loads(response)

@app.post("/analyze-answer")
async def analyze_answer(data: AnswerAnalysisRequest):
    prompt = f"""
    Role: {data.role}
    Question: {data.question}
    Candidate Answer: {data.answer}
    
    Task: Evaluate strictly.
    1. Score (0-100).
    2. Difficulty Adjustment: +1 (Good), -1 (Bad), 0 (Average).
    3. Feedback: Concise advice.
    
    Return ONLY JSON: {{ "score": 85, "difficulty_adjustment": 1, "feedback": "..." }}
    """
    response = call_groq(prompt, "You are a Technical Recruiter.")
    return json.loads(response)

@app.post("/evaluate-voice")
async def evaluate_voice(data: VoiceEvaluationRequest):
    prompt = f"""
    Role: {data.role}
    Question: {data.question}
    Voice Transcript: "{data.answer}"
    
    Task: Analyze the candidate's spoken communication.
    1. Check for clarity, confidence, and filler words.
    2. Check technical accuracy.
    
    Return ONLY JSON: 
    {{ 
        "score": 85, 
        "feedback": "Your delivery was confident, but you missed...", 
        "clarity_score": 90, 
        "technical_accuracy": 80 
    }}
    """
    response = call_groq(prompt, "You are a Voice & Communication Coach.")
    return json.loads(response)

# --- Premium Endpoints ---

@app.post("/generate-roadmap")
async def generate_roadmap(data: PremiumRequest):
    prompt = f"""
    Create a 4-week study roadmap for {data.role}.
    Return JSON: {{ "roadmap": [ {{"week": 1, "topic": "...", "details": "..."}} ] }}
    """
    response = call_groq(prompt)
    # FIX: Changed 'result' to 'response' below
    return json.loads(response) 

@app.post("/generate-flashcards")
async def generate_flashcards(data: PremiumRequest):
    prompt = f"""
    Generate 5 flashcards for {data.role}.
    Return JSON: {{ "flashcards": [ {{"front": "...", "back": "..."}} ] }}
    """
    response = call_groq(prompt)
    return json.loads(response)

@app.post("/career-guide")
async def career_guide(data: PremiumRequest):
    prompt = f"""
    Suggest career paths for {data.role}.
    Return JSON: {{ "paths": [ {{"title": "...", "description": "..."}} ] }}
    """
    response = call_groq(prompt)
    return json.loads(response)

@app.post("/gap-analysis")
async def gap_analysis(data: PremiumRequest):
    prompt = f"""
    Analyze skill gaps for {data.role}.
    Return JSON: {{ "gaps": [ {{"skill": "...", "recommendation": "..."}} ] }}
    """
    response = call_groq(prompt)
    return json.loads(response)

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    # NOTE: This runs on port 8000. 
    # Make sure your frontend calls http://localhost:8000, NOT port 5000.
    uvicorn.run(app, host="0.0.0.0", port=8000)