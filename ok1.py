import streamlit as st
import openai
from pdfminer.high_level import extract_text
import time

# Step 1: Ask for OpenAI API key at start
st.title("LinkedIn PDF to HTML Resume Generator")
openai_api_key = st.text_input("Enter your OpenAI API key", type="password")

# Step 2: Prompt for PDF Upload
uploaded_file = st.file_uploader("Upload your LinkedIn PDF resume", type="pdf")

if openai_api_key and uploaded_file is not None:
    openai.api_key = openai_api_key

    # Step 3: Extract text from PDF using pdfminer
    def extract_text_from_pdf(pdf_file):
        return extract_text(pdf_file)

    raw_text = extract_text_from_pdf(uploaded_file)

    # Step 4: Use OpenAI API to clean and format the text into an HTML resume
    if st.button("Generate HTML Resume"):
        st.write("Processing the text with OpenAI...")

        try:
            # New API call for Chat-based completion
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a resume formatter."},
                    {"role": "user", "content": f"Format this LinkedIn resume text into a professional HTML resume:\n\n{raw_text}"}
                ]
            )

            # Get formatted HTML from the API response
            formatted_resume = response['choices'][0]['message']['content']

            # Step 5: Output HTML File for download
            st.download_button("Download HTML Resume", data=formatted_resume, file_name="resume.html", mime="text/html")
        
        except openai.error.RateLimitError as e:
            st.error("Rate limit exceeded. Please try again later.")
            st.write("Error details:", e)
        except openai.error.OpenAIError as e:
            st.error("An error occurred with the OpenAI API.")
            st.write("Error details:", e)
