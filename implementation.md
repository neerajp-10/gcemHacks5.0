# Implementation Plan --- Earthworm (Backend First)

## 1. Mission

Build a reliable, explainable early-warning advisory backend for
smallholder paddy farmers in Mandya, Karnataka, India. The backend must
be completed and tested before the frontend is built. The frontend will
be developed separately using Google Stitch and React, then integrated
only after both sides are ready.

Read `context.md` before changing the project. It is the source of truth
for product goals, data integrity, language support, low-bandwidth
requirements, SMS/voice simulation, and project constraints.

## 2. Mandatory workflow

**Build order:** 1. Backend only. 2. Frontend only, using the agreed API
contract. 3. Integrate frontend and backend. 4. Test the complete
application and prepare the demo.

Until the backend phase is complete: - Work only in `backend/`. - Do not
scaffold, create, or modify a frontend. - Do not create React/Vite
files. - Do not start Stitch integration. - Do not claim frontend
integration has been tested.

## 3. Agent working rules

1.  Inspect the current workspace and environment before editing
    anything.
2.  Do not overwrite existing work without understanding it.
3.  Work in small phases. Run tests after each meaningful change.
4.  Explain important choices briefly in plain language; the project
    owner is a beginner, but wants practical progress rather than long
    lessons.
5.  Do not fabricate real satellite/weather/soil observations,
    historical records, benchmarks, accuracy scores, delivery
    confirmations, yield gains, or water savings.
6.  Use clearly labelled demo fixtures when real data is not yet
    connected.
7.  Every observation or derived value should preserve source,
    timestamp, status and quality information when available.
8.  Keep credentials on the server in environment variables. Never put
    secrets in frontend code, source control, logs, prompts, or
    documentation. Add `.env` to `.gitignore`; use `.env.example` with
    placeholders only.
9.  External APIs must not be required for the backend to start or for
    its basic demo endpoints to work.
10. Keep the implementation small enough for a 24-hour hackathon. Prefer
    a tested vertical slice to broad unfinished functionality.
11. Preserve working code and use Git checkpoints if Git is available.
12. Report exact commands used to run and test the backend, plus actual
    test results. Never claim a test passed unless it was run.

## 4. Backend structure

Inspect the workspace first. If no suitable backend structure exists,
propose and create something close to:

``` text
backend/
  app/
    main.py
    config.py
    api/
      routes/
    schemas/
    models/
    services/
      satellite/
      weather/
      soil/
      advisory/
      communications/
    repositories/
    data/
      demo/
  tests/
  requirements.txt
  .env.example
  .gitignore
  README.md
```

Keep this structure practical. Avoid unnecessary layers and
dependencies. If the workspace already has a good structure, adapt
rather than forcing this exact layout.

Use: - Python - FastAPI - Pydantic for request/response validation -
Pytest and FastAPI's test client (or an appropriate compatible test
setup) - Supabase/PostgreSQL integration only after the API contract and
demo flow are stable enough

Do not add a machine-learning framework unless a verified need appears.

## 5. Phase 0 --- Inspect and report

Before writing code: - Inspect the current workspace, existing files,
Git state and Python environment. - Determine whether a backend already
exists. - Check available Python version and dependency tooling. -
Report blockers and the proposed backend-only task sequence. - Do not
create frontend files or integrate external services at this stage.

## 6. Phase 1 --- Minimal runnable backend

Implement only the foundation: - A FastAPI application. -
`GET /api/health` with a small structured response. - Configuration
loading that is safe when optional environment variables are absent. - A
documented way to run the server locally. - A minimal test for the
health endpoint. - Basic error handling. - A `.gitignore` and
`.env.example` if not already present.

Acceptance criteria: - The application starts successfully. - The health
endpoint returns the expected response. - The test runs and passes. - No
real credentials are required. - No frontend files are created.

After testing, report exact run/test commands and wait for the next
phase unless the user explicitly asks to continue.

## 7. Phase 2 --- API contract and domain schemas

Create typed Pydantic schemas and document the initial API contract
before building complex logic. Keep schemas small and consistent.

### Farm

Possible fields: - `id` - `name` - `district` - `state` - `crop` -
`crop_season` (nullable if unknown) - `growth_stage` (nullable if
unknown) - `location` or geometry (only if valid data exists) -
`data_status` (`observed`, `derived`, `estimated`, `simulated`, `demo`
as appropriate)

### Observation

