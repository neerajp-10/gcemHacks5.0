# 🌍 Earthworm | Complete Technical Workflow, Architecture & Implementation Guide

> **Satellite-Powered Early-Warning and Explainable Crop Advisory for Smallholder Farmers**  
> *Targeted at Smallholder Paddy Farmers in Mandya, Karnataka & Pan-India Demo Parcels*

---

## 📋 Table of Contents
1. [Project Overview & Core Philosophy](#1-project-overview--core-philosophy)
2. [End-to-End System Workflow](#2-end-to-end-system-workflow)
3. [Libraries & Technologies Used](#3-libraries--technologies-used)
   - [Backend Python Dependencies](#backend-python-dependencies)
   - [Frontend Libraries & Web APIs](#frontend-libraries--web-apis)
4. [Detailed Python Script Documentation](#4-detailed-python-script-documentation)
   - [Entrypoints & Core Configuration](#entrypoints--core-configuration)
   - [Database & Storage Layer](#database--storage-layer)
   - [Domain Data Schemas (Pydantic)](#domain-data-schemas-pydantic)
   - [API Route Handlers (FastAPI)](#api-route-handlers-fastapi)
   - [Demonstration Data & Agronomic Fixtures](#demonstration-data--agronomic-fixtures)
   - [Automated Test Suite (Pytest)](#automated-test-suite-pytest)
5. [In-Depth Supabase Integration Architecture](#5-in-depth-supabase-integration-architecture)
   - [Design Philosophy: Non-Blocking Graceful Fallback](#design-philosophy-non-blocking-graceful-fallback)
   - [Safe Connection Verification (Zero-Leakage Probing)](#safe-connection-verification-zero-leakage-probing)
   - [Database Schema (PostgreSQL DDL)](#database-schema-postgresql-ddl)
   - [Manual Setup & Credential Management](#manual-setup--credential-management)
6. [Deployment & Execution Instructions](#6-deployment--execution-instructions)

---

## 1. Project Overview & Core Philosophy

**Earthworm** addresses the critical "last-mile" barrier between spaceborne Earth observation (Copernicus Sentinel-2 multispectral imagery, Open-Meteo regional agro-meteorology) and smallholder farmers in rural India.

Most commercial agri-tech platforms fail smallholders due to three chronic barriers:
1. **Bandwidth Poverty**: Heavy modern web apps stall on intermittent rural 2G/EDGE cellular connections.
2. **The "Black Box" Problem**: Opaque AI recommendations (*"Spray chemical X on Tuesday"*) inspire distrust because they lack context.
3. **Linguistic & Literacy Barriers**: Advisories delivered exclusively in English or high-density technical jargon exclude vernacular-speaking farmers.

### Earthworm's Solution
- **Ultra-Resilient Dual-Mode Interface**: Full visual interactive dashboard on broadband with an instant one-click toggle to **2G Low-Bandwidth Mode** (strips heavy tiles and heavy charts to operate under 15 KB).
- **3-Stage Explainable Agronomy**: Every advisory is structured into:
  1. **Notice** (*What the satellite saw* – e.g., 14% drop in vegetation canopy greenness).
  2. **Meaning** (*Why it matters agronomically* – e.g., panicle moisture stress during critical tillering).
  3. **Action** (*Exact next steps* – e.g., irrigate 4–5 cm, withhold excess urea).
- **Multilingual Vernacular Delivery**: Native support for **English**, **Kannada (ಕನ್ನಡ)**, and **Hindi (हिन्दी)** with built-in voice readouts via the Web Speech API and 160-character SMS previews.

---

## 2. End-to-End System Workflow

The following flowchart illustrates the complete lifecycle of data through Earthworm:

```
+-----------------------------------------------------------------------------------+
| 1. DATA ACQUISITION & INGESTION                                                   |
| - Copernicus Sentinel-2 MSI (10m Multi-Spectral: Band 4 Red, Band 8 NIR)          |
| - Open-Meteo High-Resolution Agro-Weather (Rainfall, Relative Humidity, Temp)     |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 2. AGRONOMIC PROCESSING & ANOMALY DETECTION                                       |
| - NDVI Computation: (NIR - Red) / (NIR + Red)                                      |
| - Multi-Temporal Baseline Comparison (10-day rolling baseline vs. regional norms) |
| - Cloud-masking & Quality Flag Filtering (SCL Scene Classification)               |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 3. PERSISTENCE LAYER (HYBRID ENGINE)                                              |
| - Primary: Supabase PostgreSQL (PostgREST API, RLS Policies, Service Role)        |
| - Fallback: In-memory curated agronomic fixtures (pan-India demo parcels)         |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 4. FASTAPI BACKEND API LAYER                                                      |
| - GET /api/health       -> System status & mode ('live' vs. 'demo_ready')          |
| - GET /api/health/db    -> Safe non-destructive Supabase PostgREST probe          |
| - GET /api/farms        -> Cadastral parcel listings                              |
| - GET /api/farms/{id}/advisory?language=kn -> Localized 3-stage advisory          |
| - GET /api/farms/{id}/observations        -> 20-day historical NDVI trend         |
| - GET /api/farms/{id}/weather             -> 3-day meteorological outlook         |
| - GET /                 -> Dual-mode root: serves Web UI or API metadata JSON     |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 5. FARMER-FACING FRONTEND DASHBOARD                                               |
| - Broadband Mode: Interactive Leaflet map + SVG NDVI trend + Weather cards        |
| - 2G Resilient Mode: High-contrast, zero-tile text layout (< 15 KB payload)      |
| - Vernacular Voice Engine: In-browser Web Speech API audio narration               |
| - SMS Broadcast Simulator: Character-counted telecom preview for feature phones   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Libraries & Technologies Used

### Backend Python Dependencies

All backend dependencies are defined in `requirements.txt` and `backend/requirements.txt`:

| Library | Version Spec | Purpose in Earthworm |
| :--- | :--- | :--- |
| **`fastapi`** | `>=0.110.0` | High-performance, asynchronous web framework powering all REST endpoints, OpenAPI/Swagger documentation generation, and ASGI lifecycle. |
| **`uvicorn[standard]`** | `>=0.28.0` | Ultra-fast ASGI production server built on `uvloop` and `httptools` providing hot-reload and worker management. |
| **`pydantic`** | `>=2.6.0` | Strict data validation, schema enforcement, data serialization, and runtime type checking across all data contracts. |
| **`pydantic-settings`** | `>=2.2.0` | Type-safe application configuration management, cascading `.env` file resolution, and environment variable parsing. |
| **`supabase`** | `>=2.33.0` | Official Supabase Python SDK for connecting to PostgreSQL via Supabase's PostgREST gateway, storage buckets, and auth. |
| **`httpx`** | `>=0.27.0` | Modern, asynchronous/synchronous HTTP client used for safe, non-destructive connection probing of Supabase and internal test clients. |
| **`pytest`** | `>=8.0.0` | Test framework for executing the 22 automated test cases covering health checks, farm endpoints, advisories, Supabase fallbacks, and Vercel compatibility. |

---

### Frontend Libraries & Web APIs

The frontend is built with clean Vanilla HTML5 and JavaScript without heavy npm bundling overhead:

| Library / Web API | Source / Version | Purpose in Earthworm |
| :--- | :--- | :--- |
| **`Leaflet.js`** | `v1.9.4` (CDN) | Interactive mapping library rendering satellite imagery tiles, cadastral farm parcel boundaries, NDVI heat overlays, and regional pins. |
| **`Tailwind CSS`** | `v3.x` (CDN) | Utility-first CSS framework styled with earthy, agricultural color tokens (`emerald`, `amber`, `stone`, `teal`). |
| **`Web Speech API`** | Native Browser API | Zero-latency, client-side synthetic speech synthesis (`window.speechSynthesis`) providing audio readouts in Kannada, Hindi, and English without incurring third-party cloud API costs. |
| **`Google Fonts`** | `Outfit` & `Inter` | Clean, modern typography designed for maximum legibility on low-resolution mobile displays. |
| **`Custom SVG Engine`**| Native JavaScript | Lightweight vector generators for 20-day historical NDVI trend bars, cloud-cover markers, and weather sparklines without pulling in bulky charting libraries. |

---

## 4. Detailed Python Script Documentation

Every Python file across the repository serves a distinct, modular role:

```
backend/
├── api/
│   └── index.py               # Vercel serverless function entrypoint (backend mirror)
├── app/
│   ├── __init__.py            # Marks app directory as a Python package
│   ├── main.py                # Main application factory & route orchestration
│   ├── config.py              # Centralized Pydantic application configuration
│   ├── api/
│   │   ├── __init__.py        # Marks api package
│   │   └── routes/
│   │       ├── __init__.py    # Marks routes package
│   │       ├── health.py      # Health & Supabase probe endpoints
│   │       └── farms.py       # Farms, advisories, observations & weather routes
│   ├── data/
│   │   ├── __init__.py        # Marks data package
│   │   └── demo/
│   │       ├── __init__.py    # Marks demo package
│   │       └── fixtures.py    # Curated pan-India demo parcels & trilingual advisories
│   ├── db/
│   │   ├── __init__.py        # Marks db package
│   │   └── supabase.py        # Reusable client singleton & safe connection verifier
│   └── schemas/
│       ├── __init__.py        # Marks schemas package
│       ├── farm.py            # Pydantic schemas for farm metadata
│       ├── observation.py     # Pydantic schemas for NDVI & time-series
│       ├── advisory.py        # Pydantic schemas for 3-stage agronomic advisories
│       └── communication.py   # Pydantic schemas for SMS & voice preview
└── tests/
    ├── __init__.py            # Marks tests package
    ├── test_health.py         # Test suite for health & error handling
    ├── test_farms.py          # Test suite for farm domain endpoints
    ├── test_supabase.py       # Test suite for Supabase fallback & security
    └── test_vercel.py         # Test suite for Vercel serverless compatibility
```

---

### Entrypoints & Core Configuration

#### 1. `api/index.py` (and `backend/api/index.py`)
- **Purpose**: Serves as the serverless function handler when deployed to **Vercel**.
- **How it works**:
  - Dynamically calculates the project root and `backend/` directories.
  - Inserts the appropriate directory into `sys.path` so that imports (`from app.main import app`) resolve reliably regardless of whether Vercel's root directory is set to `.` or `backend/`.
  - Exposes `app` as an ASGI application discovered by Vercel's Python runtime.

#### 2. `backend/app/config.py`
- **Purpose**: Centralized application settings using `pydantic_settings.BaseSettings`.
- **How it works**:
  - Reads configuration values from `backend/.env` or system environment variables.
  - Declares core properties: `app_name`, `app_env`, `debug`, `host`, `port`, and `api_prefix`.
  - Declares Supabase configuration keys: `supabase_url`, `supabase_secret_key`, and alias `supabase_key`.
  - Provides a computed property `effective_supabase_key` that checks both standard and alias key names.
  - Defaults all secrets to `None` so the application boots immediately out-of-the-box without requiring external configuration.

#### 3. `backend/app/main.py`
- **Purpose**: Application factory, middleware setup, route registration, and static file mounting.
- **How it works**:
  - `create_app() -> FastAPI`: Instantiates the FastAPI application with configured metadata and Swagger documentation.
  - Configures **CORS Middleware** (`allow_origins=["*"]`) enabling frontend clients to interact with the API across different domains or local ports.
  - Configures a **Global Exception Handler** that catches unhandled exceptions and formats them into structured JSON (`500 InternalServerError`).
  - Registers the `health.router` and `farms.router` under the `/api` prefix.
  - Mounts static file directories for `/app` and `/frontend` using `StaticFiles(html=True)`.
  - **Dual-Mode `GET /` Route**:
    - Inspects incoming request headers.
    - If the request comes from a web browser (`Accept: text/html` without explicit `?format=json`), it serves the interactive frontend HTML (`index.html` / `code.html`).
    - If requested by an API client, curl, or automated test client (`format=json` or `Accept: application/json`), it returns structured application metadata JSON.

---

### Database & Storage Layer

#### 4. `backend/app/db/supabase.py`
- **Purpose**: Manages the backend-only Supabase client lifecycle and connection verification.
- **Key Functions**:
  - `is_supabase_configured() -> bool`: Verifies that `SUPABASE_URL` and `SUPABASE_SECRET_KEY` are populated and not default dummy placeholders.
  - `get_supabase_client() -> Optional[Client]`: Singleton accessor that initializes `create_client(url, key)`. Returns `None` if credentials are absent, allowing the application to operate in demo mode without crashing.
  - `reset_supabase_client() -> None`: Clears the cached client singleton (crucial for automated testing under mock environments).
  - `verify_supabase_connection(timeout: float = 4.0) -> Dict[str, Any]`: Performs a safe, read-only HTTP GET probe against Supabase's PostgREST root (`/rest/v1/`). Never exposes API keys in logs or responses; returns safe connection status codes (`connected`, `authentication_failed`, `connection_error`, `not_configured`).

---

### Domain Data Schemas (Pydantic)

#### 5. `backend/app/schemas/farm.py`
- **Purpose**: Defines data models for farm holdings and parcels.
- **Models**:
  - `FarmBase`: Declares parcel fields including `id`, `name`, `district`, `state`, `crop`, `crop_variety`, `crop_season`, `growth_stage`, `survey_plot`, `area_hectares`, and `data_status`.
  - `Farm`: Inherits from `FarmBase` for domain modeling and API responses.

#### 6. `backend/app/schemas/observation.py`
- **Purpose**: Defines Earth observation data structures.
- **Models**:
  - `ObservationPoint`: Represents a single historical satellite acquisition with `date`, `ndvi` (float), and `cloud_cover` percentage.
  - `Observation`: Represents a complete observation record including current `metric` ("NDVI"), `value`, `benchmark_value`, `unit`, `quality_flags`, `source` ("Copernicus Sentinel-2 MSI"), and a list of `history` points.

#### 7. `backend/app/schemas/advisory.py`
- **Purpose**: Defines the structure for 3-stage explainable agronomic guidance.
- **Models**:
  - `Advisory`: Contains `id`, `farm_id`, `created_at`, `language`, `severity` (e.g., "advisory_warning"), `headline`, `description`, `metric_summary`, `notice`, `meaning`, `next_steps` (list of actionable steps), `sms_preview`, `voice_transcript`, `uncertainty_note`, and `data_status`.

#### 8. `backend/app/schemas/communication.py`
- **Purpose**: Defines models for low-bandwidth message simulation.
- **Models**:
  - `CommunicationPreview`: Contains `id`, `farm_id`, `language`, `channel` ("sms" or "voice"), `preview_text`, `char_count`, `audio_url`, and `status`.

---

### API Route Handlers (FastAPI)

#### 9. `backend/app/api/routes/health.py`
- **Purpose**: System health diagnostics and database connectivity monitoring.
- **Endpoints**:
  - `GET /api/health`: Returns service health status, application name, ISO 8601 UTC timestamp, and `data_mode` (`"live"` if Supabase is connected, `"demo_ready"` if running off fixtures).
  - `GET /api/health/db`: Executes `verify_supabase_connection()` and returns structured database connectivity status without exposing secrets.

#### 10. `backend/app/api/routes/farms.py`
- **Purpose**: Main business logic endpoints for farms, advisories, observations, and weather.
- **Endpoints**:
  - `GET /api/farms`: Lists all monitored parcels across India.
  - `GET /api/farms/{farm_id}`: Retrieves parcel metadata for a specific farm (returns 404 if not found).
  - `GET /api/farms/{farm_id}/observations`: Retrieves the latest satellite NDVI observation and 20-day historical time-series.
  - `GET /api/farms/{farm_id}/advisory?language={en|kn|hi}`: Retrieves the 3-stage explainable advisory in English, Kannada, or Hindi with graceful English fallback.
  - `GET /api/farms/{farm_id}/communications/preview?channel={sms|voice}&language={en|kn|hi}`: Generates character-budgeted SMS previews and speech transcripts.
  - `GET /api/farms/{farm_id}/weather`: Retrieves a 3-day meteorological outlook (precipitation, humidity, temp, advisory hints).

---

### Demonstration Data & Agronomic Fixtures

#### 11. `backend/app/data/demo/fixtures.py`
- **Purpose**: Supplies authentic agricultural demonstration data representing four distinct agro-climatic zones across India:
  1. **Mandya, Karnataka**: Plot #142/A (Sona Masoori Paddy, Panicle Initiation stage) experiencing moisture stress.
  2. **Ludhiana, Punjab**: Plot #89/C (PBW 343 Wheat, Active Tillering stage).
  3. **Varanasi, Uttar Pradesh**: Plot #214/B (Varuna Mustard & Vegetables, Flowering stage).
  4. **Nashik, Maharashtra**: Plot #56/D (Red Pinhead Onion, Bulb Expansion stage).
- Contains full trilingual advisories (English, Kannada script, and Hindi Devanagari script) complete with agronomic recommendations, SMS text, and voice transcripts.

---

### Automated Test Suite (Pytest)

All tests are executed with `pytest -v` and run in **1.6 seconds**:

#### 12. `backend/tests/test_health.py` (4 tests)
- Tests `test_root_endpoint`: Verifies application metadata at `GET /`.
- Tests `test_health_check_returns_200`: Confirms 200 OK, service name, and data mode at `GET /api/health`.
- Tests `test_health_check_timestamp_format`: Asserts valid ISO 8601 UTC timestamp format.
- Tests `test_unknown_route_returns_404`: Validates structured 404 responses for non-existent endpoints.

#### 13. `backend/tests/test_farms.py` (8 tests)
- Tests `test_list_farms`: Confirms 4 demo parcels are returned.
- Tests `test_get_specific_farm`: Verifies Mandya farm metadata.
- Tests `test_get_unknown_farm_returns_404`: Validates 404 behavior for unknown farm IDs.
- Tests `test_get_observations`: Validates NDVI values, benchmark metrics, and history arrays.
- Tests `test_get_advisory_english`: Verifies 3-stage fields (`notice`, `meaning`, `next_steps`).
- Tests `test_get_advisory_kannada`: Validates vernacular Kannada text delivery (`ತೇವಾಂಶ`).
- Tests `test_get_communication_preview_sms`: Verifies telecom character counting and preview status.
- Tests `test_get_weather`: Confirms 3-day meteorological forecast structure.

#### 14. `backend/tests/test_supabase.py` (5 tests)
- Tests `test_supabase_unconfigured_by_default`: Asserts safe demo mode fallback when `.env` is absent.
- Tests `test_health_db_endpoint_unconfigured`: Verifies `GET /api/health/db` returns `configured: false`.
- Tests `test_verify_connection_never_exposes_secret_key`: Proves that secrets are never leaked in responses.
- Tests `test_verify_connection_success_mocked`: Validates HTTP 200 handling from Supabase PostgREST.
- Tests `test_verify_connection_auth_failure_mocked`: Validates HTTP 401 handling without crashing.

#### 15. `backend/tests/test_vercel.py` (5 tests)
- Tests `test_vercel_entrypoint_health`: Verifies Vercel entrypoint routes `/api/health`.
- Tests `test_vercel_entrypoint_farms`: Verifies Vercel entrypoint routes `/api/farms`.
- Tests `test_vercel_entrypoint_kannada_advisory`: Verifies Vercel entrypoint localized advisories.
- Tests `test_vercel_entrypoint_root_browser_request`: Confirms browser requests to `/` receive visual HTML.
- Tests `test_vercel_entrypoint_root_api_json_request`: Confirms API requests to `/?format=json` receive JSON.

---

## 5. In-Depth Supabase Integration Architecture

### Design Philosophy: Non-Blocking Graceful Fallback

Earthworm follows a **zero-downtime, backend-first** approach to external database dependencies:

```
                      +-----------------------------+
                      | Application Startup         |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      | Is SUPABASE_URL & Key set?  |
                      +------+---------------+------+
                             |               |
                       [No]  |               |  [Yes]
                             v               v
             +--------------------+    +--------------------+
             | Operational Mode:  |    | Operational Mode:  |
             | "demo_ready"       |    | "live"             |
             | Serves Curated     |    | Initializes Client |
             | Demo Fixtures      |    | & Queries Postgres |
             +--------------------+    +--------------------+
```

1. **No Hard Crashes**: If Supabase credentials are missing, empty, or misconfigured, the backend logs an informational message and automatically falls back to curated agronomic fixtures.
2. **Read-Only Verification**: The application verifies database connectivity via an active probe without mutating tables, creating temporary records, or executing destructive SQL.
3. **No Credential Exposure**: Supabase secret keys are used exclusively on the backend. No secret key is ever returned in an HTTP response, logged to stdout, or committed to source control.

---

### Safe Connection Verification (Zero-Leakage Probing)

The `verify_supabase_connection()` function probes Supabase safely:

```python
endpoint = f"{url.rstrip('/')}/rest/v1/"
headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
}
response = httpx.get(endpoint, headers=headers, timeout=4.0)
```

- When valid credentials are supplied, Supabase PostgREST responds with **HTTP 200** (returning the OpenAPI schema for the database).
- If the key is invalid or revoked, PostgREST returns **HTTP 401/403 Unauthorized**.
- If the domain does not resolve, `httpx.ConnectError` is caught safely.
- In all outcomes, only the parsed hostname (`xyz.supabase.co`) is surfaced, never the key itself.

---

### Database Schema (PostgreSQL DDL)

When you are ready to transition from demo fixtures to live database tables, run the following SQL script in your **Supabase SQL Editor**:

```sql
-- 1. Enable UUID Extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Farms Table
CREATE TABLE IF NOT EXISTS public.farms (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    district TEXT NOT NULL,
    state TEXT NOT NULL,
    crop TEXT NOT NULL,
    crop_variety TEXT,
    crop_season TEXT,
    growth_stage TEXT,
    survey_plot TEXT,
    area_hectares NUMERIC(6, 2),
    data_status TEXT DEFAULT 'live',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Satellite Observations Table
CREATE TABLE IF NOT EXISTS public.observations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id TEXT REFERENCES public.farms(id) ON DELETE CASCADE,
    observed_at TIMESTAMPTZ NOT NULL,
    retrieved_at TIMESTAMPTZ DEFAULT NOW(),
    source TEXT DEFAULT 'Copernicus Sentinel-2 MSI',
    observation_type TEXT DEFAULT 'optical_multispectral',
    metric TEXT DEFAULT 'NDVI',
    value NUMERIC(4, 3) NOT NULL,
    benchmark_value NUMERIC(4, 3),
    unit TEXT DEFAULT 'NDVI [-1 to 1]',
    quality_flags TEXT DEFAULT 'cloud_free',
    status TEXT DEFAULT 'verified',
    method TEXT DEFAULT 'mean_parcel_reflectance',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Historical NDVI Observation Points (Time-Series)
CREATE TABLE IF NOT EXISTS public.observation_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id TEXT REFERENCES public.farms(id) ON DELETE CASCADE,
    observation_date DATE NOT NULL,
    ndvi NUMERIC(4, 3) NOT NULL,
    cloud_cover NUMERIC(4, 1) DEFAULT 0.0
);

-- 5. Agronomic Advisories Table
CREATE TABLE IF NOT EXISTS public.advisories (
    id TEXT PRIMARY KEY,
    farm_id TEXT REFERENCES public.farms(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    language TEXT NOT NULL DEFAULT 'en',
    severity TEXT NOT NULL DEFAULT 'info',
    headline TEXT NOT NULL,
    description TEXT NOT NULL,
    metric_summary TEXT,
    notice TEXT NOT NULL,
    meaning TEXT NOT NULL,
    next_steps JSONB NOT NULL DEFAULT '[]'::jsonb,
    sms_preview TEXT,
    voice_transcript TEXT,
    uncertainty_note TEXT,
    data_status TEXT DEFAULT 'live'
);

-- 6. Row Level Security (RLS)
ALTER TABLE public.farms ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.observations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.observation_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.advisories ENABLE ROW LEVEL SECURITY;

-- Allow public read access (or restrict to authenticated service role)
CREATE POLICY "Allow public read access to farms" ON public.farms FOR SELECT USING (true);
CREATE POLICY "Allow public read access to observations" ON public.observations FOR SELECT USING (true);
CREATE POLICY "Allow public read access to observation_history" ON public.observation_history FOR SELECT USING (true);
CREATE POLICY "Allow public read access to advisories" ON public.advisories FOR SELECT USING (true);
```

---

### Manual Setup & Credential Management

To connect your live Supabase project to Earthworm:

1. Open your Supabase Dashboard: `https://supabase.com/dashboard/project/<your-project-id>/settings/api`
2. Locate:
   - **Project URL**: e.g., `https://njaqygzvfpcctxyjcuhb.supabase.co`
   - **Service Role Key** (or `anon` public key for read-only access).
3. Create or update `backend/.env`:
   ```env
   SUPABASE_URL=https://njaqygzvfpcctxyjcuhb.supabase.co
   SUPABASE_SECRET_KEY=your_actual_service_role_key_here
   ```
4. Restart the FastAPI server.
5. Query `GET /api/health/db` to verify connection status:
   ```json
   {
     "configured": true,
     "connected": true,
     "status": "connected",
     "message": "Successfully connected and authenticated with Supabase PostgREST.",
     "host": "njaqygzvfpcctxyjcuhb.supabase.co"
   }
   ```

---

## 6. Deployment & Execution Instructions

### Local Development

1. **Activate the Virtual Environment**:
   ```powershell
   # Windows PowerShell
   cd c:\Earthworm\backend
   .\.venv\Scripts\Activate.ps1
   ```

2. **Run Automated Tests**:
   ```powershell
   pytest -v
   ```

3. **Start the FastAPI Development Server**:
   ```powershell
   uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
   ```

4. **Access Applications in Browser**:
   - **Interactive Web App**: [http://127.0.0.1:8080/](http://127.0.0.1:8080/)
   - **Interactive Swagger Docs**: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
   - **Service Health Check**: [http://127.0.0.1:8080/api/health](http://127.0.0.1:8080/api/health)
   - **Supabase DB Probe**: [http://127.0.0.1:8080/api/health/db](http://127.0.0.1:8080/api/health/db)

---

### Vercel Serverless Production Deployment

Earthworm is configured for zero-configuration deployment to **Vercel**:
- [vercel.json](file:///c:/Earthworm/vercel.json) rewrites `/api/*` to the Python serverless function at `/api/index.py`.
- Static files at root `/` and `/frontend/*` are served directly through Vercel's Edge Network with ultra-low latency.
- Repository: [https://github.com/neerajp-10/gcemHacks5.0](https://github.com/neerajp-10/gcemHacks5.0)
