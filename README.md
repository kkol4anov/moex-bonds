# MOEX Bonds

Analytics for Moscow Exchange bonds (OFZ, corporate, replacement bonds)

Data source: public [MOEX ISS API](https://iss.moex.com/iss/reference/).

> **Status:** In active development. See [Roadmap](#roadmap). Currently implemented: project skeleton, domain model.

## Architecture

Layered: `api → services → repositories → models` with an isolated pure-function layer (`finance/`) for financial math.

[Architecture](docs/architecture.md)

## Related work

This is not a novel product. Bond screening for MOEX is a solved problem, and now the exchange itself ships a real-time screener covering all ~4,000 listed issues. Commercial services (Cbonds, Rusbonds, dohod.ru, bonds-lab.ru) go considerably further.

What this project does differently is not the feature set:

- **ISS clients** (`apimoex`, `aiomoex`, `moex_iss`) are libraries, not applications. A thin in-repo client over four endpoints keeps the Pydantic parsing of ISS column-row payloads explicit and testable, without a dependency for 4 endpoints.
- **Open-source MOEX bond tools** are almost exclusively single-file scripts, notebooks, or Telegram bots. None ship schema migrations, a typed domain model, or tests that assert financial correctness.
  The closest architectural sibling is `kapitanov/moex-bond-recommender` (Go, ISS + Postgres + Docker), which models hold-to-maturity only.
- **FX-denominated issues** (replacement bonds, CNY-denominated OFZ) are absent from every open-source project surveyed. They are the reason `FxRate` exists in the schema from the first migration.

The goal here is a correct and defensible core: `Decimal` end to end, pure finance functions with no I/O, and reference-bond tests.

## Trade-offs & Scope

- **PostgreSQL vs SQLite**: single user app, but Postgres gives production-grade numeric/date types, ENUMs and real Alembic migrations.
- **No authentication** - single-user local tool by design; `user_id` will be reserved in schema for a future multi-user design.
- **`Decimal` for money, never `float`** — monetary columns are `Numeric(18, 4)` and stay `Decimal` in Python; `float` appears only
  inside numeric solvers, at an explicit local boundary. Cost: verbosity and manual conversion at solver edges.
- **Repository layer on a single-user project** — arguably over-engineering at this size, kept because it makes service-level tests independent of a live database and states the boundary between business logic and storage. Cost: one extra layer of indirection.
- **Async throughout** — the ISS client is I/O-bound and asynchronous anyway; mixing sync and async paradigms in one codebase produces avoidable friction.
  Cost: a heavier test setup and a smaller pool of synchronous libraries.
- **End-of-day data, not real-time** — ISS history endpoints are sufficient for yield and duration analysis. Cost: intraday analysis is out of scope entirely.
- **Server-side rendering with Jinja, not a Single Page Application (SPA)** — the focus of this project is backend and domain logic; a separate frontend would add a build step, a second language and a second deployment for no analytical value. Cost: no rich interactivity.

## Roadmap
- [x] Stage 0 - project skeleton, Docker, CI, migrations
- [x] Stage 1 - domain model
- [ ] Stage 2 - MOEX ISS client & data loader
- [ ] Stage 3 - financial math with tests
- [ ] Stage 4 - REST API
- [ ] Stage 5 - UI (Jinja)
- [ ] Stage 6 - polish, v1.0

## Tech details

`app/main.py` — entry point FastAPI

[Makefile](Makefile) — unified command interface

## Quick start

```bash
git clone https://github.com/kkol4anov/moex-bonds.git
cd moex-bonds
cp .env.example .env
make up
```

The API is available at `http://localhost:8000`
OpenAPI docs at `http://localhost:8000/docs`

Health check:
```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

## Database migrations
Postgres must be running (make up) before applying migrations:
```bash
make migrate # alembic upgrade head
```

## Development

```bash
uv sync # install dependencies incl. dev tools
make check # lint + typecheck + test (same as CI)
make test # pytest only
make logs # tail application logs
make down # stop containers
```

## License

MIT