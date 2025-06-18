from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import pdfplumber
import docx
import pandas as pd
import chardet

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def extract_text(filePath):
    ext = os.path.splitext(filePath)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(filePath)
    elif ext == '.txt':
        return extract_text_from_txtFile(filePath)
    elif ext == '.docx':
        return extract_text_from_docx(filePath)
    elif ext == '.csv':
        return extract_text_from_csv(filePath)
    elif ext in ['.py', '.java', '.js', '.cpp', '.c', '.cs', '.html', '.xml', '.json','.sql']:
        return extract_text_from_code(filePath)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = " ".join(page.extract_text() for page in pdf.pages)
    return text

def extract_text_from_txtFile(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        return f.read()
    
def extract_text_from_docx(doc_path):
    doc = docx.Document(doc_path)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_text_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df.to_string(index=False)

def extract_text_from_code(code_file_path):
    with open(code_file_path, 'rb') as f:
        raw = f.read()
        encoding = chardet.detect(raw)['encoding']
    return raw.decode(encoding)

def getRedundantLines(text):
    lines = text.split("\n")
    noOfLinesInFile = len(lines)
    indexesToAvoid = []
    redundantLines = dict()
    for i in range(0,noOfLinesInFile):
        if(i not in indexesToAvoid):
            for j in range(i+1,noOfLinesInFile):
                lineCompareFrom = lines[i].strip()
                lineCompareTo = lines[j].strip()
                if(j not in indexesToAvoid and lineCompareFrom == lineCompareTo):
                    if(lineCompareFrom in redundantLines):
                        redundantLines[lineCompareFrom].append(j+1)
                        indexesToAvoid.append(j+1)
                    else:
                        redundantLines[lineCompareFrom] = [i+1,j+1]
                        indexesToAvoid.extend([i+1,j+1])
    return redundantLines

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    file_path = f"temp_{file.filename}"
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    try:
        text = extract_text(file_path)
        redundants = getRedundantLines(text)  
        os.remove(file_path)
        return {"redundant_lines": redundants}
    except Exception as e:
        os.remove(file_path)
        return {"error": str(e)}
    