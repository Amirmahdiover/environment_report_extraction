# Disaster Info Extractor (OpenAI + FastAPI)

This project uses OpenAI's function calling to extract structured disaster information from unstructured text. It also stores chat history in a SQLite database using FastAPI.

---

## 🚀 How to Run the Project

### 1. Create and activate a virtual environment


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


### 2. Run this command in terminal


uvicorn src.app.main:app --reload