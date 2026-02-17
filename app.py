import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def input_pdf_text(file_path_or_buffer):
    reader = pdf.PdfReader(file_path_or_buffer)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += page.extract_text()
    return text

def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(input_prompt)
    return response.text

input_prompt_template = """
Act as a strict and efficient Technical Recruiter or ATS (Applicant Tracking System).
Your task is to evaluate the candidate's resume against the provided Job Description.

Resume Text: {text}
Job Description: {jd}

Extract the following information and output strictly in JSON format:
1. "Name": Candidate's full name.
2. "Email": Candidate's email.
3. "MatchScore": Percentage (0-100).
4. "MissingKeywords": List of missing skills.
5. "Summary": A string containing exactly 3 bullet points starting with '•'. Separate them with a newline character. Example: "• Strong Python skills\n• Missing AWS experience\n• Good education background"

Extract the following information and output strictly in JSON format:
{{"Name": "Candidate's full name", "Email": "Candidate's email", "MatchScore": "Percentage (0-100)", "MissingKeywords": ["list", "of", "missing", "skills"], "Summary": "Brief justification"}}
"""

st.set_page_config(page_title="TalentScout", page_icon="🎯", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 42px;
        font-weight: 700;
        color: #1a202c;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-header {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 18px;
        color: #718096;
        text-align: center;
        margin-bottom: 40px;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 45px;
        font-weight: 600;
    }
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎯 TalentScout</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Intelligent ATS & Candidate Screening Dashboard</div>', unsafe_allow_html=True)

if 'results' not in st.session_state:
    st.session_state.results = []

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📋 Job Configuration")
    jd = st.text_area("Job Description", height=250, placeholder="Paste the Job Description here...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📂 Candidate Pipeline")
    
    tab_upload, tab_demo = st.tabs(["📤 Upload Files", "🎲 Demo Mode"])
    
    with tab_upload:
        uploaded_files = st.file_uploader("Upload Resumes (PDF)", type="pdf", accept_multiple_files=True, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("✨ Screen Uploaded Candidates", type="primary")
    
    with tab_demo:
        st.info("ℹ️ Loads resumes from local 'demo_data' folder.")
        demo_btn = st.button("🚀 Load & Screen Demo Candidates")
        
    st.markdown('</div>', unsafe_allow_html=True)

if analyze_btn and uploaded_files:
    if not jd:
        st.warning("⚠️ Please provide a Job Description.")
    else:
        results = []
        progress_text = "Screening candidates..."
        my_bar = st.progress(0, text=progress_text)
        
        for i, file in enumerate(uploaded_files):
            try:
                text = input_pdf_text(file)
                final_prompt = input_prompt_template.format(text=text, jd=jd)
                response = get_gemini_response(final_prompt)
                
                clean_response = response.strip()
                if clean_response.startswith("```json"):
                    clean_response = clean_response.split("```json")[1].split("```")[0]
                
                data = json.loads(clean_response)
                data["Filename"] = file.name
                results.append(data)
                
            except Exception as e:
                st.error(f"Error analyzing {file.name}: {str(e)}")
            
            my_bar.progress((i + 1) / len(uploaded_files), text=f"Analyzed {file.name}")
            
        my_bar.empty()
        st.session_state.results = results
        st.success("Batch Analysis Complete!")

if demo_btn:
    if not jd:
        st.warning("⚠️ Please provide a Job Description first.")
    else:
        demo_folder_path = "demo_data"
        
        if not os.path.exists(demo_folder_path):
            st.error(f"❌ Folder '{demo_folder_path}' not found. Please create it and add PDF files.")
        else:
            demo_files = [f for f in os.listdir(demo_folder_path) if f.endswith('.pdf')]
            
            if not demo_files:
                st.error(f"❌ No PDF files found in '{demo_folder_path}'.")
            else:
                results = []
                progress_text = "Processing Demo Candidates..."
                my_bar = st.progress(0, text=progress_text)
                
                for i, filename in enumerate(demo_files):
                    file_path = os.path.join(demo_folder_path, filename)
                    try:
                        text = input_pdf_text(file_path)
                        final_prompt = input_prompt_template.format(text=text, jd=jd)
                        response = get_gemini_response(final_prompt)
                        
                        clean_response = response.strip()
                        if clean_response.startswith("```json"):
                            clean_response = clean_response.split("```json")[1].split("```")[0]
                        
                        data = json.loads(clean_response)
                        data["Filename"] = filename
                        results.append(data)
                        
                    except Exception as e:
                        st.error(f"Error analyzing {filename}: {str(e)}")
                    
                    my_bar.progress((i + 1) / len(demo_files), text=f"Analyzed {filename}")
                
                my_bar.empty()
                st.session_state.results = results
                st.success("Demo Batch Analyzed Successfully!")

if st.session_state.results:
    st.markdown("---")
    st.subheader("🏆 Candidate Leaderboard")
    
    df = pd.DataFrame(st.session_state.results)
    
    if "MatchScore" in df.columns:
        df["MatchScore"] = pd.to_numeric(df["MatchScore"], errors='coerce').fillna(0)
        df.loc[df["MatchScore"] <= 1, "MatchScore"] = df["MatchScore"] * 100
        df["MatchScore"] = df["MatchScore"].astype(int)
        df = df.sort_values(by="MatchScore", ascending=False)
    
    st.dataframe(
        df,
        column_config={
            "Name": st.column_config.TextColumn("Candidate Name", width="medium"),
            "MatchScore": st.column_config.ProgressColumn(
                "Match Score",
                format="%d%%",
                min_value=0,
                max_value=100,
                width="small"
            ),
            "Email": st.column_config.LinkColumn("Contact"),
            "MissingKeywords": st.column_config.ListColumn("Skill Gaps"),
            "Summary": st.column_config.TextColumn("AI Summary", width="large"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Report (CSV)",
        data=csv,
        file_name="talentscout_report.csv",
        mime="text/csv"
    )