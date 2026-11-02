import time
import streamlit as st
from cold_email_agent import build_prompt, ask_ai, save_log

st.set_page_config(page_title="Cold Email Agent", page_icon="✉️")

st.title("Cold Email Agent")
st.write("Enter the lead's details and get a personalised cold email in seconds.")

name = st.text_input("Lead name", "Priya Sharma")
company = st.text_input("Lead company", "GreenLeaf Organic Store")
offer = st.text_area(
    "Our offer",
    "an AI agent that answers customer WhatsApp inquiries automatically",
)

if st.button("Generate email"):
    if not name.strip() or not company.strip() or not offer.strip():
        st.warning("Please fill in all three fields.")
    else:
        with st.spinner("Writing your email..."):
            start = time.time()
            email, model = ask_ai(build_prompt(name, company, offer))
            seconds = time.time() - start

        if email:
            st.success(f"Done in {seconds:.1f} seconds (model: {model})")
            st.text_area("Your email (copy it from here)", email, height=300)
            save_log(name, company, offer, model, seconds, email)
            st.caption("Saved to email_log.csv")
        else:
            st.error("All models failed. Google's servers may be busy. Wait a minute and try again.")