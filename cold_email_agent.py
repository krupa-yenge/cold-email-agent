import os
import sys
import csv
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ---------- EDIT THESE 2 LINES (your signature) ----------
SENDER_NAME = "Your Name"
SENDER_COMPANY = "Parivestra Ventures"
# ----------------------------------------------------------

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not found. Check your .env file.")
    sys.exit(1)

# 15-second timeout per call (value is in milliseconds)
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=15000),
)

# Fastest model first, backup second
MODELS = ["gemini-flash-lite-latest", "gemini-flash-latest"]
LOG_FILE = "email_log.csv"


def build_prompt(name, company, offer):
    return f"""ROLE: You are a B2B sales assistant who writes short, personalised cold emails.
TASK: Write one cold email to {name} at {company}, offering: {offer}.
SENDER: {SENDER_NAME} from {SENDER_COMPANY}.
RULES:
- Maximum 120 words.
- Friendly, professional tone. No hype, no false claims.
- Do not invent facts about the company.
- End with one clear call to action (a short call).
- Sign off with exactly: {SENDER_NAME}, {SENDER_COMPANY}
- Plain text only. No asterisks, no markdown, no placeholders in square brackets.
OUTPUT: Return only the subject line, then the email body."""


def ask_ai(prompt):
    for round_no in range(1, 3):  # two rounds over the models
        for model in MODELS:
            print(f"Asking {model} (round {round_no})...", flush=True)
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                if response.text:
                    return response.text.strip(), model
            except Exception as e:
                print(f"   Failed: {str(e)[:100]}", flush=True)
                time.sleep(2)
    return None, None


def save_log(name, company, offer, model, seconds, email):
    new_file = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["time", "lead", "company", "offer", "model", "seconds", "email"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name, company, offer, model, round(seconds, 1), email,
        ])


def ask_input(label, default):
    value = input(f"{label} [{default}]: ").strip()
    return value if value else default


if __name__ == "__main__":
    print("=== Cold Email Agent ===")
    print("Press Enter to use the sample value shown in [brackets].\n")

    name = ask_input("Lead name", "Priya Sharma")
    company = ask_input("Lead company", "GreenLeaf Organic Store")
    offer = ask_input(
        "Our offer",
        "an AI agent that answers customer WhatsApp inquiries automatically",
    )

    start = time.time()
    email, model_used = ask_ai(build_prompt(name, company, offer))
    seconds = time.time() - start

    if email:
        print("\n===== GENERATED EMAIL =====\n")
        print(email)
        print(f"\n(Model: {model_used} | Time: {seconds:.1f}s)")
        save_log(name, company, offer, model_used, seconds, email)
        print(f"Saved to {LOG_FILE}")
    else:
        print("\nAll attempts failed. Servers may be busy. Wait a few minutes and run again.")