# 🌍 Earthworm | Complete Technical Workflow, Architecture & Implementation Guide

> **Satellite-Powered Early-Warning and Explainable Crop Advisory for Smallholder Farmers**  
> *Targeted at Smallholder Paddy Farmers in Mandya, Karnataka & Pan-India Demo Parcels*

---

## 📋 Table of Contents
1. [Project Overview & Core Philosophy](#1-project-overview--core-philosophy)
   - [The Smallholder Reality](#the-smallholder-reality)
   - [Earthworm's Three Pillars](#earthworms-three-pillars)
2. [End-to-End System Workflow](#2-end-to-end-system-workflow)
   - [Complete Architectural Workflow Diagram](#complete-architectural-workflow-diagram)
   - [Data Lifecycle & Subsystems](#data-lifecycle--subsystems)
3. [Low-Bandwidth Rural Agri-Telephony Subsystem](#3-low-bandwidth-rural-agri-telephony-subsystem)
   - [Core Principle: Decoupled Web & Cellular Telephony](#core-principle-decoupled-web--cellular-telephony)
   - [Outbound Cellular SMS Advisory (160-Char Budget)](#outbound-cellular-sms-advisory-160-char-budget)
   - [Outbound Automated IVR Voice Phone Calls](#outbound-automated-ivr-voice-phone-calls)
   - [Headless Background Dispatcher CLI (`dispatch_advisory.py`)](#headless-background-dispatcher-cli-dispatch_advisorypy)
   - [Two-Way Low-Bandwidth Helpline Webhooks](#two-way-low-bandwidth-helpline-webhooks)
     - [Missed Call / IVR Helpline (`/api/communications/incoming-call`)](#missed-call--ivr-helpline)
     - [Inbound SMS Advisory Gateway (`/api/communications/incoming-sms`)](#inbound-sms-advisory-gateway)
   - [Multi-Lingual Neural Voice Synthesis Engine](#multi-lingual-neural-voice-synthesis-engine)
   - [Twilio Provider Credentials & Dual-Mode Telephony](#twilio-provider-credentials--dual-mode-telephony)
4. [7 Vernacular Indian Languages Expansion](#4-7-vernacular-indian-languages-expansion)
   - [Language Matrix & Regional Dialects](#language-matrix--regional-dialects)
   - [Unified Translation Architecture](#unified-translation-architecture)
5. [Advanced Satellite Parcel Inspector](#5-advanced-satellite-parcel-inspector)
   - [5 Multispectral Satellite Layers](#5-multispectral-satellite-layers)
   - [Agronomic Significance & Interactive Visualizer](#agronomic-significance--interactive-visualizer)
6. [Libraries & Technologies Used](#6-libraries--technologies-used)
   - [Backend Python Dependencies](#backend-python-dependencies)
   - [Frontend Frameworks & Libraries](#frontend-frameworks--libraries)
7. [Detailed Python Script & Codebase Documentation](#7-detailed-python-script--codebase-documentation)
   - [Entrypoints & Server Configuration](#entrypoints--server-configuration)
   - [API Route Handlers (FastAPI)](#api-route-handlers-fastapi)
   - [Business Logic & Service Layer](#business-logic--service-layer)
   - [Pydantic Domain Schemas](#pydantic-domain-schemas)
   - [Automated Pytest Suite](#automated-pytest-suite)
8. [Copernicus Sentinel Hub Live Satellite Integration](#8-copernicus-sentinel-hub-live-satellite-integration)
   - [OAuth2 Client Credentials & Token Caching](#oauth2-client-credentials--token-caching)
   - [Process API & True-Color Evalscript](#process-api--true-color-evalscript)
   - [Regional Bounding Boxes & Dynamic Fallbacks](#regional-bounding-boxes--dynamic-fallbacks)
9. [In-Depth Supabase Integration Architecture](#9-in-depth-supabase-integration-architecture)
   - [Non-Blocking Hybrid Storage Design](#non-blocking-hybrid-storage-design)
   - [PostgreSQL Database Schema (DDL)](#postgresql-database-schema-ddl)
   - [Connection Verification & Safe Probing](#connection-verification--safe-probing)
10. [Deployment & Execution Instructions](#10-deployment--execution-instructions)
    - [Local Development & CLI Execution](#local-development--cli-execution)
    - [Automated Testing](#automated-testing)
    - [Vercel Serverless Production Deployment](#vercel-serverless-production-deployment)

---

## 1. Project Overview & Core Philosophy

**Earthworm** bridges the critical "last-mile" barrier separating spaceborne Earth observation (Copernicus Sentinel-2 multispectral sensors, Open-Meteo agro-meteorological forecasting) and smallholder farmers cultivating 0.5 to 2-acre parcels across rural India.

### The Smallholder Reality
Traditional commercial agri-tech platforms fail rural farmers due to three chronic disconnects:
1. **Bandwidth Poverty & Feature Phone Ownership**: Smallholders in remote agrarian belts frequently rely on basic 2G/3G keypad feature phones without reliable mobile data connections. Requiring farmers to download heavy web or mobile applications ensures total exclusion.
2. **The "Black Box" Trust Deficit**: Opaque AI recommendations (*"Spray 250ml fungicide on Tuesday"*) generate distrust because they do not explain *what* was detected, *why* it matters, or *how* the conclusion was reached.
3. **Linguistic & Jargon Barriers**: Advisories delivered in technical English or academic terminology are inaccessible to vernacular-speaking farmers.

### Earthworm's Three Pillars
- **Decoupled Low-Bandwidth Delivery**: Advisories are delivered directly over cellular telecom networks (GSM/PSTN) via 160-character cellular SMS and automated IVR voice phone calls straight to the farmer's physical phone number (`+91 9731803808`). Zero internet access, smartphones, or web pages are required on the farmer's end.
- **3-Stage Explainable Agronomy**: Every advisory translates raw sensor observations into three plain-language steps:
  1. **Notice** (*What the satellite saw* – e.g., 14% drop in vegetation canopy greenness over 10 days).
  2. **Meaning** (*Why it matters agronomically* – e.g., panicle moisture stress during critical tillering phase).
  3. **Action** (*Exact next steps* – e.g., irrigate 4–5 cm immediately, withhold urea application).
- **Comprehensive 7-Language Vernacular Support**: Native UI, audio speech streaming, SMS segments, and voice call readouts across **English**, **Kannada (ಕನ್ನಡ)**, **Hindi (हिन्दी)**, **Telugu (తెలుగు)**, **Tamil (தமிழ்)**, **Marathi (मराठी)**, and **Bengali (বাংলা)**.

---

## 2. End-to-End System Workflow

### Complete Architectural Workflow Diagram

```
+-------------------------------------------------------------------------------------------------------+
|                                1. DATA ACQUISITION & REMOTE SENSING                                   |
| - European Space Agency (ESA) Copernicus Sentinel-2 MSI (10m Multi-Spectral: B02, B03, B04, B08)     |
| - Sentinel Hub Process API (services.sentinel-hub.com) with true-color BOA L2A Evalscript             |
| - Open-Meteo Regional Agro-Meteorological Forecasts (Rainfall, Relative Humidity, Soil Temp)          |
+---------------------------------------------------+---------------------------------------------------+
                                                    |
                                                    v
+-------------------------------------------------------------------------------------------------------+
|                               2. AGRONOMIC ENGINE & ANOMALY DETECTION                                 |
| - Multispectral Vegetation Indices:                                                                  |
|   * NDVI = (NIR - Red) / (NIR + Red)               [Canopy Vigor & Biomass Density]                   |
|   * CIR = NIR False Color Composite                [Leaf Cellular Structure & Health]                 |
|   * NDWI = (NIR - SWIR) / (NIR + SWIR)             [Canopy Water Content & Moisture Stress]           |
|   * SAR Proxy = Dual-Pol Backscatter Reflectance   [Root-Zone Soil Hydration Dynamics]                |
| - 10-Day Rolling Temporal Baseline Comparison (Flags early-stage water/nutrient stress anomalies)    |
| - 3-Stage Explainable Agronomic Engine (Transforms indices into Notice -> Meaning -> Action)          |
+---------------------------------------------------+---------------------------------------------------+
                                                    |
                                                    v
+-------------------------------------------------------------------------------------------------------+
|                               3. HYBRID PERSISTENCE LAYER (ZERO-LOCKIN)                               |
| - Primary Store: Supabase PostgreSQL via PostgREST API (RLS security, farm parcels, telemetry)       |
| - Safe Non-Blocking Fallback: In-memory agronomic fixtures for zero-downtime offline execution        |
+---------------------------------------------------+---------------------------------------------------+
                                                    |
                                                    v
+-------------------------------------------------------------------------------------------------------+
|                                    4. FASTAPI BACKEND API LAYER                                       |
| - Core Health:           GET  /api/health, GET /api/health/db, GET /api/health/sentinel              |
| - Farm Metadata:         GET  /api/farms, GET /api/farms/{id}, GET /api/farms/{id}/satellite-image   |
| - Agronomic Advisory:    GET  /api/farms/{id}/advisory?language=kn                                    |
| - Parcel Telemetry:      GET  /api/farms/{id}/observations, GET /api/farms/{id}/weather                |
| - Telephony Status:      GET  /api/communications/status                                              |
| - Outbound Cellular SMS: POST /api/communications/sms                                                 |
| - Outbound IVR Call:     POST /api/communications/call                                                |
| - Unified Dispatch:      POST /api/communications/dispatch-low-bandwidth                              |
| - Inbound IVR Helpline:  POST /api/communications/incoming-call  (Twilio Voice Webhook)               |
| - Inbound SMS Helpline:  POST /api/communications/incoming-sms   (Twilio SMS Webhook)                 |
| - Natural Voice Stream:  GET  /api/communications/speak?language=kn&farm_id=mandya                    |
+----------------------------------+----------------------------------+---------------------------------+
                                   |                                  |
                                   v                                  v
+----------------------------------------------------+  +-----------------------------------------------+
|       5. EXTENSION WORKER / AGRONOMIST UI          |  |   6. LOW-BANDWIDTH CELLULAR TELECOM SUBSYSTEM |
|      (Web Dashboard & Control Center)              |  |      (Farmer Feature Phone / Keypad Device)   |
| - Leaflet Parcel Map & Boundary GeoJSON            |  | - Direct GSM/PSTN Cellular Delivery           |
| - Multi-Layer Parcel Inspector:                    |  | - 160-character vernacular SMS text message   |
|   * NDVI Heatmap, CIR Infrared, True Color RGB,    |  | - Automated inbound/outbound IVR voice calls  |
|     Moisture Stress (NDWI), SAR Radar Proxy        |  | - Zero web browser, zero app, zero internet   |
| - 20-Day NDVI Historical Trend Line                |  | - Standalone CLI: dispatch_advisory.py        |
| - 3-Day Agro-Weather Outlook Cards                 |  | - Missed Call / IVR Dial-in Helpline          |
| - 7-Language Vernacular Switcher                   |  | - Two-Way Inbound SMS Query Gateway           |
+----------------------------------------------------+  +-----------------------------------------------+
```

---

## 3. Low-Bandwidth Rural Agri-Telephony Subsystem

### Core Principle: Decoupled Web & Cellular Telephony
A foundational architectural principle of Earthworm is the **strict separation between the administrative dashboard and last-mile farmer communication**:
- **The Web Dashboard** (`http://127.0.0.1:8080/`) serves agricultural extension officers, agronomists, village cooperatives, and field researchers who possess laptops, smartphones, and internet access.
- **The Farmer** (`+91 9731803808`) interacts strictly through their physical phone handset over standard 2G/3G cellular towers (GSM/PSTN). The farmer does **not** visit a webpage, launch a browser, or download an application.

### Outbound Cellular SMS Advisory (160-Char Budget)
- **Constraint**: Feature phones operating on 2G networks receive text via standard 160-character GSM-7 / UCS-2 SMS segments.
- **Payload Design**: The backend auto-derives concise, highly actionable advisories fitting within 1 SMS segment:
  - Example (Kannada, 129 chars):  
    `[ಅರ್ಥ್‌ವರ್ಮ್-ಕೃಷಿ] ಪ್ಲಾಟ್ 142/A (ಮಂಡ್ಯ): ಈಶಾನ್ಯ ಭಾಗದಲ್ಲಿ ತೇವಾಂಶ ಇಳಿಕೆ. ಮುಂದಿನ 3 ದಿನ ಮಳೆಯಿಲ್ಲ. ನೀರು ಹಾಯಿಸುವ ಮುನ್ನ ಮಣ್ಣು ಪರಿಶೀಲಿಸಿ.`
  - Example (English, 139 chars):  
    `[EARTHWORM-AGRI] Plot 142/A (Mandya): Moisture stress detected in NE zone. No rain expected next 3 days. Inspect topsoil before irrigating.`
- **API Endpoint**: `POST /api/communications/sms`
  ```json
  {
    "to": "+919731803808",
    "farm_id": "mandya",
    "language": "kn"
  }
  ```

### Outbound Automated IVR Voice Phone Calls
- **Workflow**: Automated phone calls place a direct cellular trunk call to the farmer's SIM card. When the farmer answers the ring, an interactive voice response (IVR) reads the customized regional-language advisory.
- **TwiML Generation**: Dynamic XML response formatted with native pronunciation:
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <Response>
      <Say voice="Google.kn-IN-Standard-A" language="kn-IN">
          ನಮಸ್ಕಾರ ರೈತ ಬಾಂಧವರೇ. ಮಂಡ್ಯ ಪ್ಲಾಟ್ 142/A ಉಪಗ್ರಹ ವರದಿಯಂತೆ ಈಶಾನ್ಯ ವಲಯದಲ್ಲಿ ಬೆಳೆ ತೇವಾಂಶ ಕಡಿಮೆಯಾಗಿದೆ. ಮುಂದಿನ ಮೂರು ದಿನ ಮಳೆಯ ಮುನ್ಸೂಚನೆ ಇಲ್ಲ. ನೀರು ಹಾಯಿಸುವ ಮೊದಲು ಮಣ್ಣನ್ನು ಪರಿಶೀಲಿಸಿ.
      </Say>
  </Response>
  ```
- **API Endpoint**: `POST /api/communications/call`

### Headless Background Dispatcher CLI (`dispatch_advisory.py`)
To ensure total decoupling from the browser, Earthworm includes a standalone command-line dispatcher (`backend/dispatch_advisory.py`). This allows cron schedules, automated Sentinel-2 anomaly detection workers, or extension officers to trigger cellular communications directly from the operating system shell:

```powershell
# Dispatch both SMS and IVR voice call in Kannada to farmer mobile handset
python backend/dispatch_advisory.py --to "+919731803808" --farm mandya --lang kn --channel both

# Dispatch SMS only in Hindi to a farmer in Ludhiana
python backend/dispatch_advisory.py --to "+919876543210" --farm ludhiana --lang hi --channel sms

# Dispatch IVR voice call only in Marathi to a farmer in Nashik
python backend/dispatch_advisory.py --to "+919812345678" --farm nashik --lang mr --channel call
```

### Two-Way Low-Bandwidth Helpline Webhooks

#### Missed Call / IVR Helpline (`POST /api/communications/incoming-call`)
1. Smallholder farmers can give a **missed call** or dial the Earthworm helpline number.
2. Twilio receives the cellular call and issues an HTTP POST webhook to `/api/communications/incoming-call`.
3. The backend matches the caller's phone number or query parameters to their registered plot, synthesizes the latest advisory in their native language (e.g. Kannada), and returns the TwiML stream.
4. The farmer hears the advisory and the call disconnects—costing the farmer ₹0.

#### Inbound SMS Advisory Gateway (`POST /api/communications/incoming-sms`)
1. A farmer sends a basic SMS text query (e.g., `MANDYA`, `WEATHER`, or `STATUS`) from their keypad phone.
2. Twilio triggers the incoming SMS webhook at `/api/communications/incoming-sms`.
3. The backend parses the query text, derives the relevant 160-character localized advisory, and returns a `<Response><Message>...</Message></Response>` TwiML payload.
4. Twilio dispatches the reply SMS directly back to the farmer's phone inbox.

### Multi-Lingual Neural Voice Synthesis Engine
To prevent robotic, synthetic-sounding audio, Earthworm implements a multi-engine voice pipeline:
- **Twilio Carrier Engines**: Amazon Polly Aditi (`en-IN`, `hi-IN`) and Google Neural Cloud Voices (`kn-IN`, `te-IN`, `ta-IN`, `mr-IN`, `bn-IN`).
- **Streaming High-Fidelity Audio API (`GET /api/communications/speak`)**: Provides high-fidelity, naturally chunked MP3 audio streaming with in-memory caching for real-time audio playback.

### Twilio Provider Credentials & Dual-Mode Telephony
The telephony subsystem dynamically detects the presence of live carrier credentials in `backend/.env`:
- **Live Carrier Mode**: When `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_PHONE_NUMBER` are configured, calls and SMS messages are routed through real telecom trunks to physically ring and text `+91 9731803808`.
- **Telecom Simulation Mode**: When credentials are absent or during local development, the system executes full end-to-end telecom simulation (generating realistic SIDs like `SM840599...` and `CAde68...`, tracking segment budgets, and streaming synthetic audio), ensuring zero errors or disruptions during demos.

---

## 4. 7 Vernacular Indian Languages Expansion

Earthworm natively supports 7 major agrarian languages spoken across India's agricultural belts:

| Code | Language | Script | Monitored Agricultural Belt | Voice Synthesis Engine |
| :---: | :--- | :--- | :--- | :--- |
| **`kn`** | Kannada | ಕನ್ನಡ | Mandya, Cauvery Basin, Karnataka (Paddy, Sugarcane) | `Google.kn-IN-Standard-A` |
| **`hi`** | Hindi | हिन्दी | Varanasi, Gangetic Alluvium, UP (Mustard, Wheat) | `Polly.Aditi` |
| **`te`** | Telugu | తెలుగు | Krishna-Godavari Delta, Andhra/Telangana (Paddy, Cotton) | `Google.te-IN-Standard-A` |
| **`ta`** | Tamil | தமிழ் | Thanjavur, Cauvery Delta, Tamil Nadu (Paddy) | `Google.ta-IN-Standard-A` |
| **`mr`** | Marathi | मराठी | Nashik, Deccan Plateau, Maharashtra (Onion, Grapes) | `Google.mr-IN-Standard-A` |
| **`bn`** | Bengali | বাংলা | Burdwan, Lower Gangetic Plain, West Bengal (Rice, Jute) | `Google.bn-IN-Standard-A` |
| **`en`** | English | Latin | Pan-India Scientific / Agronomist Reference | `Polly.Aditi` (`en-IN`) |

Every linguistic profile includes full translations for:
- 3-Stage Explainable Advisory (Notice, Meaning, Action).
- 160-Character SMS segment preview.
- High-fidelity voice call audio transcript.
- Full dashboard navigation, buttons, weather badges, and telemetry labels.

---

## 5. Advanced Satellite Parcel Inspector

The dashboard replaces redundant parcel info modals with the **Multispectral Satellite Parcel Inspector**, offering five analytical satellite imaging modes:

```
+-----------------------------------------------------------------------------------+
|                        SATELLITE PARCEL INSPECTOR MODES                           |
+-------------------+-------------------------------+-------------------------------+
| Mode              | Spectral Bands                | Agronomic Diagnostic Purpose  |
+-------------------+-------------------------------+-------------------------------+
| 1. NDVI Heatmap   | NIR (B8) + Red (B4)           | Canopy greenness, biomass vigor|
| 2. Infrared (CIR) | NIR (B8) + Red (B4) + Green(B3)| Cell structure & plant health |
| 3. True Color RGB | Red (B4) + Green(B3) + Blue(B2)| Natural human-visible view    |
| 4. NDWI Moisture  | NIR (B8) + SWIR (B11)         | Leaf internal water content   |
| 5. SAR Radar      | Sentinel-1 C-Band VV/VH Proxy | Root-zone soil dielectric wetness|
+-------------------+-------------------------------+-------------------------------+
```

Each mode features:
- Interactive color scale ramps with live threshold indicators (e.g., `< 0.35` Water Stress, `> 0.70` Healthy Canopy).
- SVG rendering with regional coordinate grids and plot boundary delineations.
- Plain-language agronomic takeaways translated into the active vernacular language.

---

## 6. Libraries & Technologies Used

### Backend Python Dependencies
Defined in [backend/requirements.txt](file:///c:/Earthworm/backend/requirements.txt):

| Package | Version | Purpose & Architectural Justification |
| :--- | :--- | :--- |
| **`fastapi`** | `>=0.115.0` | Core high-performance ASGI web framework with automatic OpenAPI documentation. |
| **`pydantic`** | `>=2.10.0` | Strict data validation, schema serialization, and type enforcement. |
| **`pydantic-settings`** | `>=2.6.0` | Environment variable parsing and `.env` configuration management. |
| **`uvicorn[standard]`** | `>=0.32.0` | Production-grade ASGI web server handling HTTP requests and static asset delivery. |
| **`twilio`** | `>=9.0.0` | Twilio REST API client for cellular SMS transmission, IVR call dispatch, and TwiML generation. |
| **`httpx`** | `>=0.27.0` | Async and sync HTTP client for Sentinel Hub Process API and Supabase PostgREST queries. |
| **`requests`** | `>=2.31.0` | Reliable synchronous HTTP networking for external agro-weather and TTS requests. |
| **`pytest`** | `>=8.3.0` | Automated unit, regression, and integration testing framework. |
| **`pytest-anyio`** | `>=0.0.2` | Asynchronous test execution runner for FastAPI TestClient test suites. |

### Frontend Frameworks & Libraries
- **Vanilla Modern JavaScript**: Zero build steps; blazing-fast load times on low-bandwidth rural connections.
- **Tailwind CSS (Custom Token Build)**: Responsive design system adhering to accessible contrast ratios and tactile touch targets.
- **Leaflet.js (`v1.9.4`)**: Lightweight, mobile-friendly interactive mapping with custom parcel boundary GeoJSON layers.
- **Google Fonts (Outfit & Inter)**: Crisp, modern typography engineered for readability across mobile screen densities.
- **Google Material Symbols Outlined**: Intuitive agrarian and telephony iconography.

---

## 7. Detailed Python Script & Codebase Documentation

### Entrypoints & Server Configuration

#### `backend/app/main.py`
The primary FastAPI application instance:
- Configures CORS middleware supporting extension officer local testing and web clients.
- Mounts static file directories for imagery, assets, and frontend HTML.
- Implements a **Dual-Mode Root Endpoint (`GET /`)**:
  - Serves `frontend/index.html` when accessed by web browsers (`Accept: text/html`).
  - Serves API discovery metadata JSON when queried by automated API clients (`Accept: application/json`).
- Mounts API routers under `/api`: `health_router`, `farms_router`, and `communications_router`.

#### `backend/app/config.py`
Runtime configuration powered by `pydantic_settings.BaseSettings`:
- Resolves `.env` from `backend/.env` with safe, zero-crash fallback defaults.
- Computes `is_twilio_configured`: verifies `twilio_account_sid`, `twilio_auth_token`, and `twilio_phone_number`.
- Computes `is_sentinel_configured`: verifies `sentinel_client_id` and `sentinel_client_secret`.
- Computes `effective_supabase_key`: resolves primary and alias keys safely.

### API Route Handlers (FastAPI)

#### `backend/app/api/routes/communications.py`
Handles all telephony, messaging, and audio streaming endpoints:
- `GET /api/communications/status`: Reports carrier mode (`live` vs `simulation`), Twilio phone number, and voice engine mappings.
- `POST /api/communications/sms`: Dispatches cellular SMS advisory to farmer mobile numbers.
- `POST /api/communications/call`: Places automated IVR voice advisory call.
- `POST /api/communications/dispatch-low-bandwidth`: Headless unified endpoint dispatching SMS, voice call, or both.
- `POST /api/communications/incoming-call`: Webhook handling incoming farmer calls / missed-call callback.
- `POST /api/communications/incoming-sms`: Webhook handling incoming farmer SMS queries.
- `GET /api/communications/twiml`: Dynamic TwiML voice XML generator.
- `GET /api/communications/speak`: High-fidelity regional audio streaming endpoint.

#### `backend/app/api/routes/farms.py`
Exposes cadastral parcel listings and agronomic telemetry:
- `GET /api/farms`: Lists registered parcels with coordinates, crop types, baseline NDVI, and imagery URLs.
- `GET /api/farms/{farm_id}`: Retrieves details for a specific parcel.
- `GET /api/farms/{farm_id}/advisory`: Generates 3-stage localized advisory in requested language.
- `GET /api/farms/{farm_id}/observations`: Returns 20-day historical NDVI observations.
- `GET /api/farms/{farm_id}/weather`: Returns 3-day agro-meteorological outlook.
- `GET /api/farms/{farm_id}/satellite-image`: Direct stream of live Sentinel-2 true-color imagery.

#### `backend/app/api/routes/health.py`
System diagnostics and safe connectivity verification:
- `GET /api/health`: Overall service uptime and active operational mode.
- `GET /api/health/db`: Non-destructive Supabase PostgREST connection probe (zero credential leakage).
- `GET /api/health/sentinel`: Diagnostic check of Copernicus Sentinel Hub OAuth2 token acquisition.

### Business Logic & Service Layer

#### `backend/app/services/twilio_service.py`
Telephony abstraction layer:
- `send_sms(to_number, message_body, language)`: Sends live SMS via Twilio Client or simulates transmission.
- `place_voice_call(to_number, script_text, language)`: Places live IVR call or simulates voice readout.
- `generate_twiml(script_text, language)`: Constructs standard TwiML voice response XML.
- `generate_twiml_sms(message_body)`: Constructs standard TwiML messaging response XML.
- `synthesize_speech(text, language)`: Splits text into natural sentence clauses and streams regional MP3 audio.

#### `backend/app/services/sentinel_service.py`
Copernicus Sentinel-2 satellite imagery client:
- `get_access_token()`: Fetches and caches OAuth2 Bearer tokens with preemptive 60-second refresh.
- `fetch_live_satellite_image(farm_id)`: Issues Process API Evalscript requests for 10m L2A imagery.
- Implements graceful fallback to local cached assets during external API latency.

#### `backend/app/services/supabase_service.py`
Non-blocking PostgreSQL database integration:
- `verify_connection()`: Performs zero-leakage PostgREST schema verification.
- Queries registered farm parcels, sensor observations, and advisory logs.

#### `backend/dispatch_advisory.py`
Standalone CLI script for headless, browser-free low-bandwidth dispatch. Supports `--to`, `--channel`, `--farm`, `--lang`, and `--message` flags with UTF-8 console output.

### Pydantic Domain Schemas
- [backend/app/schemas/farm.py](file:///c:/Earthworm/backend/app/schemas/farm.py): `FarmBase`, `FarmResponse`, `FarmListResponse`.
- [backend/app/schemas/advisory.py](file:///c:/Earthworm/backend/app/schemas/advisory.py): `AdvisoryResponse`, `ObservationPoint`, `ObservationsResponse`, `WeatherDay`, `WeatherResponse`.

### Automated Pytest Suite
Located in [backend/tests/](file:///c:/Earthworm/backend/tests/):
- `test_communications.py`: Validates status endpoint, SMS simulation, IVR call generation, unified low-bandwidth dispatch, incoming call/SMS webhooks, and TwiML rendering (7 tests).
- `test_farms.py`: Tests farm listings, advisory localization, NDVI observations, and weather endpoints (8 tests).
- `test_health.py`: Validates health checks and route 404 handlers (4 tests).
- `test_sentinel.py`: Validates Sentinel Hub diagnostics and image serving (3 tests).
- `test_supabase.py`: Tests credential safety and mock connection states (5 tests).
- `test_vercel.py`: Validates serverless entrypoint routing (5 tests).
- **Total: 32 Automated Tests Passing.**

---

## 8. Copernicus Sentinel Hub Live Satellite Integration

### OAuth2 Client Credentials & Token Caching
Sentinel Hub authentication utilizes OAuth2 Client Credentials (`POST https://services.sentinel-hub.com/oauth/token`):
1. **Credentials**: `SENTINEL_CLIENT_ID` and `SENTINEL_CLIENT_SECRET` configured in `backend/.env`.
2. **Token Lifecycle**: Bearer tokens are cached in memory (`_access_token`) with expiration timestamps (`_token_expires_at`).
3. **Preemptive Refresh**: When remaining lifetime drops below 60 seconds, tokens are refreshed automatically.

### Process API & True-Color Evalscript
Imagery requests submit an inline JavaScript Evalscript to `POST https://services.sentinel-hub.com/api/v1/process`:
```javascript
//VERSION=3
function setup() {
  return {
    input: ["B04", "B03", "B02"],
    output: { bands: 3 }
  };
}
function evaluatePixel(sample) {
  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
}
```
- Multi-spectral bands: **B04 (Red)**, **B03 (Green)**, **B02 (Blue)** at 10-meter ground resolution.
- Reflectance boosted by a 2.5 factor to produce vivid, true-color visible composites.
- Requests enforce `maxCloudCoverage: 30%` on Sentinel-2 Level-2A bottom-of-atmosphere data.

### Regional Bounding Boxes & Dynamic Fallbacks
- **Mandya, Karnataka**: `[76.85, 12.48, 76.92, 12.55]` (Cauvery basin paddy plots)
- **Ludhiana, Punjab**: `[75.80, 30.85, 75.92, 30.95]` (Wheat cultivation belt)
- **Varanasi, Uttar Pradesh**: `[82.95, 25.28, 83.05, 25.38]` (Gangetic mustard plots)
- **Nashik, Maharashtra**: `[73.75, 19.95, 73.88, 20.08]` (Deccan onion horticulture)
- **Fallback**: Network errors or rate limits gracefully serve cached assets from `frontend/assets/{farm_id}.jpg`.

---

## 9. In-Depth Supabase Integration Architecture

### Non-Blocking Hybrid Storage Design
Earthworm guarantees 100% application uptime regardless of database connectivity:
- If Supabase credentials are configured and valid, the system reads and writes to PostgreSQL.
- If credentials are absent, invalid, or experiencing downtime, the system transitions to in-memory fixtures without crashing or throwing 500 errors.

### PostgreSQL Database Schema (DDL)
```sql
CREATE TABLE IF NOT EXISTS farms (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    state VARCHAR(128) NOT NULL,
    crop VARCHAR(128) NOT NULL,
    area_acres NUMERIC(6, 2) NOT NULL,
    baseline_ndvi NUMERIC(4, 2) NOT NULL,
    coordinates JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS observations (
    id BIGSERIAL PRIMARY KEY,
    farm_id VARCHAR(64) REFERENCES farms(id),
    date DATE NOT NULL,
    ndvi NUMERIC(4, 2) NOT NULL,
    anomaly VARCHAR(32) DEFAULT 'normal'
);

CREATE TABLE IF NOT EXISTS advisories (
    id BIGSERIAL PRIMARY KEY,
    farm_id VARCHAR(64) REFERENCES farms(id),
    language VARCHAR(8) NOT NULL,
    notice TEXT NOT NULL,
    meaning TEXT NOT NULL,
    action TEXT NOT NULL,
    sms_preview VARCHAR(160) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Connection Verification & Safe Probing
The probe at `GET /api/health/db` tests database accessibility via PostgREST schema verification without modifying data or exposing keys in response payloads or error logs.

---

## 10. Deployment & Execution Instructions

### Local Development & CLI Execution

1. **Activate Virtual Environment**:
   ```powershell
   cd c:\Earthworm\backend
   .\.venv\Scripts\Activate.ps1
   ```

2. **Start the FastAPI Development Server**:
   ```powershell
   uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
   ```

3. **Dispatch Low-Bandwidth Advisory via CLI (Zero Browser Needed)**:
   ```powershell
   python dispatch_advisory.py --to "+919731803808" --channel both --lang kn --farm mandya
   ```

4. **Verify Application in Browser**:
   - Web Dashboard: [http://127.0.0.1:8080/](http://127.0.0.1:8080/)
   - Swagger Documentation: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
   - Telephony Status: [http://127.0.0.1:8080/api/communications/status](http://127.0.0.1:8080/api/communications/status)

### Automated Testing
Execute all 32 automated tests across health, farms, Sentinel Hub, Supabase, Vercel, and low-bandwidth communications:
```powershell
pytest -v
```

### Vercel Serverless Production Deployment
Earthworm is pre-configured for zero-configuration serverless deployment to **Vercel**:
- [vercel.json](file:///c:/Earthworm/vercel.json) routes `/api/*` requests to the Python serverless entrypoint at `/api/index.py`.
- Static files at root `/` and `/frontend/*` are served directly via Vercel's global Edge CDN.
- GitHub Repository: [https://github.com/neerajp-10/gcemHacks5.0](https://github.com/neerajp-10/gcemHacks5.0)
