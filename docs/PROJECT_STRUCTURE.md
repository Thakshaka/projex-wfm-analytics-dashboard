# Project Structure

```
projex-wfm-analytics-dashboard/
├── backend/                    # FastAPI backend service
│   ├── main.py                 # App entry point
│   ├── .env                    # Environment config (not in git)
│   ├── .env.example            # Environment template
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── dependencies.py     # FastAPI dependencies
│   │   └── project_analytics.py # Project analytics endpoints
│   └── core/                   # Core utilities
│       ├── __init__.py
│       ├── config.py           # Configuration management
│       ├── database.py          # Database connection
│       └── security.py         # JWT utilities
│
├── frontend/                   # Frontend dashboard
│   └── project-analytics.html  # HTML dashboard
│
├── docs/                       # Documentation
│   ├── README.md              # Docs overview
│   ├── SETUP.md               # Setup guide
│   ├── API.md                 # API reference
│   ├── POSTMAN.md             # Postman testing
│   ├── FRONTEND_AUTH.md       # Frontend auth guide
│   ├── PROJECT_STRUCTURE.md    # This file
│   └── poc.txt                # Original requirements
│
├── scripts/                    # Utility scripts
│   ├── start_backend.bat      # Windows startup
│   └── start_backend.sh       # Linux/Mac startup
│
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview
└── LICENSE                     # License file
```

## Key Files

**Backend:**
- `backend/main.py` - FastAPI app entry point
- `backend/.env` - Environment variables (create from .env.example)
- `backend/api/` - All API endpoints
- `backend/core/` - Shared utilities

**Frontend:**
- `frontend/project-analytics.html` - Dashboard UI

**Documentation:**
- All docs in `docs/` folder
- Start with `docs/SETUP.md` for setup
- See `docs/API.md` for endpoint details

## Environment Files

- `backend/.env.example` - Template (commit to git)
- `backend/.env` - Actual config (don't commit, contains secrets)

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cd backend
cp .env.example .env
# Edit .env

# Start
python main.py
```

See [SETUP.md](SETUP.md) for detailed instructions.

