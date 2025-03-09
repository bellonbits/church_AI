# api/index.py - Main serverless function entry point
from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import os
import json
from datetime import datetime

# API Configuration - Use environment variables for sensitive info
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")  # Set this in Vercel Environment Variables
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-70b-8192"

# Create FastAPI app
app = FastAPI(title="Church AI Assistant")

class ChurchAssistant:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        self.system_prompt = """
        You are a Church AI Assistant designed to help young Christians in their spiritual journey.
        Your primary roles are:
        
        1. Help users plan meaningful quiet times with God
        2. Recommend appropriate Christian books for spiritual growth
        3. Assist with Bible studies by providing explanations and context
        4. Answer questions about Christianity using the Bible as your primary reference
        
        Always provide Biblical references when possible. Be encouraging, supportive, and 
        deeply rooted in Christian theology while remaining accessible to young believers.
        Aim to foster a deeper relationship with God rather than just providing information.
        """
        
    def get_response(self, user_message):
        """Send a request to Groq API and get a response"""
        
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        try:
            response = requests.post(GROQ_API_URL, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"Error communicating with the API: {e}"
        except (KeyError, IndexError) as e:
            return f"Error processing the response: {e}"
    
    def suggest_quiet_time_plan(self, duration_minutes=15, focus_area=None):
        """Generate a quiet time plan based on user preferences"""
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        prompt = f"""
        Please create a structured quiet time plan for today ({today}) that takes approximately {duration_minutes} minutes.
        """
        
        if focus_area:
            prompt += f" The focus should be on: {focus_area}."
        
        prompt += """
        Include:
        1. A specific Bible passage to read
        2. Prayer points
        3. Reflection questions
        4. A practical application step
        
        Format this in a clear, step-by-step manner that's easy to follow.
        """
        
        return self.get_response(prompt)
    
    def recommend_books(self, topic=None, spiritual_level="beginner", count=3):
        """Recommend Christian books based on topic and spiritual maturity"""
        
        levels = {
            "beginner": "new to Christianity or early in their faith journey",
            "intermediate": "established in their faith but looking to go deeper",
            "advanced": "mature believers looking for challenging theological content"
        }
        
        level_description = levels.get(spiritual_level.lower(), levels["beginner"])
        
        prompt = f"""
        Please recommend {count} Christian books for someone who is {level_description}.
        """
        
        if topic:
            prompt += f" The focus should be on: {topic}."
        
        prompt += """
        For each book, provide:
        1. Title and author
        2. A brief description (2-3 sentences)
        3. Why it's valuable for spiritual growth
        4. A key concept or takeaway
        """
        
        return self.get_response(prompt)
    
    def bible_study_guide(self, passage):
        """Create a Bible study guide for a specific passage"""
        
        prompt = f"""
        Please create a detailed Bible study guide for the passage: {passage}.
        
        Include:
        1. Historical and cultural context
        2. Key themes and theological concepts
        3. Verse-by-verse explanation
        4. Cross-references to other relevant scriptures
        5. Application questions for personal reflection
        6. How this passage points to Jesus and the gospel
        
        Make this accessible for young Christians while maintaining theological depth.
        """
        
        return self.get_response(prompt)
    
    def answer_question(self, question):
        """Answer a question about Christianity using Biblical references"""
        
        prompt = f"""
        Question about Christianity: {question}
        
        Please provide a thorough answer that:
        1. Addresses the question directly
        2. Provides relevant Bible verses and references
        3. Explains any theological concepts in an accessible way
        4. Offers practical wisdom if applicable
        
        Base your response primarily on Biblical teachings rather than denominational perspectives.
        """
        
        return self.get_response(prompt)

# Create an instance of the Church Assistant
assistant = ChurchAssistant()

# Define the request models using Pydantic
class QuietTimeRequest(BaseModel):
    duration: int = 15
    focus_area: str = None

class BookRequest(BaseModel):
    topic: str = None
    spiritual_level: str = "beginner" 
    count: int = 3

class BibleStudyRequest(BaseModel):
    passage: str

class QuestionRequest(BaseModel):
    question: str

# Define API endpoints for Vercel
@app.get("/api")
async def root():
    return {"message": "Church AI Assistant API is running"}

@app.post("/api/quiet-time")
async def get_quiet_time(request: QuietTimeRequest):
    response = assistant.suggest_quiet_time_plan(request.duration, request.focus_area)
    return {"result": response}

@app.post("/api/recommend-books")
async def get_book_recommendations(request: BookRequest):
    response = assistant.recommend_books(request.topic, request.spiritual_level, request.count)
    return {"result": response}

@app.post("/api/bible-study")
async def get_bible_study(request: BibleStudyRequest):
    response = assistant.bible_study_guide(request.passage)
    return {"result": response}

@app.post("/api/answer-question")
async def answer_christian_question(request: QuestionRequest):
    if not request.question or request.question.strip() == "":
        return {"result": "Please provide a specific question about Christianity."}
    
    try:
        response = assistant.answer_question(request.question)
        return {"result": response}
    except Exception as e:
        # Log the error (Vercel will capture this in logs)
        print(f"Error processing question: {e}")
        return {"result": "I apologize, but there was an issue processing your question. Please try again later.",
                "error": str(e)}
