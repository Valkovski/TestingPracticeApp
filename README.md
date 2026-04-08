# TestingPracticeApp

## Description

A modular, server-rendered e-commerce web app built as a **QA training application** with **intentional hidden bugs**.

Students should **test** the system (manual + automated), not fix it.

## Tech stack

- Flask
- SQLite (raw SQL only; no ORM)
- pytest
- Playwright (optional)

## Setup

```powershell
python -m pip install -r requirements.txt
python database\reset_db.py
python app.py
```

## Run (Windows)

```bat
run.bat
```

## Notes

- The app contains intentional bugs used for teaching testing.
- Students should test behaviors and report defects, not change code.
