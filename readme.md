# InferRoute

**An intelligent LLM gateway with cost-aware routing, rate limiting, and circuit breaking.**

InferRoute sits in front of multiple LLM providers and routes each request to the model that best balances cost, latency, and quality — using a trained cost-prediction model rather than static rules. It's built to behave like production infrastructure: async by default, observable, and resilient to upstream failures.

---

## Why InferRoute

Most LLM gateways route on simple heuristics (round-robin, fixed fallback chains, or manual model pinning). InferRoute instead predicts the expected cost and performance of a request *before* sending it, and routes accordingly — giving teams a way to cut inference spend without hand-tuning rules for every use case.

---

## Features

- **Intelligent routing** — predicts cost/latency per request using a trained ML model and routes to the optimal backend
- **Cost prediction** — XGBoost/LightGBM models served via a dedicated FastAPI `/predict` microservice
- **Rate limiting** — Redis-backed, per-key and per-tenant limits
- **Circuit breaking** — hand-rolled circuit breaker to isolate failing upstream providers rather than cascading failures
- **Dual authentication** — API key hashing (SHA-256) for `/v1/*` data-plane routes, JWT for `/admin/*` management routes
- **Observability** — Prometheus metrics with Grafana dashboards out of the box

---

## Architecture

```
Client
  │
  ▼
FastAPI Gateway (async, SQLAlchemy 2.0)
  │
  ├── Auth Layer (API key / JWT)
  ├── Rate Limiter (Redis)
  ├── Router ──► Cost Prediction Service (FastAPI /predict, XGBoost/LightGBM)
  ├── Circuit Breaker
  │
  ▼
Upstream LLM Providers
  │
  ▼
PostgreSQL (source of truth) · Redis (cache/rate limiting) · Prometheus/Grafana (metrics)
```

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI |
| ORM / DB access | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL |
| Cache / rate limiting | Redis |
| Migrations | Alembic |
| ML routing model | XGBoost / LightGBM |
| Metrics | Prometheus + Grafana |
| Frontend (admin dashboard) | React + Tailwind |

> ClickHouse is under consideration as an analytics store for request-level logs at scale.

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker (optional, for local services)

### Installation

```bash
git clone https://github.com/upendra-uddagiri/inferroute.git
cd inferroute
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Copy the example environment file and set your database, Redis, and provider credentials:

```bash
cp .env.example .env
```

### Run migrations

```bash
alembic upgrade head
```

### Start the gateway

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## Authentication

- **`/v1/*`** (inference routes) — API key in the `Authorization` header, hashed with SHA-256 before comparison/storage
- **`/admin/*`** (management routes) — JWT bearer tokens

---

## Project Status

InferRoute is under active development. Core routing, auth, and rate limiting are implemented; the cost-prediction layer and observability stack are being built out iteratively. See the [Software Design Document](./docs/SDD.pdf) for the full architecture and phased build plan.

A phone-native spinoff, **InferRoute Mobile**, adapts the routing concept to route prompts between an on-device NPU model and the cloud gateway.

---

## Contributors

- [Upendra Uddagiri](https://github.com/upendra-uddagiri) — architecture, gateway, infrastructure
- Aswin — ML / cost-intelligence layer

---

## License

MIT