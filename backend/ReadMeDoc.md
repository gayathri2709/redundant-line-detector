ReadMeDoc
1. Created the Repo calles RedundantLinesExtracter
2. Navigated to that Repo
cd Desktop/RedundantLinesExtracter
3. Created the virtual environment to not effect this Projects package to all global Projects
python3 -m venv venv
4. To activate the virtual environment
source venv/bin/activate
5. created backend repo to add files related to backend and navigated into that
cd backend
6. Added the main API
main.py
7. Packages related to that API is being written in requirements.txt
8. To install all the packages used pip install requirements.txt
9. All packages are installed and after we did uvicorn main:app --reload
10. App is up and running
11. To check and test the APP using the following swagger URL http://127.0.0.1:8000/docs
12. Libraries used
    12.1. Fast API - FastAPI makes it extremely easy to expose Python logic (like your redundant line detection) as a web API.It is a web framework like Flask and django
    12.2. Uvicorn is the server that actually runs your FastAPI app.it ASGI(Asynchronous server Gateway Interface) - this uvicorn listens to HTTP requests and forward then to this Fast API
    In Flask or Django, you sometimes start by directly running python app.py — but that’s mostly for dev only.

    FastAPI doesn’t have a built-in server like Flask’s simple app.run() — instead, it’s designed to run on production-ready servers like uvicorn or hypercorn.
    12.3. pdfplumber - This is the library used to read pdf files
    12.4. docx - This is the library used to read the doc files
    12.5. Pandas - This is the library used to read csv files
    12.6. chardet - This is used to check whether the file uploaded is UTF-8 encoded for code files
    12.7. python-multipart - This is basically used to get file format similar to how the front end is sending. Basically metadata nad the actual file with speerators.

Wanted to Run command
go to Desktop C:users/gayayjeri-kancheti/Desktop
source venv/bin/activate - to enter the vm
cd RedundantLinesExtracter
cd backend
uvicorn main:app --reload
if there is already something running get that by this command
lsof -i :8000
to kill each process kill -9 pid
after killing run uvicorn main:app --reload


