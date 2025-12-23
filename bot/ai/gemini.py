import requests
import os
import re
import json
from dotenv import load_dotenv
from storage.db import cur, conn

load_dotenv()

def get_api_key():
    """Retrieve OpenRouter API key from environment"""
    return os.getenv("OPENROUTER_API_KEY", "")

def generate(prompt: str, guild_id: str = None):
    try:
        api_key = get_api_key()
        if not api_key:
            print(f"❌ OpenRouter API Error: No API key found in environment")
            return ""
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo/threadmind",
            "X-Title": "ThreadMind Discord Bot"
        }
        
        data = {
            "model": "google/gemma-3-27b-it",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                               headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            text = result["choices"][0]["message"]["content"]
            text = re.sub(r'^```(?:json)?\n', '', text)
            text = re.sub(r'\n```$', '', text)
            return text
        else:
            print(f"❌ OpenRouter API Error: {response.status_code} - {response.text}")
            return ""
            
    except Exception as e:
        print(f"❌ OpenRouter API Error: {e}")
        return ""
