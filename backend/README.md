# 🌱 Earthworm (ಅರ್ಥ್‌ವರ್ಮ್) — Satellite Crop Advisory Platform

[![Vercel Deployment Ready](https://img.shields.io/badge/Vercel-Deployment%20Ready-black?style=flat&logo=vercel)](https://vercel.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Earthworm** is an explainable, satellite-based early warning and agronomic advisory platform tailored for smallholder farmers, piloted in **Mandya district, Karnataka, India** with pan-India agricultural support.

It combines **Copernicus Sentinel-2** vegetation reflectance observations, **Open-Meteo** agrometeorological insights, and contextual soil data to alert farmers to crop stress before visible leaf symptoms expand.

---

## ✨ Key Features

- **📡 Space Agromet Observations:** Sentinel-2 Level-2A cloud-free satellite imagery with registered farm parcel overlays.
- **📈 20-Day NDVI Trend Visualizer:** 5-point time-series history bars (04 Feb, 09 Feb, 14 Feb, 19 Feb, 24 Feb) with seasonal benchmark comparison (0.70).
- **💡 3-Stage Explainable Advisory Framework:**
  1. *What did we notice? (ಗಮನಿಸಿದ್ದು)* — Multi-spectral canopy index anomaly.
  2. *What could it mean? (ಅರ್ಥವೇನು)* — Root-zone moisture or subsoil percolation changes.
  3. *What should I do next? (ಮುಂದೇನು)* — Practical low-cost ground checks before applying water or inputs.
- **🗣️ Multilingual & Voice Narration:** Native Web Speech API reading advisories aloud in **Kannada (`kn`)**, **Hindi (`hi`)**, and **English (`en`)**.
- **📱 Feature Phone SMS Simulation:** 1-tap copyable SMS preview designed for rural delivery via Kisan Call Centres.
- **🏛️ National Kisan Helpline:** One-touch direct dialing to `1800-180-1551`.

---

## 🚀 Deploy to Vercel (1-Click Ready)

Earthworm is pre-configured with `vercel.json` and `api/index.py` serverless routing for zero-friction Vercel deployment:

1. Import your GitHub repository (`gcemHacks5.0`) into [Vercel](https://vercel.com/new).
2. **Framework Preset:** Select **Other**.
3. **Root Directory:** Keep `./` (leave default).
4. **Environment Variables (Optional):**
   - `SUPABASE_URL`: Your Supabase project URL (e.g. `https://xyz.supabase.co`)
   - `SUPABASE_SECRET_KEY`: Your Supabase service role key
   *(The platform operates automatically in offline demo mode if these are omitted).*
5. Click **Deploy**!

Vercel will automatically:
- Serve the responsive UI at `https://<your-project>.vercel.app/`
- Execute the FastAPI serverless backend at `https://<your-project>.vercel.app/api/...`

---

## 💻 Running Locally

### 1. Prerequisites
- Python 3.10+

### 2. Setup Virtual Environment
```powershell
cd c:\Earthworm\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Start the Server
```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- **Web Application:** [http://127.0.0.1:8000/app/code.html](http://127.0.0.1:8000/app/code.html) or [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Swagger Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Health:** [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

### 4. Run Automated Tests (20 Tests Passing)
```powershell
pytest -v
```

---

## 🔒 Security & Data Integrity

- API keys and database credentials are kept exclusively server-side in `.env` (strictly ignored by Git).
- No destructive SQL or unverified disease claims are made without physical ground truth.
