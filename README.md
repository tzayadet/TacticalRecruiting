# Tactical Recruiting

A local-first prototype for IT talent operations. It combines a Python application with SQLite persistence, a technical interview question bank and a separate static web showcase.

<p align="center">
  <a href="https://github.com/tzayadet/TacticalRecruiting"><img src="https://img.shields.io/badge/SOURCE-GITHUB-161b22?style=flat-square&logo=github" alt="Source code"></a>
  <a href="rrhh-demo/index.html"><img src="https://img.shields.io/badge/SHOWCASE-SOURCE-00a86b?style=flat-square" alt="Showcase source"></a>
</p>

[![Python CI](https://github.com/tzayadet/TacticalRecruiting/actions/workflows/ci.yml/badge.svg)](https://github.com/tzayadet/TacticalRecruiting/actions/workflows/ci.yml) · [![Pages deployment](https://github.com/tzayadet/TacticalRecruiting/actions/workflows/pages.yml/badge.svg)](https://github.com/tzayadet/TacticalRecruiting/actions/workflows/pages.yml)

## What it does

- Organizes candidate records in a local SQLite database.
- Provides a technical question bank for IT recruitment workflows.
- Separates the Python application from the browser-based showcase.
- Uses illustrative candidate profiles and sample records in the static demo.

## Run locally

**Requirements:** Python 3.10 or later.

```bash
python main.py
```

The application stores data locally in SQLite. Candidate CV files and local databases are excluded from version control. Do not add real candidate records, CVs, exports or personal data to this public repository.

## Project structure

| Path | Purpose |
|---|---|
| `main.py`, `database.py` | Modular Python application and SQLite persistence |
| `models.py` | Data models and enumerations |
| `questions.py` | Technical interview question bank |
| `rrhh-demo/` | Independent static showcase |
| `tests/` | Automated tests |
| `.github/workflows/` | CI and Pages deployment |

## Showcase and deployment

The static showcase is in `rrhh-demo/`. It uses fictional data and browser-local storage. It does not connect to the Python application or SQLite database and does not send records to a server.

The Pages workflow publishes only `rrhh-demo/`, not the backend, local database or internal files. GitHub Pages still needs to be enabled in repository settings and the `ENABLE_PAGES=true` Actions variable configured before the deployment can be considered live.

## Scope and limitations

This is a prototype, not a production applicant tracking system (ATS). The web showcase and Python application are independent components; they do not share an API or database. The local application does not provide production-grade encryption, access control, retention management or audit controls.

Any scoring or evaluation output is advisory and must not be used as an automated hiring decision. Before handling real candidate data, the application would require a full privacy, security and legal review.

## Tests

```bash
python -m pytest
```

## License

No reuse license is currently declared. Public visibility does not grant permission to redistribute, modify or use the project commercially.
