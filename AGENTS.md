# AGENTS.md

> **TL;DR**  This repository hosts an **AI‑powered Quotation Generator** for **Portal Center**, a small business that installs and maintains automatic gates, CCTV systems and security structures for condominiums across Greater São Paulo.  The system lets the owner send a short **voice or text message in Telegram** and instantly receive a fully‑formatted **DOCX proposal** based on the company’s long‑time template.  The backend is written in **Python 3.12** (FastAPI + FastMCP + python‑docx) and is orchestrated via **n8n**.  The goal of this document is to brief Codex (and any human contributors) on how the project is organised, how to run it locally and how to collaborate effectively.

---

## 1  Project Purpose & Scope

|                  | Details                                                                                                                                                                                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Objective**    | Automate generation of client quotations, cutting preparation time from *tens of minutes* to *seconds*.                                                                                                                                          |
| **Primary User** | Company director (Telegram on mobile).                                                                                                                                                                                                           |
| **MVP Features** | \* Parse natural‑language (PT‑BR) voice or text. \* Validate required fields (A/C, e‑mail, date…). \* Maintain dialogue to collect missing data. \* Insert line‑items (product/service, qty, unit price). \* Produce DOCX using legacy template. |
| **Out‑of‑scope** | Redesigning the visual layout, digital signatures, CRM integration (future).                                                                                                                                                                     |
| **Tech Stack**   | Python 3.12, FastAPI, FastMCP, python‑docx, Pydantic, PostgreSQL (SQLite for dev), OpenAI GPT‑4o & Whisper, n8n, Telegram Bot API, Docker, GitHub Actions.                                                                                       |

### 1.1  System Architecture (high‑level)

```
┌──────────────────┐      ┌─────────────┐      ┌────────────────┐
│ Telegram Client  │──►──│  n8n LLM    │──►──│ FastMCP Client │
└──────────────────┘      │  (GPT‑4o)   │      │  (FastAPI)     │
                          └─────┬───────┘      └──────┬─────────┘
                                │                   ┌─▼───────────┐
                                │                   │ Service     │
                                │                   │  Layer      │
                                │                   └─┬───┬───┬───┘
                                │                     │   │   │
                                ▼                     ▼   ▼   ▼
                          ┌─────────────┐   ┌──────────────┐   ┌────────────┐
                          │ Template    │   │ Docx Builder │   │ Persistence │
                          │ Validation  │   │ (python‑docx)│   │  (DB)       │
                          └─────────────┘   └──────────────┘   └────────────┘
```

*Every AI call is wrapped by ****FastMCP**** so that the agent can decide which "tool" (endpoint) to invoke:*

- **create\_budget** – start a new quotation.
- **add\_item** – append a line‑item.
- **update\_header** – update header fields (client, email, …).
- **update\_item** – edit qty/price/description of an existing line.

---

## 2  Code Base Layout

```
📦 portalcenter‑quotation
├─ app/                   # FastAPI entrypoint & routers
│  ├─ main.py             # `uvicorn app.main:app` boots here
│  ├─ api/                # REST + MCP endpoints
│  ├─ core/               # settings, logging, deps
│  ├─ mcp_tools/          # create_budget.py, add_item.py, …
│  ├─ services/           # business logic (LLM, docx, db)
│  ├─ models/             # Pydantic schemas & ORM models
│  └─ templates/          # .docx master template(s)
├─ tests/                 # pytest suites
├─ scripts/               # one‑off helpers / data loaders
├─ requirements.txt       # frozen with `pip‑tools`
└─ docker/                # Dockerfile & compose overrides
```

> **Tip:** keep modules small and side‑effect‑free; business logic must live in `services/`, never inside routes.

---

## 3  Development Standards

