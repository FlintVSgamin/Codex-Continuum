# Codex-Continuum
 OCR tool that translates incomplete or damaged Latin transcripts into English while auto filling missing characters and words.

# Getting Started
# Step 1: Start the UI
cd frontend
npm run build
npm run dev

Visit the provided localhost URL (usually http://localhost:5173) and ensure the frontend hits http://localhost:8000/ocr once you have completed step 2.

# Step 2: Run the OCR Service
# In WSL
cd Codex-Continuum-main/backend/ocr_service

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install openai  # for Groq translation

Set the Groq API key:
export GROQAPIKEY="gsk_your_real_key_here"

Run the backend:
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Testing & Coverage
We use pytest with coverage. Run everything from the project root.
Quick run (skip OCR test that needs extra deps)
Windows (PowerShell) – from repo root
.\.venv\Scripts\Activate.ps1            # activate root venv 
python -m pytest --cov=backend --cov-report=term-missing --ignore=tests/backend/test_ocr_service.py
The command above generates a line-by-line coverage report for backend/ and ignores the OCR test file that pulls in heavy PDF/multipart dependencies.
First-time setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r backend\requirements.txt
python -m pip install pytest pytest-cov

If you want to run all tests (including OCR), install the extra packages:
python -m pip install python-multipart pdf2image pillow
Then run:
python -m pytest --cov=backend --cov-report=term-missing

Note: always invoke pytest as python -m pytest so it uses the active virtualenv