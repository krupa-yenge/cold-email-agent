import time
from cold_email_agent import build_prompt, ask_ai, save_log

LEADS = [
    ("Priya Sharma", "GreenLeaf Organic Store", "an AI agent that answers customer WhatsApp inquiries automatically"),
    ("Rahul Mehta", "FitZone Gym", "an AI agent that books gym trial appointments automatically"),
    ("Anita Rao", "Bright Smile Dental Clinic", "an AI agent that handles appointment booking and reminders"),
    ("Karan Singh", "UrbanWear Fashion", "an AI agent that recommends products to online shoppers"),
    ("Neha Gupta", "QuickBooks Accounting Services", "an AI agent that extracts data from invoices"),
    ("Vikram Patel", "SpiceRoute Restaurant", "an AI agent that answers customer questions on WhatsApp"),
    ("Sunita Joshi", "EduSpark Coaching Centre", "an AI agent that answers student and parent queries"),
    ("Arjun Nair", "BuildRight Constructions", "an AI agent that sorts and prioritises customer inquiries"),
    ("Meera Iyer", "PetCare Plus Clinic", "an AI agent that sends follow-up reminders to customers"),
    ("Sanjay Kumar", "TechNova IT Solutions", "an AI agent that scores and qualifies incoming leads"),
]

ok = 0
times = []

for i, (name, company, offer) in enumerate(LEADS, 1):
    print(f"\n--- Test {i} of {len(LEADS)}: {name}, {company} ---", flush=True)
    start = time.time()
    email, model = ask_ai(build_prompt(name, company, offer))
    seconds = time.time() - start
    if email:
        ok += 1
        times.append(seconds)
        save_log(name, company, offer, model, seconds, email)
        print(f"SUCCESS | {model} | {seconds:.1f}s", flush=True)
    else:
        print(f"FAILED  | {seconds:.1f}s", flush=True)
    time.sleep(2)

print("\n===== SUMMARY =====")
print(f"Successful: {ok} of {len(LEADS)}")
if times:
    print(f"Average time: {sum(times) / len(times):.1f}s")
    print(f"Fastest: {min(times):.1f}s | Slowest: {max(times):.1f}s")