Possible fields: - `id` - `farm_id` - `observed_at` - `retrieved_at` -
`source` - `observation_type` (`satellite`, `weather`, `soil`) -
`metric` (e.g. NDVI, rainfall, temperature) - `value` - `unit` -
`quality_flags` - `status` (`observed`, `derived`, `estimated`,
`simulated`, `demo`) - `method` or calculation description where
relevant

### Baseline / benchmark

Possible fields: - `id` - `farm_id` or comparison group/region -
`metric` - `period_start` - `period_end` - crop/season/growth-stage
context when known - summary value/statistics - `source` -
`sample_count` - `method` - `limitations` - `status`

### Advisory

Possible fields: - `id` - `farm_id` - `created_at` - `language` -
`severity` (with a defined meaning) - `headline` - `observations_used` -
`possible_interpretation` - `recommended_next_step` -
`uncertainty_note` - `data_status`

### Communication preview/delivery

Possible fields: - `id` - `advisory_id` - `language` - `channel` (`sms`
or `voice`) - `preview_text` - `status` (use `preview_only` or
`simulated` for simulations) - `created_at` - real provider message IDs
only if an actual provider response exists

Do not implement every optional field immediately. Agree on the minimal
contract and keep it documented.

## 8. Phase 3 --- Demo data and core endpoints

Create small, explicit demo fixtures. Every synthetic item must be
marked as demo/simulated and must not be presented as real satellite or
field data.

Suggested endpoints: - `GET /api/health` - `GET /api/farms` -
`GET /api/farms/{farm_id}` - `GET /api/farms/{farm_id}/observations` -
`GET /api/farms/{farm_id}/history` -
`GET /api/farms/{farm_id}/baseline` -
`GET /api/farms/{farm_id}/advisory` -
`GET /api/farms/{farm_id}/communications/preview?language=kn&channel=sms`

Endpoint names can be refined, but once agreed, document them and keep
response schemas stable for the future frontend.

Add tests for: - successful requests, - unknown farm IDs, -
empty/missing observations, - malformed or unsupported parameters, -
correct demo/provenance labels.

## 9. Phase 4 --- Historical trends and benchmarks

Support historical comparisons in the API, but only compute a real
benchmark after verifying that the underlying data is suitable.

Keep distinct: 1. Same-field history: dated observations for the
selected field. 2. Seasonal baseline: observations for a compatible
season/crop stage, when available. 3. Regional benchmark: a documented
comparison group, only when the source and methodology support it. 4.
District yield statistics: regional context only, not evidence of
individual-field performance or intervention impact.

Rules: - Compare like with like as far as the available data permits. -
Record the period, source, method, sample count and limitations. - Do
not compare incompatible crop stages, seasons, cloud conditions or
processing products without a documented method. - If the baseline is
missing or insufficient, return an explicit unavailable status and a
reason. Do not invent a benchmark. - Demo baselines must be clearly
labelled as demo data. - Add tests for missing baselines, insufficient
samples and valid comparisons.

## 10. Phase 5 --- Explainable advisory rules

Implement transparent, testable rules in the backend. Do not claim they
are scientifically validated unless appropriate evidence supports that
claim.

Every advisory should include: - evidence used, - observation
timestamps, - possible interpretation, - practical next check/action, -
uncertainty/data-quality note, - data status and sources.

Example of cautious logic: a declining vegetation indicator alongside
low recent rainfall may justify a **possible water-stress warning** and
a suggestion to check field water conditions. It does not prove water
stress and must not automatically instruct irrigation.

If evidence is insufficient, return a neutral monitoring/inspection
recommendation. Do not prescribe specific pesticide, fungicide or
nutrient treatment without adequate validated evidence.

Tests should cover: - no warning when data is missing or poor quality, -
possible-stress rule when supporting evidence exists, - uncertainty
notes, - no disease diagnosis from NDVI alone, - clear handling of stale
observations.

## 11. Phase 6 --- Provider adapters and data integration

Do not integrate every provider at once. First prove one end-to-end
source path with one known location/date, then add other sources as time
permits.

### Satellite

-   Evaluate Sentinel-2 Level-2A surface-reflectance access through a
    feasible provider.
-   Check access/registration, terms, quotas, spatial coverage, cloud
    filtering and implementation complexity.
-   Compute NDVI from valid red and near-infrared reflectance values
    using `(NIR - Red) / (NIR + Red)`.
-   Handle invalid denominators, missing bands, cloud-contaminated
    pixels and invalid geometries.
-   Preserve source identifiers, observation date, retrieval date and
    quality flags.
