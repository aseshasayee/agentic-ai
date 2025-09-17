import google.generativeai as genai
import dotenv
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
dotenv.load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

tools = [
    {
        "function_declarations": [
            {
                "name": "fixed__deposit",
                "description": "Calculate maturity amount for a fixed deposit",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "principal": {"type": "number"},
                        "time": {"type": "number", "description": "time period in years"}
                    },
                    "required": ["principal", "time"]
                }
            }
        ]
    }
]

def fixed__deposit(principal, time):
    rate = 7.0
    amount = principal * (1 + (rate / 100) * time)
    return amount

prompt = """
You are an expert financial advisor.
Give clear, simple investment advice for a 20-year-old.
If the user asks about fixed deposit, call the fixed__deposit function.
"""

user_question = "I want to invest 10000 rupees. Where to invest? Also, if I choose FD for 5 years, how much will I get?"

model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content(
    contents=[
        {"role": "user", "parts": [{"text": prompt}]},
        {"role": "user", "parts": [{"text": user_question}]}
    ],
    tools=tools
)

fn_call = None
for part in response.candidates[0].content.parts:
    if hasattr(part, "function_call") and part.function_call:
        fn_call = part.function_call
        break

if fn_call:
    fn_name = fn_call.name
    args = fn_call.args
    if fn_name == "fixed__deposit":
        result = fixed__deposit(args["principal"], args["time"])
        # Send tool result back to Gemini for a final explanation (wrap result in a dict)
        follow_up = model.generate_content(
            contents=[
                {"role": "user", "parts": [{"text": prompt}]},
                {"role": "user", "parts": [{"text": user_question}]},
                {"role": "model", "parts": [{"function_call": fn_call}]},
                {"role": "function", "parts": [{"function_response": {"name": fn_name, "response": {"maturity_amount": result}}}]}
            ]
        )
        print(follow_up.text)
else:
    print(response.text)