# import os
# import requests
# import json
# from dotenv import load_dotenv

# load_dotenv()

# LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
# MODEL = "gpt-oss:120b-cloud"

# def call_llama(prompt, system_message="You are an AI Interview Career Coach."):
#     url = "https://api.llama-api.com/chat/completions" # Update based on provider
#     headers = {
#         "Authorization": f"Bearer {LLAMA_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model": MODEL,
#         "messages": [
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": prompt}
#         ],
#         "response_format": { "type": "json_object" }
#     }
    
#     response = requests.post(url, headers=headers, json=payload)
#     return response.json()['choices'][0]['message']['content']/













# import os
# import requests
# import json
# import re
# from dotenv import load_dotenv

# load_dotenv()

# # Use environment variables from your ai/.env file
# LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
# MODEL = os.getenv("LLAMA_MODEL", "gpt-oss:120b-cloud")

# def call_llama(prompt, system_message="You are an AI Interview Career Coach."):
#     """Calls the Llama API and ensures the output is a clean JSON string."""
#     url = "https://api.llama-api.com/chat/completions" 
#     headers = {
#         "Authorization": f"Bearer {LLAMA_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model": MODEL,
#         "messages": [
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": prompt}
#         ],
#         "response_format": { "type": "json_object" }
#     }
    
#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()
#         content = response.json()['choices'][0]['message']['content']
        
#         # Clean the string in case the LLM wraps it in markdown (```json ... ```)
#         return clean_json_string(content)
#     except Exception as e:
#         print(f"Error calling Llama API: {e}")
#         return json.dumps({"error": "AI service unavailable", "details": str(e)})

# def clean_json_string(text):
#     """Helper to remove markdown formatting if the AI includes it."""
#     return re.sub(r'^```json\s*|\s*```$', '', text.strip(), flags=re.MULTILINE)

# # Alias for consistent naming with your existing backend controllers
# def generate_ai_response(prompt, system_message="You are an AI Interview Career Coach."):
#     return call_llama(prompt, system_message)














# import os
# import requests
# import json
# import re
# from dotenv import load_dotenv

# load_dotenv()

# LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
# # Default to a widely available model if specific one fails
# MODEL = os.getenv("LLAMA_MODEL", "llama3-70b") 

# def call_llama(prompt, system_message="You are an AI Interview Career Coach."):
#     """
#     Calls the Llama API. 
#     FALLBACK: If the API fails (404, 500, auth error), it returns a MOCK response 
#     so the user can still use the app.
#     """
#     # URL for LlamaAPI.com (Verify this is the provider you are using)
#     # If using Groq or another provider, change this URL.
#     url = "https://api.llama-api.com/chat/completions" 
    
#     headers = {
#         "Authorization": f"Bearer {LLAMA_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model": MODEL,
#         "messages": [
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": prompt}
#         ],
#         "response_format": { "type": "json_object" }
#     }
    
#     try:
#         response = requests.post(url, headers=headers, json=payload, timeout=10)
        
#         if response.status_code != 200:
#             print(f"⚠️ API Error {response.status_code}: {response.text}")
#             raise Exception(f"API Error {response.status_code}")
            
#         content = response.json()['choices'][0]['message']['content']
#         return clean_json_string(content)
        
#     except Exception as e:
#         print(f"❌ AI Service Failed: {e}. Switching to Mock Response.")
#         return generate_mock_response(prompt)

# def clean_json_string(text):
#     """Helper to remove markdown formatting."""
#     return re.sub(r'^```json\s*|\s*```$', '', text.strip(), flags=re.MULTILINE)

# def generate_mock_response(prompt):
#     """Returns valid JSON structure based on the prompt content when API fails."""
#     if "interview question" in prompt.lower():
#         return json.dumps({
#             "question": "Describe a challenging technical problem you solved recently. (AI Offline Mode)",
#             "type": "behavioral"
#         })
#     elif "analyze this interview" in prompt.lower() or "score" in prompt.lower():
#         return json.dumps({
#             "score": 75,
#             "difficulty_adjustment": 0,
#             "feedback": "This is a placeholder feedback because the AI service is currently unreachable. Your answer was recorded."
#         })
#     elif "roadmap" in prompt.lower():
#         return json.dumps({
#             "roadmap": [
#                 {"week": "Week 1", "topic": "Fundamentals", "details": "Review core concepts."},
#                 {"week": "Week 2", "topic": "Advanced Topics", "details": "Deep dive into system design."}
#             ]
#         })
#     else:
#         return json.dumps({"error": "AI unavailable"})