-   Do not assume every nominal revisit produces a usable cloud-free
    observation.
-   If live access is blocked, use a documented cached/prepared dataset
    with an accurate status label.

### Weather

-   Choose a documented provider after checking current terms, limits
    and attribution.
-   Distinguish historical observations from forecasts.
-   Preserve units, location, timestamps and source.
-   Cache successful responses and expose last-refresh information.

### Soil

-   Use a documented source only if its resolution and properties suit
    the intended context.
-   Label coarse/modelled soil properties as contextual estimates.
-   Never describe a coarse soil map as a real-time measurement of exact
    farm-level soil moisture or nutrients.

### Reliability

-   Keep provider code behind adapters so the advisory logic does not
    depend directly on one provider's response format.
-   Handle timeouts, missing values, rate limits and provider errors.
-   Keep basic demo endpoints working without external access.
-   Report which integrations are real, cached, simulated or still
    unimplemented.

## 12. Phase 7 --- English/Kannada advisory and SMS/voice simulation

The backend must support the future frontend's language and
communication features.

### Languages

-   Initial languages: English (`en`) and Kannada (`kn`).
-   Keep translation templates separate from advisory decision logic.
-   Localize common labels, advisory headlines, explanations and next
    steps.
-   Keep units and scientific identifiers accurate.
-   Provide a sensible fallback when a translation is missing; do not
    silently return empty text.

### SMS

-   Provide a short SMS preview generated from the same advisory record.
-   Account for Unicode text length/encoding when reporting message
    length.
-   Never send a real message in simulation mode.
-   Do not expose provider credentials.

### Voice

-   Provide a voice-advisory text/transcript and a clear simulation
    response suitable for frontend playback or text-to-speech
    integration.
-   Do not claim an outbound call happened when it did not.
-   Evaluate Twilio only after checking current support, India-specific
    restrictions, registration, pricing and account setup.
-   Real delivery is optional; preview/simulation is the required MVP.

### Consent and status

-   Design the backend so real communications require explicit consent
    and a deliberate send action.
-   Keep preview, simulated and real provider statuses distinct.
-   Use `sent` or `delivered` only when a real provider response
    supports that status.
-   Add tests for language fallback, SMS preview, voice preview and
    simulation status.

## 13. Phase 8 --- Supabase persistence

Add Supabase after the core API contract and demo flow work.

-   Use environment variables for project URL and server-side keys.
-   Never expose a service-role key to the browser.
-   Provide schema/migration/setup instructions.
-   Apply appropriate access policies and Row Level Security if
    user-specific data is introduced.
-   Keep a reliable demo fallback if the database is unavailable or
    credentials are not configured.
-   Do not claim authentication or data access security is complete
    without testing it.

## 14. Phase 9 --- Backend validation and handoff

Before calling the backend complete: - Run the full backend test
suite. - Test normal, empty, invalid-ID, stale-data, missing-baseline,
low-quality-data and provider-failure cases. - Verify English/Kannada
outputs. - Verify SMS and voice simulations are unmistakably labelled. -
Verify source, timestamp, status and limitations are returned wherever
applicable. - Confirm no credentials are tracked or logged. - Confirm
the backend runs from documented instructions in a fresh
terminal/session. - Write a backend README containing setup,
configuration, run commands, tests, endpoints and known limitations. -
Create/update an API contract document with example responses for the
future frontend. - Update this file with implemented, tested, simulated
and unimplemented features.

**Backend completion means tested API behavior and a documented
contract, not that every external provider is necessarily connected.**

## 15. Frontend and integration are separate later phases

Only after the backend is accepted as complete: 1. Build the frontend
separately using Stitch's exported design and React. 2. Use the
documented API contract and TypeScript types. 3. Implement language
selection, low-bandwidth layout, field/history/advisory views and
SMS/voice previews. 4. Test the frontend with clearly labelled fixtures
or mocked API responses before integration. 5. Integrate with the
completed backend only after both sides are independently runnable. 6.
Test end-to-end behavior and the final demo.

Do not start these phases unless explicitly instructed after backend
completion.

## 16. Immediate next action for Antigravity

Inspect the current workspace and report: 1. Existing files and folders.
2. Current Python version and environment/dependency tooling. 3. Whether
a backend already exists. 4. Git status, if available. 5. Any setup
blockers. 6. A concise backend-only sequence.

Then implement **Phase 1 only**. Run its tests and report exact
commands/results. Do not scaffold the frontend and do not continue
through all phases in one unreviewed batch.