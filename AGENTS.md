# AGENTS.md

> **TL;DR** This repository hosts an **AI‑powered Quotation Generator** for **Portal Center**, a small business that installs and maintains security gates, CCTV systems and metal structures for condominiums across Greater São Paulo.  The owner sends a short **voice or text message in Telegram** and instantly receives a fully‑formatted **DOCX proposal** based on the company’s long‑time template.  The backend is built with **Python 3.12**, **FastMCP** and **python‑docx**.  This document briefs Codex (and any human contributors) on how the project is organised, how to run it locally and how to collaborate effectively.

> ℹ️ **Mais detalhes sobre a aplicação de MCP encontram‑se na pasta** `learn` **na raiz do repositório.**

---

## 1  Project Purpose & Scope

|                  | Details                                                                                                                                                                                                                                     |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**    | Automate generation of client quotations, cutting preparation time from *tens of minutes* to *seconds*.                                                                                                                                     |
| **Primary User** | Company director (Telegram on mobile).                                                                                                                                                                                                      |
| **MVP Features** | • Parse natural‑language (PT‑BR) voice or text. • Validate required fields (A/C, e‑mail, date…). • Maintain dialogue to collect missing data. • Insert line‑items (product/service, qty, unit price). • Produce DOCX using legacy template. |
| **Out‑of‑scope** | Redesigning the visual layout, digital signatures, CRM integration (future).                                                                                                                                                                |
| **Tech Stack**   | Python 3.12, **FastMCP**, python-docx, Pandas, Pydantic, OpenAI GPT-4o & Whisper, Telegram Bot API. |

### 1.1  System Architecture (high‑level)

```
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│ Telegram Client  │──►──│  LLM Orchestrator │──►──│ FastMCP Server   │
└──────────────────┘      │    (GPT‑4o)      │      │    (Python)      │
                          └─────┬───────┘      └──────┬──────────┘
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

*The FastMCP server exposes tools consumed directly by the LLM agent:*

- **create\_budget** – start a new quotation.
- **add\_item** – append a line‑item.
- **update\_header** – update header fields (client, email, …).
- **update\_item** – edit qty/price/description of an existing line.

---

## 2  Code Base Layout

```
📦 budget_agent
├─ mcp_server.py         # `python mcp_server.py` boots FastMCP
├─ mcp_tools/            # MCP tools used by the agent
├─ services/             # document generation logic
├─ tests/                # pytest suites
├─ learn/                # FastMCP notes and examples
├─ requirements.txt      # locked dependencies
└─ logo_portal_center.png # branding asset used in quotes
```

> **Tip:** keep modules small and side‑effect‑free; business logic lives in `services/`, never in `mcp_tools/`.

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

## 5  Testing Strategy

| Tool           | Purpose                                                  |
| -------------- | -------------------------------------------------------- |
| **pytest**     | Unit & integration tests.                                |
| **pytest‑cov** | Enforce ≥ 90 % coverage on `services/` and `mcp_tools/`. |
| **httpx**      | Async client to test MCP HTTP transport.                 |

### Rules

1. Every new tool or service function requires at least one happy‑path and one failure test.
2. Fixtures use factory‑based objects (`pytest‑factoryboy`) to avoid brittle IDs.
3. Mock external APIs (OpenAI, Telegram) with `respx`.

---

## 6  Automation & CI

Continuous integration is not yet configured. Contributors should run
`ruff`, `mypy` and `pytest` locally before opening a pull request.

---

## 7  Contribution Guide

1. **Open an Issue** – use the *Bug Report* or *Feature Request* template.
2. **Fork → Branch → PR** – reference the issue ID in the title (`feat(#42): allow decimal qty`).
3. **Code Review** – respond to all comments, squash when approved.
4. **Communication** – primary channel is GitHub Discussions; secondary is Slack `#portalcenter‑dev`.

---

## 8  Scalability & Maintenance

| Area              | Recommendation                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------ |
| **Templates**     | Version each DOCX in `templates/vYYYYMMDD_template.docx`; store migration notes.           |
| **Database**      | Use Alembic for schema migrations; never break backward compatibility with old quotations. |
| **Services**      | Keep pure functions; side‑effects isolated (I/O, external APIs).                           |
| **Agents**        | New "tools" inherit from `BaseTool` and auto‑register in `mcp_tools.__init__`.             |
| **Docs**          | All public functions/classes need docstrings; complex flows get diagrams in `/docs/`.      |
| **Dependencies**  | Weekly Dependabot updates; pin exact versions in `requirements.txt`.                       |
| **Observability** | Structured logging (json) + OpenTelemetry traces (future).                                 |

---

## 9  Roadmap (next steps)

| Q3 2025                                      | Q4 2025                                         |
| -------------------------------------------- | ----------------------------------------------- |
| • Web dashboard for quote history & editing. | • PDF output option with corporate styling.     |
| • OAuth‑based multi‑tenant support.          | • CRM integration (HubSpot).                    |
| • Fine‑tuned Whisper model for noisy audio.  | • Self‑service analytics on quotation win‑rate. |

---

## 10  Acknowledgements

*Business domain experts*: **Portal Center** (São Bernardo do Campo, BR) — template & process insights.

*Technical mentorship*: **Felipe Matos Silvieri** – project lead & architect.

---

> **Happy Shipping! 🚀**

