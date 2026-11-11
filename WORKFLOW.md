# 🌍 Earthworm | Complete Technical Workflow, Architecture & Implementation Guide

> **Satellite-Powered Early-Warning and Explainable Crop Advisory for Smallholder Farmers**  
> *Targeted at Smallholder Paddy Farmers in Mandya, Karnataka & Pan-India Demo Parcels*

---

## 📋 Table of Contents
1. [Project Overview & Core Philosophy](#1-project-overview--core-philosophy)
   - [The Smallholder Reality](#the-smallholder-reality)
   - [Earthworm's Core Pillars](#earthworms-core-pillars)
2. [End-to-End System Workflow](#2-end-to-end-system-workflow)
   - [Complete Architectural Workflow Diagram](#complete-architectural-workflow-diagram)
   - [Data Lifecycle & Subsystems](#data-lifecycle--subsystems)
3. [Decoupled Agronomic Advice Architecture](#3-decoupled-agronomic-advice-architecture)
   - [Brief Modal Summary vs. Deep Explanatory Part](#brief-modal-summary-vs-deep-explanatory-part)
   - [Copernicus Sentinel-2 Biophysical Reflectance Physics](#copernicus-sentinel-2-biophysical-reflectance-physics)
   - [Calibrated Canopy Reflectance Vigor Gauge](#calibrated-canopy-reflectance-vigor-gauge)
   - [Subterranean Root-Zone Hydrology & Soil Percolation](#subterranean-root-zone-hydrology--soil-percolation)
   - [Differential Agronomic Hypotheses & Probabilities](#differential-agronomic-hypotheses--probabilities)
   - [4-Stage Time-Sensitive Action Plan](#4-stage-time-sensitive-action-plan)
4. [Low-Bandwidth Rural Agri-Telephony Subsystem](#4-low-bandwidth-rural-agri-telephony-subsystem)
   - [Core Principle: Decoupled Web & Cellular Telephony](#core-principle-decoupled-web--cellular-telephony)
   - [Outbound Cellular SMS Advisory (160-Char Budget)](#outbound-cellular-sms-advisory-160-char-budget)
   - [Outbound Automated IVR Voice Phone Calls](#outbound-automated-ivr-voice-phone-calls)
   - [Headless Background Dispatcher CLI (`dispatch_advisory.py`)](#headless-background-dispatcher-cli-dispatch_advisorypy)
   - [Two-Way Low-Bandwidth Helpline Webhooks](#two-way-low-bandwidth-helpline-webhooks)
     - [Missed Call / IVR Helpline (`/api/communications/incoming-call`)](#missed-call--ivr-helpline)
     - [Inbound SMS Advisory Gateway (`/api/communications/incoming-sms`)](#inbound-sms-advisory-gateway)
   - [Multi-Lingual Neural Voice Synthesis Engine](#multi-lingual-neural-voice-synthesis-engine)
   - [Twilio Provider Credentials & Dual-Mode Telephony](#twilio-provider-credentials--dual-mode-telephony)
5. [7 Vernacular Indian Languages & Strict Native Isolation](#5-7-vernacular-indian-languages--strict-native-isolation)
   - [Language Matrix & Regional Dialects](#language-matrix--regional-dialects)
   - [100% Native Language Isolation Architecture](#100-native-language-isolation-architecture)
   - [Unified Translation & Deep Advice Profiles](#unified-translation--deep-advice-profiles)
6. [Responsive Multi-Device Interface Architecture](#6-responsive-multi-device-interface-architecture)
   - [Automatic Viewport Detection & Dynamic Adaptation](#automatic-viewport-detection--dynamic-adaptation)
   - [Desktop 2-Column Workstation Dashboard](#desktop-2-column-workstation-dashboard)
   - [Desktop 2-Column Explanatory Advice Workspace](#desktop-2-column-explanatory-advice-workspace)
   - [Mobile Ergonomic Single-Column Stack & Bottom Navigation](#mobile-ergonomic-single-column-stack--bottom-navigation)
   - [Persistent Manual Interface Mode Toggle](#persistent-manual-interface-mode-toggle)
7. [Professional Visual Design & Dual Theme Engine](#7-professional-visual-design--dual-theme-engine)
   - [Executive Mineral Sage Slate Canvas (`#E2EAE4`)](#executive-mineral-sage-slate-canvas-e2eae4)
   - [Space-to-Soil Dark Command Console (`#0B140F`)](#space-to-soil-dark-command-console-0b140f)
   - [1-Click Theme Switcher Engine](#1-click-theme-switcher-engine)
8. [High-Precision Satellite & Rhizosphere Intro Screen](#8-high-precision-satellite--rhizosphere-intro-screen)
   - [Copernicus Sentinel-2 Spacecraft Model](#copernicus-sentinel-2-spacecraft-model)
   - [Volumetric Multispectral Scanning Beam & Reticle](#volumetric-multispectral-scanning-beam--reticle)
   - [Stratified Soil Cross-Section & Rhizosphere Roots](#stratified-soil-cross-section--rhizosphere-roots)
   - [Peristaltic Earthworm Mascot & Soil Aeration](#peristaltic-earthworm-mascot--soil-aeration)
   - [Dynamic Telemetry Progression & Replay Engine](#dynamic-telemetry-progression--replay-engine)
9. [Advanced Satellite Parcel Inspector](#9-advanced-satellite-parcel-inspector)
   - [5 Multispectral Satellite Layers](#5-multispectral-satellite-layers)
   - [Agronomic Significance & Interactive Visualizer](#agronomic-significance--interactive-visualizer)
10. [Manual Land Boundary Marking & Dynamic Acreage Subsystem](#10-manual-land-boundary-marking--dynamic-acreage-subsystem)
    - [Farmer-Centric Boundary Delineation Workflow](#farmer-centric-boundary-delineation-workflow)
    - [Live Geodesic Acreage & Perimeter Math (WGS84 Spherical Shoelace)](#live-geodesic-acreage--perimeter-math-wgs84-spherical-shoelace)
    - ["GPS My Spot" Geolocation Integration](#gps-my-spot-geolocation-integration)
    - [Draggable Boundary Pins & Real-Time Geometry](#draggable-boundary-pins--real-time-geometry)
    - [Save Parcel Modal & Cadastral Attributes](#save-parcel-modal--cadastral-attributes)
    - [Dual-Layer Persistence (LocalStorage + REST API)](#dual-layer-persistence-localstorage--rest-api)
    - [Quick-Toggle Custom Parcel Badges](#quick-toggle-custom-parcel-badges)
11. [Libraries & Technologies Used](#11-libraries--technologies-used)
    - [Backend Python Dependencies](#backend-python-dependencies)
    - [Frontend Frameworks & Libraries](#frontend-frameworks--libraries)
12. [Detailed Python Script & Codebase Documentation](#12-detailed-python-script--codebase-documentation)
    - [Entrypoints & Server Configuration](#entrypoints--server-configuration)
    - [API Route Handlers (FastAPI)](#api-route-handlers-fastapi)
    - [Business Logic & Service Layer](#business-logic--service-layer)
    - [Pydantic Domain Schemas](#pydantic-domain-schemas)
    - [Automated Pytest Suite (34 Passed)](#automated-pytest-suite-34-passed)
13. [Copernicus Sentinel Hub Live Satellite Integration](#13-copernicus-sentinel-hub-live-satellite-integration)
    - [OAuth2 Client Credentials & Token Caching](#oauth2-client-credentials--token-caching)
    - [Process API & True-Color Evalscript](#process-api--true-color-evalscript)
    - [Regional Bounding Boxes & Dynamic Fallbacks](#regional-bounding-boxes--dynamic-fallbacks)
14. [In-Depth Supabase Integration Architecture](#14-in-depth-supabase-integration-architecture)
    - [Non-Blocking Hybrid Storage Design](#non-blocking-hybrid-storage-design)
    - [PostgreSQL Database Schema (DDL)](#postgresql-database-schema-ddl)
    - [Connection Verification & Safe Probing](#connection-verification--safe-probing)
15. [Deployment, Multi-Target Sync & Production Execution](#15-deployment-multi-target-sync--production-execution)
    - [Local Development & CLI Execution](#local-development--cli-execution)
    - [Automated Testing Execution](#automated-testing-execution)
    - [Six-Target Distribution Synchronization](#six-target-distribution-synchronization)
    - [Vercel Serverless Production Deployment](#vercel-serverless-production-deployment)

---

## 1. Project Overview & Core Philosophy

**Earthworm** bridges the critical "last-mile" barrier separating spaceborne Earth observation (Copernicus Sentinel-2 multispectral sensors, Open-Meteo agro-meteorological forecasting) and smallholder farmers cultivating 0.5 to 2-acre parcels across rural India.

### The Smallholder Reality
Traditional commercial agri-tech platforms fail rural farmers due to three chronic disconnects:
1. **Bandwidth Poverty & Feature Phone Ownership**: Smallholders in remote agrarian belts frequently rely on basic 2G/3G keypad feature phones without reliable mobile data connections. Requiring farmers to download heavy web or mobile applications ensures total exclusion.
2. **The "Black Box" Trust Deficit**: Opaque AI recommendations (*"Spray 250ml fungicide on Tuesday"*) generate distrust because they do not explain *what* was detected, *why* it matters, or *how* the conclusion was reached.
3. **Linguistic & Jargon Barriers**: Advisories delivered in technical English or academic terminology are inaccessible to vernacular-speaking farmers.

### Earthworm's Core Pillars
- **Decoupled Low-Bandwidth Delivery**: Advisories are delivered directly over cellular telecom networks (GSM/PSTN) via 160-character cellular SMS and automated IVR voice phone calls straight to the farmer's physical phone number. Zero internet access, smartphones, or web pages are required on the farmer's end.
- **Two-Tier Explainable Agronomy**:
  1. **Quick Brief Modal**: High-impact, immediate takeaways (Notice $\rightarrow$ Meaning $\rightarrow$ Action) for rapid field decisions.
  2. **Dedicated Explanatory Part (`view-advice`)**: Full scientific diagnostics, canopy biophysical physics, calibrated vigor scales, root-zone hydrology models, 3 differential agronomic hypotheses, and 4-step precision checklists.
- **Comprehensive 7-Language Vernacular Support**: Native UI, audio speech streaming, SMS segments, and voice call readouts with **100% native language isolation** across **English**, **Kannada (ಕನ್ನಡ)**, **Hindi (हिन्दी)**, **Telugu (తెలుగు)**, **Tamil (தமிழ்)**, **Marathi (मराठी)**, and **Bengali (বাংলা)**.
- **Adaptive Multi-Device Interface**: Seamlessly switches between an expansive 2-column Desktop Workstation and a single-handed Mobile Stack.
- **Executive Glare-Free Design**: Professional mineral-sage slate canvas with instant 1-click toggle to a high-contrast Space-to-Soil Dark Command Console.

---

## 2. End-to-End System Workflow

### Complete Architectural Workflow Diagram

```
+-------------------------------------------------------------------------------------------------------+
|                                1. DATA ACQUISITION & REMOTE SENSING                                   |
| - European Space Agency (ESA) Copernicus Sentinel-2 MSI (10m Multi-Spectral: B02, B03, B04, B08)     |
| - Sentinel Hub Process API (services.sentinel-hub.com) with true-color BOA L2A Evalscript             |
| - Open-Meteo Regional Agro-Meteorological Forecasts (Rainfall, Relative Humidity, Soil Temp, ET)      |
+---------------------------------------------------+---------------------------------------------------+
                                                    |
                                                    v
+-------------------------------------------------------------------------------------------------------+
|                               2. AGRONOMIC ENGINE & ANOMALY DETECTION                                 |
| - Multispectral Vegetation Indices:                                                                  |
|   * NDVI = (NIR - Red) / (NIR + Red)               [Canopy Vigor & Biomass Density]                   |
|   * CIR = NIR False Color Composite                [Leaf Cellular Structure & Health]                 |
|   * NDWI = (NIR - SWIR) / (NIR + SWIR)             [Canopy Water Content & Moisture Stress]           |
|   * SAR Proxy = Dual-Pol Backscatter Reflectance   [Root-Zone Soil Dielectric Wetness]                |
| - 10-Day Rolling Temporal Baseline Comparison (Flags early-stage water/nutrient stress anomalies)    |
| - Two-Tier Explainable Engine: Brief 3-Stage Modal + Deep Explanatory Agronomic Part                  |
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
| - Adaptive Viewport (Desktop 2-Col / Mobile 1-Col) |  | - Direct GSM/PSTN Cellular Delivery           |
| - Dual Theme: Executive Sage vs Space Dark Console |  | - 160-character vernacular SMS text message   |
| - Multi-Layer Parcel Inspector (5 Bands)           |  | - Automated inbound/outbound IVR voice calls  |
| - Dedicated Explanatory Advice Screen (`view-adv`) |  | - Zero web browser, zero app, zero internet   |
| - 4-Card KPI Strip & Calibrated Vigor Gauge        |  | - Standalone CLI: dispatch_advisory.py        |
| - 3 Differential Hypotheses with Probabilities     |  | - Missed Call / IVR Dial-in Helpline          |
| - 7-Language Native Switcher (0 cross-fallback)    |  | - Two-Way Inbound SMS Query Gateway           |
+----------------------------------------------------+  +-----------------------------------------------+
```

---

## 3. Decoupled Agronomic Advice Architecture

A key advancement in Earthworm is the architectural separation between the **Brief Summary Modal** and the **Dedicated Explanatory Advice Screen (`view-advice`)**:

```
+---------------------------------------------------------------------------------------+
|                                    USER INTERACTION FLOW                              |
|                                                                                       |
|   [ Dashboard Action Tile ] -----> Taps "View Advice" / Bottom Sheet Modal            |
|                                    └──> BRIEF SUMMARY MODAL                           |
|                                         ├── Notice (Observation)                      |
|                                         ├── Meaning (Interpretation)                  |
|                                         └── Action (Today's 3 Practical Steps)        |
|                                                                                       |
|   [ Advice Tab / "View Full Advice" ] --> Navigates to dedicated view:                |
|                                    └──> EXPLANATORY ADVICE PART (#view-advice)        |
|                                         ├── Section 1: Satellite Vigor Analysis       |
|                                         ├── Section 2: Root-Zone & Field Causes       |
|                                         ├── Section 3: 4-Step Field Action Plan       |
|                                         └── Section 4: Handset Dispatch (SMS/Voice)   |
+---------------------------------------------------------------------------------------+
```

### Brief Modal Summary vs. Deep Explanatory Part
- **Brief Modal (`#adviceModal`)**: Built for rapid field triage. Presents 3 concise bulleted items (`Notice`, `Meaning`, `Action`), current NDVI value, and quick voice readout. Does not overwhelm farmers or field workers with dense physics.
- **Deep Explanatory Part (`#view-advice`)**: Activated by clicking the dedicated **Advice** navigation tab or the **"View Full Advice"** button. Contains complete scientific rationale, biophysical physics, calibrated vigor scales, hydrological models, hypotheses, and an actionable 4-step protocol.

### Copernicus Sentinel-2 Biophysical Reflectance Physics
Section 1 of the explanatory view breaks down the exact optical physics:
- **Optical Instrument**: Copernicus Sentinel-2 Multispectral Instrument (MSI Level-2A) at 10-meter ground resolution.
- **Mathematical Formula**:
  $$\text{NDVI} = \frac{\text{NIR (Band 8, 842nm)} - \text{Red (Band 4, 665nm)}}{\text{NIR (Band 8, 842nm)} + \text{Red (Band 4, 665nm)}}$$
- **Plant Physiology Explanation**: Healthy, turgid crop leaves contain water-filled spongy mesophyll cells reflecting $40\%\text{--}50\%$ of incoming Near-Infrared radiation, while chlorophyll-a/b pigments absorb visible Red light. When root-zone moisture declines, leaf guard cells close stomata, dropping cellular turgor and compressing mesophyll cell walls, causing NIR reflectance to dip days before visible human eye yellowing.

### Calibrated Canopy Reflectance Vigor Gauge
Features an interactive visual slider mapping live NDVI against calibrated crop baselines:
- `0.0` Water / Fallow $\rightarrow$ `0.3` Sparse Canopy $\rightarrow$ `▲ Current: 0.58` $\rightarrow$ `▲ Target: 0.70` $\rightarrow$ `0.9` Dense Vegetative Canopy.
- Includes pin tracking that dynamically repositions based on the parcel's observed NDVI.

### Subterranean Root-Zone Hydrology & Soil Percolation
Section 2 provides soil-depth analysis:
- Profiles topsoil (0–15 cm) vs subsoil (15–40 cm) percolation rates.
- Evaluates evapotranspiration (ET: ~4.2 mm/day) against soil water holding capacity.
- Explains why elevation gradients (e.g. 1.8° ridge slope) accelerate moisture depletion.

### Differential Agronomic Hypotheses & Probabilities
Presents three ranked agronomic hypotheses with probabilistic confidence scores and field confirmation steps:
1. **Hypothesis 1 (65% Probability)**: Sub-surface water drainage and micro-slope run-off. *Field Check: Dig 10cm test hole at 3 ridge points; check if soil crumbles without clumping.*
2. **Hypothesis 2 (25% Probability)**: Drip irrigation emitter salt blockage or pressure differential. *Field Check: Inspect emitter flow rate on terminal lateral lines.*
3. **Hypothesis 3 (10% Probability)**: Localized fungal / root-zone disease onset. *Field Check: Inspect lower leaf collar for water-soaked lesions or early blast spots.*

### 4-Stage Time-Sensitive Action Plan
Section 3 details an operational timetable:
- **Step 1 (Immediate / Tomorrow Morning 7:30–9:00 AM)**: Ground parcel inspection and topsoil moisture feel-test.
- **Step 2 (Days 1–2)**: Evening irrigation run adjustments to minimize evaporative loss.
- **Step 3 (Days 2–3)**: Lateral line flushing and acid/salt emitter de-clogging.
- **Step 4 (Day 5)**: Satellite overpass verification against next Sentinel-2 5-day cycle.

---

## 4. Low-Bandwidth Rural Agri-Telephony Subsystem

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
1. Smallholder farmers can give a **missed call** or dial the Earthworm helpline number (`1800-180-1551`).
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

## 5. 7 Vernacular Indian Languages & Strict Native Isolation

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

### 100% Native Language Isolation Architecture
To eliminate cross-language contamination (e.g. Hindi paragraphs rendering under Kannada headers):
- Regional packs are partitioned into independent data structures:
  1. `TRANSLATIONS`: UI shell labels, buttons, and navigation terms.
  2. `LANGUAGE_OVERRIDES`: Regional farm metadata (crop names, plot titles, advisory summaries, weather reports, and SMS previews).
  3. `DEEP_ADVICE_TRANSLATIONS`: In-depth scientific biophysical explanations, soil hydrology models, 3 differential hypotheses, and 4-step action plans.
- **Strict Verification**: Kannada (`kn`), Telugu (`te`), Tamil (`ta`), Marathi (`mr`), and Bengali (`bn`) maintain 100% native vocabulary across all 4 pilot regions (*Mandya*, *Ludhiana*, *Varanasi*, *Nashik*) with zero Devanagari character contamination in Dravidian or Bengali datasets.

---

## 6. Responsive Multi-Device Interface Architecture

Earthworm features an adaptive, dual-layout design system catering to both desktop workstations and mobile field devices:

### Automatic Viewport Detection & Dynamic Adaptation
- On initial page load, the application inspects `window.innerWidth`:
  - $\ge 1024\text{px}$ (laptops & desktop displays) $\rightarrow$ automatically activates **Desktop Mode**.
  - $< 1024\text{px}$ (smartphones & tablets) $\rightarrow$ automatically activates **Mobile Mode**.
- Window resize listeners dynamically adapt the interface in real time unless the user has explicitly selected a manual mode override.
- User choices are saved in `localStorage.earthworm_view_mode`.

### Desktop 2-Column Workstation Dashboard
In Desktop Mode (`max-w-7xl mx-auto px-6 pt-20 pb-12`):
- **Top Navigation Bar (`#desktop-top-nav`)**: Displays centralized navigation pills (`Home`, `My Farm`, `Advice`) with active state highlights.
- **Left Column (7 of 12 cols, ~58% width)**:
  1. **Dynamic Live Satellite Viewer**: High-resolution `420px` height viewport with telemetry HUD, coordinate reticles, and spectral layer buttons.
  2. **Regional 3-Day Agromet Forecast**: 3 clean day cards with temperature, precipitation, and agronomist recommendations.
  3. **Kisan Call Centre & Mobile SMS Advisory Dispatch**: Direct toll-free helpline button and cellular SMS dispatch card.
- **Right Column (5 of 12 cols, ~42% width)**:
  1. **Farm / Region Selector**: Pilot region pills (`Mandya`, `Ludhiana`, `Varanasi`, `Nashik`) + custom parcel registration.
  2. **Agronomic Advisory Overview**: High-priority alert badge, vegetative index metric bar, "View Full Advice" button, and voice advice readout.
  3. **Three Practical Field Action Tiles**: Interactive diagnostic action steps.
  4. **Direct Cellular SMS Input Form**: Mobile number input for zero-internet SMS delivery.

### Desktop 2-Column Explanatory Advice Workspace
When viewing `#view-advice` on Desktop:
- **Top Row**: Full-width header with field switcher pills and 4-card KPI strip (`Observed NDVI`, `Crop Stage`, `Root-Zone Soil`, `72-hr Weather Risk`).
- **Left Column (7 cols)**: Satellite vigor analysis, biophysical reflectance physics, calibrated vigor gauge, and root-zone hydrology models.
- **Right Column (5 cols, sticky `lg:top-20`)**: Step-by-step 4-stage action plan with timeline badges + cellular SMS checklist dispatch and voice playback.

### Mobile Ergonomic Single-Column Stack & Bottom Navigation
In Mobile Mode (`max-w-[640px] mx-auto px-4 pt-20 pb-28`):
- Strict single-column vertical flow prevents horizontal overflow or awkward side-by-side squishing.
- Map height is constrained to `320px` for smooth touch panning.
- Floating bottom navigation bar (`#bottom-nav-bar`) provides thumb-accessible `Home`, `My Farm`, and `Advice` tabs with safe-area bottom padding (`pb-28`).
- Modals slide up as mobile bottom sheets (`rounded-t-3xl`) with backdrop blur.

### Persistent Manual Interface Mode Toggle
The header features an interactive mode toggle (`Mobile` / `Desktop`) allowing users on any screen size to preview the alternative interface layout on demand.

---

## 7. Professional Visual Design & Dual Theme Engine

To eliminate harsh white glare and deliver an enterprise-grade experience, Earthworm provides a cohesive dual-theme system:

```
+---------------------------------------------------------------------------------------+
|                                    THEME ENGINE                                       |
|                                                                                       |
|   1. EXECUTIVE SAGE THEME (Default)                                                   |
|      - App Canvas: Mineral Sage Slate (#E2EAE4)                                       |
|      - Elevated Cards: Pure White (#FFFFFF) with subtle emerald borders               |
|      - High-Contrast Text: Deep Forest Ink (#112318)                                  |
|                                                                                       |
|   2. SPACE DARK CONSOLE THEME (1-Click Toggle)                                        |
|      - App Canvas: Deep Orbital Obsidian (#0B140F)                                    |
|      - Elevated Cards: Forest Night (#122119) with glowing emerald borders            |
|      - High-Contrast Text: Mint White (#EDF5F0) & Emerald (#34D399)                   |
|                                                                                       |
|   [ Header Toggle: 🌙 / ☀️ ] ---> Persists to localStorage.earthworm_theme             |
+---------------------------------------------------------------------------------------+
```

### Executive Mineral Sage Slate Canvas (`#E2EAE4`)
- **Elimination of White Glare**: Replaces the stark white background (`#FAFAF6`) with an architectural mineral-sage slate canvas (`#E2EAE4`).
- **Tactile Card Elevation**: Floating cards (`#FFFFFF`) pop forward with soft ambient shadows (`shadow-[0_2px_12px_rgba(0,40,20,0.04)]`) and crisp borders (`rgba(0, 82, 48, 0.10)`).
- **Frosted Glassmorphism**: Header and navigation bars use frosted glass tinted with the sage tone (`rgba(226, 234, 228, 0.92)`).

### Space-to-Soil Dark Command Console (`#0B140F`)
- **Aerospace Atmosphere**: Transforms the interface into a satellite command console inspired by ESA and NASA mission rooms.
- **Deep Obsidian Surfaces**: Canvas (`#0B140F`), cards (`#122119`), and input fields (`#172A1F`).
- **Luminescent Telemetry**: NDVI scales, radar reticles, and spectral heatmaps glow with aerospace clarity.

### 1-Click Theme Switcher Engine
- Accessible via a dedicated theme button (`#theme-toggle-btn`) in the top navigation bar.
- Toggles the `.dark` CSS class on `document.documentElement` without page reload.
- Remembers user preference across sessions via `localStorage.getItem('earthworm_theme')`.

---

## 8. High-Precision Satellite & Rhizosphere Intro Screen

Earthworm features an executive splash animation screen (`#intro-splash`) connecting space telemetry to underground biological fertility:

### Copernicus Sentinel-2 Spacecraft Model
- Vector-rendered Sentinel-2 satellite orbiting smoothly at top-left:
  - Gold Multi-Layer Insulation (**MLI**) thermal foil face.
  - Titanium chassis bus with attitude control thrusters.
  - Multispectral Instrument (**MSI**) optical barrel with lens flare reflection.
  - Dual photovoltaic solar array wings with silver grid lines.
  - Phased telemetry antenna and animated green heartbeat beacon.

### Volumetric Multispectral Scanning Beam & Reticle
- Dual-band optical scan cone (NIR Band 8 842nm + Red Band 4 665nm) projecting downward to the field.
- Dynamic radar wavefronts pulsing down along the beam.
- Ground-tracking targeting reticle `[ · ]` sweeping the crop canopy with real-time coordinate coordinates.

### Stratified Soil Cross-Section & Rhizosphere Roots
- Replaces crude flat blocks with a rich geological cross-section:
  - **Topsoil & Organic Humus (0–15 cm)**: Dark nutrient-rich loam.
  - **Active Root Zone (15–35 cm)**: Aerated loam with delicate white-gold root capillaries (Rhizosphere).
  - **Subsoil & Retentive Clay (35+ cm)**: Mineral clay with subtle glowing blue capillary moisture veins.

### Peristaltic Earthworm Mascot & Soil Aeration
- Anatomically refined biological emblem:
  - 8 metameric segments with terracotta and amber shading.
  - Velvet clitellum saddle band.
  - Naturalist, friendly head profile with clean specular glint (zero cartoon googly eyes).
  - Smooth peristaltic crawling movement along an excavated burrow tunnel, leaving behind aerated micro-pores and glowing nutrient bio-particles.

### Dynamic Telemetry Progression & Replay Engine
- Synchronized progress bar with authentic satellite acquisition phases:
  1. `Calibrating Sentinel-2 MSI 10m Radiometer...`
  2. `Analyzing Canopy Reflectance & NDVI Index...`
  3. `Mapping Subterranean Root-Zone & Soil Moisture...`
  4. `Agronomic Diagnostics Ready • Entering Dashboard...`
- Replay button (`replaySplash()`) in header allows users to replay the 60fps hardware-accelerated animation anytime.

---

## 9. Advanced Satellite Parcel Inspector

The dashboard replaces static modals with the **Multispectral Satellite Parcel Inspector**, offering five analytical satellite imaging modes:

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

## 10. Manual Land Boundary Marking & Dynamic Acreage Subsystem

Smallholder farmers in India often cultivate fragmented, irregularly shaped plots where official cadastral boundaries differ from physical field bunds (*varambas* / *mees*). To give farmers direct control over their land monitoring, Earthworm features an interactive, high-precision **Manual Land Boundary Marker**.

### Farmer-Centric Boundary Delineation Workflow
1. The farmer taps the **"Mark Land"** (`ಜಮೀನು ಗುರುತಿಸಿ` / `जमीन चिह्नित करें`) button on the Copernicus Sentinel-2 satellite card header.
2. An interactive glassmorphic HUD appears with live measurements:
   - **Corner Pin Counter**: Tracks vertices placed (`0 Corners`, `3 Corners`, etc.).
   - **Live Acreage Readout**: Computes exact area in both **Acres** and **Guntas** ($1\text{ Acre} = 40\text{ Guntas}$, or Cents in southern regions).
   - **Perimeter Readout**: Computes boundary perimeter in meters or kilometers.
   - **Quick Action Controls**:
     - 📍 **GPS My Spot**: Queries device GPS coordinates to drop a pin at the farmer's current physical standing location.
     - ↩️ **Undo**: Removes the most recently placed corner pin.
     - 🗑️ **Clear**: Resets all active markers and boundary polygons.
     - 💾 **Save Land**: Prompts the modal to name and register the marked parcel.
3. The farmer clicks anywhere on the Leaflet high-resolution satellite basemap to place sequential numbered pins (Pin 1, Pin 2, Pin 3...).
4. As soon as $\ge 3$ corner points are placed, a closed emerald polygon (`#10b981`) dynamically fills the plot boundary with real-time geodesic acreage calculation.

### Live Geodesic Acreage & Perimeter Math (WGS84 Spherical Shoelace)
Standard Euclidean Cartesian math produces major distortion when calculating surface area from latitude/longitude coordinates on a spherical planet. Earthworm implements the **Spherical Polygon Excess (Shoelace) Formula** on the WGS84 Earth ellipsoid ($R = 6,378,137\text{ m}$):

$$\text{Area} = R^2 \cdot \left| \sum_{i=1}^{n} (\lambda_{i+1} - \lambda_{i-1}) \cdot \sin(\phi_i) \right| / 2$$

Where $\phi$ is latitude in radians and $\lambda$ is longitude in radians. The computed area in square meters ($m^2$) is converted into regional revenue units:
- **Acres**: $\text{Acres} = \frac{\text{Area in } m^2}{4046.8564224}$
- **Guntas**: $\text{Guntas} = (\text{Acres} - \lfloor\text{Acres}\rfloor) \times 40$
- **Hectares**: $\text{Hectares} = \frac{\text{Area in } m^2}{10000}$

Perimeter is computed by summing the Haversine great-circle distances between adjacent vertices:

$$d = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)$$

### "GPS My Spot" Geolocation Integration
For farmers walking their physical boundary bunds in the field with a smartphone or tablet:
- Tapping **"GPS My Spot"** invokes `navigator.geolocation.getCurrentPosition({ enableHighAccuracy: true })`.
- Earthworm drops a corner marker at the farmer's exact real-world coordinates and pans the satellite viewport to center on them.

### Draggable Boundary Pins & Real-Time Geometry
- Every corner pin is rendered as an interactive, draggable Leaflet marker (`draggable: true`) with a distinct numbered badge icon (`bg-emerald-600 text-white font-bold ring-2 ring-white`).
- When a farmer drags any corner marker to adjust it along a field boundary or canal, Leaflet's `drag` event triggers real-time recalculation of the polygon geometry, perimeter, and acreage without dropping new pins.

### Save Parcel Modal & Cadastral Attributes
When the farmer taps **"Save Land"**:
- Earthworm opens a dialog displaying verified boundary metrics:
  - Total Measured Acreage (e.g. `1.85 Acres (1 Ac, 34 Guntas)`).
  - Number of boundary corners & total perimeter.
- Form fields allow the farmer to specify:
  - **Parcel Name** (e.g. *"Kavitha Sugarcane Plot"*).
  - **Primary Crop** (Paddy, Sugarcane, Ragi, Cotton, Maize, Wheat, Vegetables).
  - **Survey / Khasra Number** (optional revenue record identifier).
  - **Field Notes** (soil observations, canal access, sowing date).

### Dual-Layer Persistence (LocalStorage + REST API)
To ensure reliable operation under intermittent rural internet connectivity:
1. **Local Storage (`localStorage.earthworm_custom_parcels`)**: Immediately saves parcels on the local device, guaranteeing zero latency, offline availability, and persistence across browser reloads.
2. **REST API (`POST /api/farms/custom-marker`)**: Simultaneously pushes the parcel JSON payload to the FastAPI backend, where it is indexed in-memory and ready for PostgreSQL/Supabase sync.

### Quick-Toggle Custom Parcel Badges
Saved parcels are immediately added to the bottom telemetry bar alongside default demo plots (e.g. `[Plot #142/A] [Kavitha Sugarcane Plot (1.85 Ac)]`). Clicking any custom parcel badge:
- Centers and zooms the satellite map to the parcel's bounding box.
- Renders the custom boundary polygon with popup details.
- Displays the measured acreage and crop profile.
- Provides a delete button to remove obsolete parcels.

---

## 11. Libraries & Technologies Used

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
- **Google Fonts (Outfit, Noto Sans & Inter)**: Crisp, modern typography engineered for readability across regional Indian scripts.
- **Google Material Symbols Outlined**: Intuitive agrarian, weather, and telephony iconography.

---

## 12. Detailed Python Script & Codebase Documentation

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
Exposes cadastral parcel listings, agronomic telemetry, and manual land marker persistence:
- `GET /api/farms`: Lists registered parcels with coordinates, crop types, baseline NDVI, and imagery URLs.
- `GET /api/farms/{farm_id}`: Retrieves details for a specific parcel.
- `GET /api/farms/{farm_id}/advisory`: Generates 3-stage localized advisory in requested language.
- `GET /api/farms/{farm_id}/observations`: Returns 20-day historical NDVI observations.
- `GET /api/farms/{farm_id}/weather`: Returns 3-day agro-meteorological outlook.
- `GET /api/farms/{farm_id}/satellite-image`: Direct stream of live Sentinel-2 true-color imagery.
- `POST /api/farms/custom-marker`: Saves a farmer's manually marked land parcel with boundary coordinates, crop, and acreage.
- `GET /api/farms/{farm_id}/custom-markers`: Retrieves all custom marked parcels for a specific farm region.
- `DELETE /api/farms/{farm_id}/custom-markers/{marker_id}`: Deletes a saved custom land marker.

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
- [backend/app/schemas/farm.py](file:///c:/Earthworm/backend/app/schemas/farm.py): `FarmBase`, `FarmResponse`, `FarmListResponse`, `CustomMarkerPoint`, `CustomLandMarker`.
- [backend/app/schemas/advisory.py](file:///c:/Earthworm/backend/app/schemas/advisory.py): `AdvisoryResponse`, `ObservationPoint`, `ObservationsResponse`, `WeatherDay`, `WeatherResponse`.

### Automated Pytest Suite (34 Passed)
Located in [backend/tests/](file:///c:/Earthworm/backend/tests/):
- `test_communications.py`: Validates status endpoint, SMS simulation, IVR call generation, unified low-bandwidth dispatch, incoming call/SMS webhooks, and TwiML rendering (7 tests).
- `test_farms.py`: Tests farm listings, advisory localization, NDVI observations, weather endpoints, and custom land marker lifecycle (10 tests).
- `test_health.py`: Validates health checks and route 404 handlers (4 tests).
- `test_sentinel.py`: Validates Sentinel Hub diagnostics and image serving (3 tests).
- `test_supabase.py`: Tests credential safety and mock connection states (5 tests).
- `test_vercel.py`: Validates serverless entrypoint routing (5 tests).
- **Total: 34 Automated Tests Passing.**

---

## 13. Copernicus Sentinel Hub Live Satellite Integration

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

## 14. In-Depth Supabase Integration Architecture

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

## 15. Deployment, Multi-Target Sync & Production Execution

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

### Automated Testing Execution
Execute all 34 automated tests across health, farms, Sentinel Hub, Supabase, Vercel, and low-bandwidth communications:
```powershell
backend\.venv\Scripts\pytest backend\tests -v
```

### Six-Target Distribution Synchronization
To support direct execution, static web servers, and Vercel edge deployment without desynchronization, Earthworm maintains byte-for-byte consistency across 6 frontend targets:
1. `c:\Earthworm\frontend\index.html` (Primary master template)
2. `c:\Earthworm\frontend\code.html`
3. `c:\Earthworm\index.html` (Root Vercel edge entrypoint)
4. `c:\Earthworm\code.html`
5. `c:\Earthworm\backend\index.html` (FastAPI static mount)
6. `c:\Earthworm\backend\frontend\index.html`

### Vercel Serverless Production Deployment
Earthworm is pre-configured for zero-configuration serverless deployment to **Vercel**:
- [vercel.json](file:///c:/Earthworm/vercel.json) routes `/api/*` requests to the Python serverless entrypoint at `/api/index.py`.
- Static files at root `/` and `/frontend/*` are served directly via Vercel's global Edge CDN.
- GitHub Repository: [https://github.com/neerajp-10/gcemHacks5.0](https://github.com/neerajp-10/gcemHacks5.0)
