# Project Context --- Earthworm

## 1. Project summary

**Working name:** Earthworm\
**Project type:** Responsive website for a 24-hour hackathon\
**Domain:** Agriculture and food technology\
**Pilot region:** Mandya district, Karnataka, India\
**Initial crop focus:** Paddy (rice), subject to confirming suitable
data availability\
**Primary users:** Smallholder farmers with varying digital literacy,
limited connectivity, and a preference for local-language information.

Earthworm is a satellite-based early-warning and advisory platform. It
combines satellite-derived vegetation observations with weather
information and available soil context to flag possible crop stress,
explain the evidence, and suggest cautious next steps.

It is not a generic farming app, crop marketplace, or a system that can
diagnose every disease. It must not claim that satellite data alone can
identify a specific disease, nutrient deficiency, or irrigation need.

## 2. Problem and product promise

Farmers may not notice crop stress until visible symptoms become
obvious. The platform aims to help farmers: 1. See the latest available
observations for a selected field. 2. Understand how the field's
vegetation indicators have changed over time. 3. Compare current
observations with a suitable historical baseline or seasonal benchmark
when valid data exists. 4. View weather and available soil context that
may help explain the observations. 5. Receive an understandable,
cautious advisory in a selected language. 6. Access essential
information through a lightweight website and preview low-bandwidth
SMS/voice channels.

The system should explain what was observed, when it was observed, why
it may matter, what is uncertain, and what the farmer can check next.

## 3. Technology plan

-   Backend first: Python + FastAPI.
-   Database: Supabase (PostgreSQL), introduced after the API contract
    and demo flow are stable.
-   Frontend later: React + Vite unless Stitch export or workspace
    compatibility makes a different choice preferable.
-   Design: Google Stitch; export and implement only after the backend
    is complete.
-   Satellite source candidate: Sentinel-2 Level-2A surface reflectance
    through a feasible provider such as Copernicus Data Space or Google
    Earth Engine, if access/setup is feasible.
-   Weather source candidate: Open-Meteo or another suitable source
    after checking current API terms and limits.
-   Soil context candidate: SoilGrids or another documented source.
    Treat coarse soil properties as contextual estimates, not real-time
    field measurements.
-   Communication provider candidate: Twilio may be evaluated for
    SMS/voice, but real delivery is not a core dependency. Build a
    clearly labelled simulation first.

Do not assume any external account, API, credential, quota, dataset, or
provider integration is already configured.

## 4. Core features

### A. Farm and field overview

-   Select a demo farm/field.
-   Show location, crop, crop season/growth stage when known, and latest
    observation.
-   Show source and observation timestamp separately from the time the
    application last refreshed data.
-   Clearly label demonstration/sample data.

### B. Satellite observations and trends

-   Store dated observations and their provenance.
-   Compute vegetation indicators such as NDVI only from valid,
    documented red and near-infrared reflectance values.
-   Track cloud/quality flags and missing observations where available.
-   Show a time series when multiple valid observations exist.
-   Do not invent satellite values or pretend cached demonstration data
    is live.

### C. Historical data and benchmarks

Distinguish: - **Field history:** observations for the same field over
time. - **Seasonal baseline:** comparison from suitable observations for
the same/comparable crop stage and season, when available. - **Regional
benchmark:** contextual comparison with other fields/region only when
source and methodology justify it. - **Crop/yield statistics:**
district-level statistics are context only; they are not proof of
field-level yield improvement or intervention impact.

Every baseline/benchmark must show its period, source, sample coverage
and limitations. Avoid comparisons across incompatible crop stages,
seasons, cloud conditions or data products. If suitable historical data
is unavailable, state that honestly. Clearly label any demo fixture.

### D. Weather and soil context

-   Display relevant weather observations/forecasts and their
    source/timestamps.
-   Store/cache fetched observations when useful.
-   Treat soil information as background context unless the source
    provides current field-level measurements.
-   Never imply that coarse soil maps reveal the exact current moisture
    or nutrient state of an individual field.

### E. Explainable advisory

Use transparent, inspectable rules for the MVP rather than an opaque
model. Each advisory should include observed signals, supporting
context, possible interpretation, recommended next check/action,
uncertainty/data-quality note, observation date and sources.

A declining vegetation indicator plus low recent rainfall may justify
asking the farmer to inspect water conditions. It does not prove water
stress. Do not issue specific pesticide/fungicide or nutrient
prescriptions without adequate evidence and an appropriate validated
basis.

### F. Languages and low-bandwidth access

-   Initial UI/advisory languages: English and Kannada.
-   Keep architecture extensible for more languages.
-   Keep translated templates separate from decision logic.
-   Advisory content should be short, clear and farmer-friendly.
-   Build a text-first/low-bandwidth mode that reduces heavy imagery,
    map dependence, animation and unnecessary requests.
-   Design for small screens and slow connections.

### G. SMS and voice

For the MVP: - Build SMS preview and voice advisory preview/simulation
first. - Use explicit statuses such as `preview_only` or `simulated` for
simulations. - Never display `sent` or `delivered` unless an actual
provider response supports that state. - Provide Kannada text preview
and a voice transcript/playback path where feasible. - Require consent
before any real outbound communication. - Keep provider credentials
server-side. - Evaluate Twilio only after verifying current
availability, India-specific rules, registration requirements, pricing
and account setup. Do not make live messaging/calling a demo dependency.

## 5. Data integrity and provenance

Every observation or derived value should, where applicable, identify: -
source/provider, - observation timestamp or period, -
retrieval/processing timestamp, - field/location association, - units
and calculation method, - quality/cloud flags, - status: observed,
derived, estimated, simulated, or demo, - important limitations.

Distinguish observed, derived, estimated/contextual, and simulated/demo
data in both API responses and future UI.

Never fabricate real readings, historical records, benchmark values,
validation accuracy, delivery confirmations, yield gains or water
savings.

## 6. Validation and claims

If time allows, include evidence about usable records/fields, date
range, number of valid observations, cloud/quality exclusions, source
availability and missing-data rates.

Do not claim disease-detection accuracy without labelled ground truth.
Do not claim measured water/yield savings from a hypothetical scenario.
Any scenario estimate must be labelled simulated and state assumptions.
District-level yield statistics cannot prove farm-level impact.

## 7. Project constraints and workflow

**Mandatory build order:** 1. Complete and test the backend in
isolation. 2. Build the frontend separately using Stitch and React. 3.
Integrate the frontend with the completed backend. 4. Run end-to-end
tests and prepare the demo.

Until the backend is complete, do not create or modify frontend files.

The backend must run without external API credentials, using clearly
labelled demo fixtures where needed. Keep provider integrations modular.
Work incrementally, test each phase, report exact commands/results, and
avoid unnecessary rewrites. Explain important choices in plain language
without turning every step into a long lecture.
