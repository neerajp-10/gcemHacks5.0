# Earthworm Advisory Backend

Satellite-based early-warning and crop advisory backend for smallholder paddy farmers in Mandya district, Karnataka, India.

## Phase 1 Status: Minimal Runnable Backend
- FastAPI service with `/api/health` and `/` endpoints.
- Structured response formats and safe configuration loading without external credentials.
- Zero external database or service requirements for demo mode.

---

## 1. Setup & Installation

### Prerequisites
- Python 3.10+ (Tested with Python 3.12.14)

### Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

*(Or use the direct python path if python alias is not configured)*:
```powershell
& "C:\Users\Balaji\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m venv .venv
```

### Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 2. Running the Development Server

From the `backend/` directory:

```powershell
.\.venv\Scripts\uvicorn.exe app.main:app --reload --host 127.0.0.1 --port 8000
```

Or when the virtual environment is activated:
```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Accessing Endpoints
- **Interactive Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Service Health Check:** [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)
- **Root Info:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 3. Running Tests

From the `backend/` directory:

```powershell
.\.venv\Scripts\pytest.exe -v
```

---

## 4. Configuration & Supabase Setup

Default settings in `app/config.py` allow immediate execution without any environment variables (running in demo mode).

### Connecting Supabase (Optional)

1. Create a `backend/.env` file from the example template:
   ```powershell
   cd c:\Earthworm\backend
   copy .env.example .env
   ```

2. Open `backend/.env` and supply your Supabase project credentials:
   ```env
   SUPABASE_URL=https://<your-project-ref>.supabase.co
   SUPABASE_SECRET_KEY=<your-service-role-or-secret-key>
   ```

> **Security Note:** `backend/.env` is included in `.gitignore` and is never committed to version control. The client runs backend-only; never expose service-role keys in frontend code.

3. Verify connection without mutating database data:
   - Visit [http://127.0.0.1:8000/api/health/db](http://127.0.0.1:8000/api/health/db)
   - Or run `Invoke-RestMethod http://127.0.0.1:8000/api/health/db`
