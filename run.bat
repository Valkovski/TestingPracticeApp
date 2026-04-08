@echo off
setlocal

if not exist .venv\Scripts\python.exe (
  py -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python database\reset_db.py
python app.py

