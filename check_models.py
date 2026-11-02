import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Models available to your key:")
names = []
for m in client.models.list():
    name = m.name.replace("models/", "")
    if "flash" in name:
        names.append(name)
        print(" -", name)

print("\nTesting the first 5 flash models:")
for name in names[:5]:
    try:
        r = client.models.generate_content(model=name, contents="Say hi")
        print("WORKS:", name, "->", r.text.strip()[:40])
    except Exception as e:
        print("FAILED:", name, "->", str(e)[:100])