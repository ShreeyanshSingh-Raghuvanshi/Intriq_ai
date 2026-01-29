from fastapi import FastAPI, HTTPException, Response
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

@app.head("/health")
def health(response: Response):
    response.headers["X-version"] = "1.0"
    return Response(status_code=200)



if __name__ == "__main__":
    import uvicorn
    # NOTE: This runs on port 8000. 
    # Make sure your frontend calls http://localhost:8000, NOT port 5000.
    uvicorn.run(app, host="0.0.0.0", port=8000)