| Category          | Guideline                                                                                          |
| ----------------- | -------------------------------------------------------------------------------------------------- |
| **Style**         | Auto‑format with **black**, organise imports with **isort**, lint with **ruff** (PEP 8 compliant). |
| **Typing**        | Full type hints; mypy passes CI (“strict” mode).                                                   |
| **Branches**      | `main` → protected; feature branches use `feat/<slug>`; bug‑fixes use `fix/<slug>`.                |
| **Commits**       | **Conventional Commits** (`feat:`, `fix:`, `chore:` …).                                            |
| **Pull Requests** | At least one reviewer; description must include *what + why + screenshots/JSON sample*.            |
| **Pre‑commit**    | Run `pre‑commit install`; hooks auto‑run black, ruff, mypy & pytest.                               |

---

## 4  Local Setup

```bash
# 1. Clone and enter repo
$ git clone https://github.com/<org>/portalcenter-quotation.git && cd portalcenter-quotation

# 2. Create venv + install deps
$ python -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt

# 3. Copy & edit environment variables
$ cp .env.example .env  # fill OPENAI_API_KEY, TELEGRAM_TOKEN, TEMPLATE_PATH …

# 4. Launch API (hot‑reload)
$ uvicorn app.main:app --reload --port 8000

# 5. Run ngrok or expose via n8n → Telegram webhook
```

### 4.1  Useful Make Targets

```bash
make lint   # ruff + mypy
make test   # pytest + coverage
make run    # uvicorn production settings
```

---

## 5  Testing Strategy

| Tool           | Purpose                                                  |
| -------------- | -------------------------------------------------------- |
| **pytest**     | Unit & integration tests.                                |
| **pytest‑cov** | Enforce ≥ 90 % coverage on `services/` and `mcp_tools/`. |
| **httpx**      | Async API test‑client.                                   |

### Rules

1. Every new endpoint or service function requires at least one happy‑path and one failure test.
2. Fixtures must be factory‑based (`pytest‑factoryboy`) to avoid brittle hard‑coded IDs.
3. Mock external APIs (OpenAI, Telegram) with `respx`.

---

## 6  Automation & CI

- **GitHub Actions** pipeline:
  1. `setup` – cache deps, install Python.
  2. `lint` – black + ruff + mypy.
  3. `test` – pytest w/ coverage, upload badge.
  4. `docker` – build & push on tag `v*.*.*`.
- Merges into `main` require ✅ for steps 2‑3.

---

## 7  Contribution Guide

1. **Open an Issue** – use the *Bug Report* or *Feature Request* template.
2. **Fork → Branch → PR** – reference the issue ID in the title (`feat(#42): allow decimal qty`).
3. **Code Review** – respond to all comments, squash when approved.
4. **Communication** – primary channel is GitHub Discussions; secondary is Slack `#portalcenter‑dev`.

---

## 8  Scalability & Maintenance

| Area              | Recommendation                                                                                        |
| ----------------- | ----------------------------------------------------------------------------------------------------- |
| **Templates**     | Version each DOCX in `templates/vYYYYMMDD_template.docx`; store migration notes.                      |
| **Database**      | Use Alembic for schema migrations; never break backward compatibility with old quotations.            |
| **Services**      | Keep pure functions; side‑effects isolated (I/O, external APIs).                                      |
| **Agents**        | New "tools" must inherit from `BaseTool` and register in `app.mcp_tools.__init__` for auto‑discovery. |
| **Docs**          | All public functions/classes need docstrings; complex flows get diagrams in `/docs/`.                 |
| **Dependencies**  | Weekly Dependabot updates; pin exact versions in `requirements.txt`.                                  |
| **Observability** | Structured logging (json) + OpenTelemetry traces (future).                                            |

---

## 9  Roadmap (next steps)

| Q3 2025                                      | Q4 2025                                         |
| -------------------------------------------- | ----------------------------------------------- |
| • Web dashboard for quote history & editing. | • PDF output option with corporate styling.     |
| • OAuth‑based multi‑tenant support.          | • CRM integration (HubSpot).                    |
| • Fine‑tuned Whisper model for noisy audio.  | • Self‑service analytics on quotation win‑rate. |

---

## 10  Acknowledgements

*Business domain experts*: **Portal Center** (São Bernardo do Campo, BR)  —  template & process insights.

*Technical mentorship*: **Felipe Matos Silvieri** – project lead & architect.

---

> **Happy Shipping! 🚀**

