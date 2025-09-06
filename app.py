import streamlit as st
import pdfplumber
from docx import Document
import pandas as pd
import re

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="centered")
st.title("📄 Resume Analyzer App")
st.write("Upload a resume (PDF or DOCX) to extract key information.")

# ----------------- File Upload -----------------
uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

# ----------------- Helper Functions -----------------
def extract_text(file):
    """Extract text from PDF or DOCX"""
    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    elif file.name.endswith(".docx"):
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    else:
        return ""

def extract_contact_info(text):
    """Extract name, email, phone from text"""
    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\+?\d[\d -]{8,12}\d', text)
    # Simple heuristic: first non-empty line as name
    name = next((line.strip() for line in text.splitlines() if line.strip()), "")
    return name, email[0] if email else "", phone[0] if phone else ""

def extract_skills(text):
    """Extract skills from text"""
    # Add more skills as needed
    skills_list = [
        "Python", "Java", "C++", "C#", "SQL", "JavaScript",
        "Machine Learning", "AI", "Deep Learning", "Data Analysis",
        "TensorFlow", "PyTorch", "Pandas", "Numpy", "React"
    ]
    skills_found = [skill for skill in skills_list if skill.lower() in text.lower()]
    return skills_found

# ----------------- Processing -----------------
if uploaded_file:
    text = extract_text(uploaded_file)

    st.subheader("🔹 Extracted Information")

    # Contact Info
    name, email, phone = extract_contact_info(text)
    st.write(f"**Name:** {name}")
    st.write(f"**Email:** {email}")
    st.write(f"**Phone:** {phone}")

    # Skills
    skills = extract_skills(text)
    st.write("**Skills:**")
    if skills:
        st.write(skills)
        # Skill chart
        skill_counts = pd.Series(skills).value_counts()
        st.bar_chart(skill_counts)
    else:
        st.write("No predefined skills found.")

    # Optional: Resume Text Preview
    with st.expander("Preview Resume Text"):
        st.text(text)
