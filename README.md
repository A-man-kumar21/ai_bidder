# AI-Powered Integrated Bid Compliance Verification Platform

SIH 2026 prototype for transparent, human-in-the-loop compliance verification in GeM procurement.

## Repository layout

- `frontend/` — React dashboard for procurement officers.
- `backend-gateway/` — Express API gateway and audit-trail persistence.
- `ai-engine/` — FastAPI verification and scoring service.
- `mock-adapters/` — Pluggable government-portal adapter contracts and demo data.
- `docs/` — Architecture, integration, and decision documentation.

## Planned service boundaries

`React dashboard → Express gateway → FastAPI AI engine → adapters`

Adapter data is deliberately kept behind interfaces so government integrations can replace mock implementations without changing the scoring API.

## Development status

Only the initial monorepo scaffold is present. The mock adapters, engine, gateway functionality, and dashboard will be added in subsequent reviewed stages.
