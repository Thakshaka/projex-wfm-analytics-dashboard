# Projex WFM Analytics Dashboard

Workforce Management Analytics Dashboard for GDC Consultants.

## Project Analytics Module

This repository contains the **Project Analytics** module - one of several modules in the Projex WFM Analytics Dashboard. Additional modules (Company Overview, Employee Analytics, Client Analytics, etc.) will be added to this repository in the future.

## Quick Start

```bash
pip install -r requirements.txt
cd backend
cp .env.example .env
# Edit .env with your DB credentials
python main.py
```

## Documentation

All documentation is in the [`docs/`](docs/) folder:

- **[Setup Guide](docs/SETUP.md)** - Installation and configuration
- **[API Reference](docs/API.md)** - Endpoints and examples  
- **[Postman Guide](docs/POSTMAN.md)** - Testing with Postman
- **[Frontend Auth](docs/FRONTEND_AUTH.md)** - Frontend integration

## Project Analytics Module Features

- Project analytics with budget tracking
- PM leaderboard and performance metrics
- Risk alerts for overdue/over-budget projects
- Timeline/Gantt visualization data
- JWT authentication for frontend service

## Future Modules

Additional modules will be added to this dashboard:
- Company Overview
- Employee Analytics
- Client Analytics
- Timesheet & Expense Analytics
- Workflow & Productivity
- Predictive & AI Insights

## Project Structure

```
backend/                    # FastAPI backend service
├── main.py                 # App entry point
├── api/                    # API routes
│   └── project_analytics.py # Project Analytics endpoints
└── core/                   # Core utilities

frontend/                   # Frontend dashboards
└── project-analytics.html  # Project Analytics dashboard

docs/                       # Documentation
└── ...                     # Module-specific docs
```

**Note**: As more modules are added, the structure will expand with additional API routes and frontend pages.

## Development

- **Dev mode**: `ENVIRONMENT=dev` (no auth)
- **Prod mode**: `ENVIRONMENT=prod` (JWT auth required)

See [SETUP.md](SETUP.md) for details.
