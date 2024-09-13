import streamlit as st
import PyPDF2
import io
import base64

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

import re
from datetime import datetime

def parse_linkedin_text(text):
    sections = {
        'name': '',
        'title': '',
        'location': '',
        'about': '',
        'experience': [],
        'education': [],
        'skills': [],
        'languages': [],
        'certifications': [],
        'volunteer_experience': [],
        'accomplishments': []
    }
    
    lines = text.split('\n')
    current_section = None
    current_item = {}
    
    date_pattern = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}\s-\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}|Present'
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        if 'Experience' in line:
            current_section = 'experience'
            continue
        elif 'Education' in line:
            current_section = 'education'
            continue
        elif 'Skills' in line:
            current_section = 'skills'
            continue
        elif 'Languages' in line:
            current_section = 'languages'
            continue
        elif 'Certifications' in line:
            current_section = 'certifications'
            continue
        elif 'Volunteer Experience' in line:
            current_section = 'volunteer_experience'
            continue
        elif 'Accomplishments' in line:
            current_section = 'accomplishments'
            continue
        
        if current_section == 'experience':
            if re.match(date_pattern, line):
                if current_item:
                    sections['experience'].append(current_item)
                current_item = {'date': line}
            elif 'current_item' in locals():
                if 'company' not in current_item:
                    current_item['company'] = line
                elif 'title' not in current_item:
                    current_item['title'] = line
                else:
                    current_item['description'] = current_item.get('description', '') + line + ' '
        
        elif current_section == 'education':
            if re.match(date_pattern, line):
                if current_item:
                    sections['education'].append(current_item)
                current_item = {'date': line}
            elif 'current_item' in locals():
                if 'school' not in current_item:
                    current_item['school'] = line
                elif 'degree' not in current_item:
                    current_item['degree'] = line
                else:
                    current_item['description'] = current_item.get('description', '') + line + ' '
        
        elif current_section == 'skills':
            sections['skills'].append(line)
        
        elif current_section == 'languages':
            sections['languages'].append(line)
        
        elif current_section == 'certifications':
            sections['certifications'].append(line)
        
        elif current_section == 'volunteer_experience':
            sections['volunteer_experience'].append(line)
        
        elif current_section == 'accomplishments':
            sections['accomplishments'].append(line)
        
        elif not current_section:
            if not sections['name']:
                sections['name'] = line
            elif not sections['title']:
                sections['title'] = line
            elif not sections['location']:
                sections['location'] = line
            elif not sections['about']:
                sections['about'] += line + ' '
    
    # Append the last item if exists
    if current_section == 'experience' and current_item:
        sections['experience'].append(current_item)
    elif current_section == 'education' and current_item:
        sections['education'].append(current_item)
    
    return sections

def generate_html_resume(parsed_data):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{name} - Resume</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; background-color: #fff; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }}
            .section {{ margin-bottom: 20px; }}
            ul {{ padding-left: 20px; }}
            .job-title {{ font-weight: bold; }}
            .job-company {{ font-style: italic; }}
            .job-date {{ color: #7f8c8d; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{name}</h1>
            <p><strong>{title}</strong></p>
            <p>{location}</p>
            <div class="section">
                <h2>About</h2>
                <p>{about}</p>
            </div>
            <div class="section">
                <h2>Experience</h2>
                {experience}
            </div>
            <div class="section">
                <h2>Education</h2>
                {education}
            </div>
            <div class="section">
                <h2>Skills</h2>
                <ul>
                    {skills}
                </ul>
            </div>
            <div class="section">
                <h2>Languages</h2>
                <ul>
                    {languages}
                </ul>
            </div>
            <div class="section">
                <h2>Certifications</h2>
                <ul>
                    {certifications}
                </ul>
            </div>
            <div class="section">
                <h2>Volunteer Experience</h2>
                <ul>
                    {volunteer_experience}
                </ul>
            </div>
            <div class="section">
                <h2>Accomplishments</h2>
                <ul>
                    {accomplishments}
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    
    experience_html = ""
    for exp in parsed_data['experience']:
        experience_html += f"""
        <div class="job">
            <p class="job-title">{exp.get('title', '')}</p>
            <p class="job-company">{exp.get('company', '')}</p>
            <p class="job-date">{exp.get('date', '')}</p>
            <p>{exp.get('description', '')}</p>
        </div>
        """
    
    education_html = ""
    for edu in parsed_data['education']:
        education_html += f"""
        <div class="education">
            <p><strong>{edu.get('school', '')}</strong></p>
            <p>{edu.get('degree', '')}</p>
            <p>{edu.get('date', '')}</p>
            <p>{edu.get('description', '')}</p>
        </div>
        """
    
    skills_html = "\n".join(f"<li>{skill}</li>" for skill in parsed_data['skills'])
    languages_html = "\n".join(f"<li>{lang}</li>" for lang in parsed_data['languages'])
    certifications_html = "\n".join(f"<li>{cert}</li>" for cert in parsed_data['certifications'])
    volunteer_html = "\n".join(f"<li>{vol}</li>" for vol in parsed_data['volunteer_experience'])
    accomplishments_html = "\n".join(f"<li>{acc}</li>" for acc in parsed_data['accomplishments'])
    
    return html_template.format(
        name=parsed_data['name'],
        title=parsed_data['title'],
        location=parsed_data['location'],
        about=parsed_data['about'],
        experience=experience_html,
        education=education_html,
        skills=skills_html,
        languages=languages_html,
        certifications=certifications_html,
        volunteer_experience=volunteer_html,
        accomplishments=accomplishments_html
    )

st.set_page_config(page_title="LinkedIn PDF to HTML Resume Converter")

st.title("LinkedIn PDF to HTML Resume Converter")

api_key = st.text_input("OpenAI API Key :")
uploaded_file = st.file_uploader("Upload your LinkedIn PDF", type="pdf")

if uploaded_file is not None and api_key:
    if st.button("Generate HTML Resume"):
        text = extract_text_from_pdf(uploaded_file)
        parsed_data = parse_linkedin_text(text)
        html_resume = generate_html_resume(parsed_data)
        
        # Create a download link for the HTML file
        b64 = base64.b64encode(html_resume.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="resume.html">Download HTML Resume</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        # Display a preview of the resume
        st.subheader("Resume Preview:")
        st.components.v1.html(html_resume, height=600, scrolling=True)