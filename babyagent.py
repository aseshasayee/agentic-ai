import google.generativeai as genai
import dotenv
import os
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')
dotenv.load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

prompt = """
you are a expert financial advisor. you have great knowledge of stock market and crypto market.
you now have to give the best advice for a 20 year old who wants to invest
give me insights of the market in simple languge, and even suggestions and ideas
make it simple and clear but also give good advice
make it short and concise
"""

model = genai.GenerativeModel("gemini-1.5-pro")

user_question = "i want to invest 10000 rupees. where to invest?"

# --- OpenRouter code starts here ---
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")  # Add your OpenRouter API key to .env

openrouter_headers = {
    "Authorization": f"Bearer {openrouter_api_key}",
    "Content-Type": "application/json"
}

openrouter_data = {
    "model": "openai/gpt-3.5-turbo",  # Free model as of Sep 2025
    "messages": [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_question}
    ]
}

openrouter_response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=openrouter_headers,
    json=openrouter_data
)

if openrouter_response.ok:
    print("OpenRouter response:")
    print(openrouter_response.json()["choices"][0]["message"]["content"])
else:
    print("OpenRouter error:", openrouter_response.text)
# --- Google Gemini code (will error if quota exceeded) ---
try:
    response = model.generate_content(f"{prompt}\nUser: {user_question}\nTutor:")
    print("Gemini response:")
    print(response.text)
except Exception as e:
    print("Gemini error:", e)