# def generate_ai_response(prompt, system_message="You are an AI Interview Career Coach."):
#     return call_llama(prompt, system_message)






















# import os
# import requests
# import json
# import re
# import random
# from dotenv import load_dotenv
# from pathlib import Path

# # Explicitly load .env from the ai folder
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)

# LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
# MODEL = "llama3-70b" # Ensure this model name is valid for your provider

# def call_llama(prompt, system_message="You are an AI Interview Coach."):
#     url = "https://api.llama-api.com/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {LLAMA_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model": MODEL,
#         "messages": [
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": prompt}
#         ],
#         "response_format": { "type": "json_object" }
#     }

#     try:
#         # debug print
#         # print(f"DEBUG: Using Key: {LLAMA_API_KEY[:5]}... for URL: {url}")
        
#         response = requests.post(url, headers=headers, json=payload, timeout=15)
        
#         if response.status_code != 200:
#             print(f"⚠️ API Error {response.status_code}: {response.text}")
#             raise Exception("API Failed")
            
#         content = response.json()['choices'][0]['message']['content']
#         return clean_json_string(content)
        
#     except Exception as e:
#         print(f"❌ AI Service Error: {e}. Using Random Mock Data.")
#         return generate_mock_response(prompt)

# def clean_json_string(text):
#     return re.sub(r'^```json\s*|\s*```$', '', text.strip(), flags=re.MULTILINE)

# # --- BETTER MOCK DATA ---
# def generate_mock_response(prompt):
#     """Returns random mock data so the app feels alive even offline."""
    
#     if "flashcards" in prompt:
#         return json.dumps({ "flashcards": [
#             {"front": "What is the Virtual DOM?", "back": "A lightweight copy of the real DOM..."},
#             {"front": "Explain Closure.", "back": "A function bundled with its lexical environment..."},
#             {"front": "What is ACID?", "back": "Atomicity, Consistency, Isolation, Durability."}
#         ]})
        
#     if "roadmap" in prompt:
#         return json.dumps({ "roadmap": [
#             {"week": "Week 1", "topic": "DSA Basics", "details": "Arrays and Strings"},
#             {"week": "Week 2", "topic": "System Design", "details": "Load Balancers and Caching"}
#         ]})

#     if "gap analysis" in prompt:
#         return json.dumps({ "gaps": [
#             {"skill": "System Design", "recommendation": "Study scalability patterns."},
#             {"skill": "Cloud Services", "recommendation": "Get certified in AWS or Azure."}
#         ]})

#     if "career" in prompt:
#          return json.dumps({ 
#              "steps": ["Master System Design", "Contribute to Open Source", "Lead a Team"],
#              "salary_insight": "$120k - $180k range for Senior roles."
#          })

#     # Random Interview Questions
#     questions = [
#         "Explain the difference between SQL and NoSQL databases.",
#         "How do you handle race conditions in a distributed system?",
#         "Describe a time you failed and how you handled it.",
#         "What is your process for code reviews?",
#         "Explain the concept of microservices architecture.",
#         "How does garbage collection work in your preferred language?",
#         "What are the pros and cons of serverless architecture?"
#     ]
    
#     if "interview question" in prompt.lower():
#         q = random.choice(questions)
#         return json.dumps({ "question": q, "type": "technical" })
    
#     # Analysis
#     return json.dumps({
#         "score": random.randint(60, 95),
#         "difficulty_adjustment": random.choice([-1, 0, 1]),
#         "feedback": "Good attempt. Try to include more specific examples in your answer to demonstrate depth."
#     })










import os
import requests
import json
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "llama-3.1-8b-instant")

def call_groq(prompt, system_message="You are an expert AI Interview Coach."):
    """
    Calls the Groq API using the Llama 3.1 model.
    Enforces JSON mode to ensure the app never crashes on parsing.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Groq API Error: {e}")
        # Return an error JSON so the frontend handles it gracefully
        return json.dumps({
            "error": "AI Service Unavailable",
            "details": str(e),
            "fallback": True
        })

# Alias for compatibility
def generate_ai_response(prompt, system_message="You are a helpful assistant."):
    return call_groq(prompt, system_message)