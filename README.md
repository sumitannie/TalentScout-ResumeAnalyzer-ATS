🎯 TalentScout - AI Resume Screener (Recruiter Assistant)

TalentScout is an intelligent Applicant Tracking System (ATS) designed to automate the initial screening process for recruiters. Unlike standard keyword matchers, it utilizes Google's Gemini 2.5 Flash model to semantically analyze multiple resumes against a job description simultaneously, generating a ranked leaderboard of candidates based on their actual fit.

🚀 Key Features
- Batch Processing: Upload and screen dozens of PDF resumes simultaneously in a single click.

- Semantic AI Analysis: Uses Generative AI to understand context (e.g., understanding that "managing a team" implies "Leadership" even if the keyword isn't present).

- Automated Ranking: Instantly generates a Leaderboard scoring candidates from 0-100% based on the Job Description (JD).

- Demo Mode: Includes a built-in "Demo Mode" that loads local resumes from a demo_data folder for instant testing without manual uploads.

- Structured Data Output: Extracts Name, Email, Missing Keywords, and a Professional Summary into a structured Pandas DataFrame.

- Exportable Reports: Recruiters can download the entire analysis as a .csv file for Excel/Sheets integration.

🛠️ Tech Stack
- Frontend: Streamlit (for the interactive dashboard)

- LLM/AI: Google Gemini API (gemini-2.5-flash for high speed and low latency)

- Data Processing: Pandas (DataFrames & CSV export), PyPDF2 (Text Extraction), json (Parsing)

- Environment: python-dotenv (Security)

📂 Project Structure
```Bash
ai_resume_analyzer/
│
├── app.py                   # Main application script (Streamlit)
├── .env                     # Environment variables (API Key) - NOT pushed to GitHub
├── requirements.txt         # List of dependencies (streamlit, pandas, google-generativeai, etc.)
├── .gitignore               # Files to exclude from Git
├── demo_data/               # Folder containing sample PDF resumes for Demo Mode
├── sampleJobDescription.md  # Text file containing a sample JD for testing
└── README.md                # Project documentation
```
⚙️ Installation & Setup
1. Clone the Repository

```Bash
git clone https://github.com/yourusername/talentscout.git
cd talentscout
```
2. Create a Virtual Environment

```Bash
python -m venv venv
# Windows
venv\Scripts\activate
```
# macOS/Linux
```bash
source venv/bin/activate
```
3. Install Dependencies

```Bash
pip install -r requirements.txt
```
4. Set up Environment Variables
Create a file named .env in the root directory and add your Google API Key:

Code snippet
```Bash
GOOGLE_API_KEY=your_actual_api_key_here
```
Note: You can get a free API key from Google AI Studio.

5. Add Demo Data (Optional)
Ensure you have a few PDF resumes inside the demo_data/ folder if you want to use the "Demo Mode".

6. Run the Application

```Bash
streamlit run app.py
```
💡 How to Use
- Configure the Role: Paste the full Job Description (JD) into the text area on the left panel.

- Choose Input Method:

- Upload: Drag and drop multiple PDF files into the uploader.

- Demo Mode: Click the "Demo Mode" tab and hit "Load & Screen Demo Candidates" to test with local files.

- Analyze: Click the "Screen Candidates" button.

View Results:

- The app will display a Candidate Leaderboard sorted by Match Score.

- Review specific Skill Gaps and AI Summaries for each candidate.

- Export: Click "Download Report (CSV)" to save the screening data.

Screenshots:
```bash
![alt text](<Screenshot (1001).png>)
![alt text](<Screenshot (1005).png>)
![alt text](<Screenshot (1002).png>)
![alt text](<Screenshot (1004).png>)
![alt text](<Screenshot (1003).png>)
```
--------------------------------------------------------------------
🤝 Future Improvements
- OCR Integration: Integrate pytesseract to handle scanned/image-based PDF resumes.

- Email Automation: Add a feature to draft "Interview Invite" or "Rejection" emails based on the score.

- Detailed Analytics: Add charts to visualize the distribution of skills across the candidate pool.