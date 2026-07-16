# MOEX Bonds

Analytics for Moscow Exchange bonds (OFZ, corporate, replacement bonds)

Data source: public [MOEX ISS API](https://iss.moex.com/iss/reference/).

> **Status:** In active development. See [Roadmap](#roadmap). Currently implemented: project skeleton, domain model.

## Architecture

Layered: `api → services → repositories → models` with an isolated pure-function layer (`finance/`) for financical math.

## Trade-offs & Scope

- **PostgreSQL vs SQLite**: single user app, but Postgres gives production-grade numeric/date types, ENUMs and real Alembic migrations.
- **No authentification** - single-user local tool by desicn; `user_id` will be reserved in schema for a future multi-user design.

## Roadmap
- [x] Stage 0 - project skeleton, Docker, CI, migrations
- [ ] Stage 1 - domain model
- [ ] Stage 2 - MOEX ISS client & data loader
- [ ] Stage 3 - financial math with tests
- [ ] Stage 4 - REST API
- [ ] Stage 5 - UI (Jinja)
- [ ] Stage 6 - polish, v1.0


## License

MIT