import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.8-flash"

for attempt in range(1, 5):  # try up to 4 times
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents="Write one sentence explaining what an AI agent is.",
        )
        print(response.text)
        break  # success, stop retrying
    except Exception as e:
        print(f"Attempt {attempt} failed: {str(e)[:120]}")
        if attempt < 4:
            print("Waiting 15 seconds, then trying again...")
            time.sleep(15)