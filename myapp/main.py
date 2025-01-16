from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
import pandas as pd
from io import StringIO

# Initialize FastAPI
app = FastAPI()

# Serve static files (for frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Replace this with your API key from Google Cloud
API_KEY = ""
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/upload/")
async def upload_csv(file: UploadFile):
    # Step 1: Read CSV into a DataFrame
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode('utf-8')))
    
    # Step 2: Convert DataFrame to JSON-like format
    data = df.to_dict(orient="records")

    # Updated prompt to request plain text output
    prompt = f"""
    You are an assistant tasked with calculating late fines for a library system.
    The rules for calculating fines are:
    - If a book is returned more than 5 days after borrowing, charge 50 per late day.
    - If the person is not a member, add an additional fine of 10.

    Here is the data in JSON format:
    {data}

    For each user, calculate the fine (if any) and provide a report in a readable format like:
    - Name: [User Name]
    - Membership: [Member/Non-Member]
    - Fine: $[Amount]

    Only include users with fines in the report. Please return the results as plain text, without any code or Python syntax.
    """
    
    # Step 4: Call the Google Generative AI model
    try:
        response = model.generate_content(prompt)
        report = response.text.strip()  # Remove any leading/trailing whitespace
        return {"report": report}
    except Exception as e:
        return {"error": "Failed to generate report", "details": str(e)}

