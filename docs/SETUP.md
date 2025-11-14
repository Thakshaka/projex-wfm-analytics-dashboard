# Setup Guide

## Prerequisites

- Python 3.8+
- MySQL with `projex_wfm` database
- pip

## Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:

```env
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=1234
DB_NAME=projex_wfm
DB_PORT=3306

# Environment
ENVIRONMENT=dev  # or 'prod' for production

# JWT (required for prod)
JWT_SECRET_KEY=your-secret-key
FRONTEND_API_KEY=your-api-key
FRONTEND_API_SECRET=your-api-secret

# CORS (prod only)
CORS_ORIGINS=https://yourfrontend.com
```

### 3. Start server

```bash
cd backend
python main.py
```

Server runs on `http://localhost:5000`

## Authentication

**Dev mode** (`ENVIRONMENT=dev`):
- No auth required
- All endpoints accessible

**Prod mode** (`ENVIRONMENT=prod`):
- Frontend must authenticate first
- All API calls need JWT token
- See [FRONTEND_AUTH.md](FRONTEND_AUTH.md) for integration

## API Docs

Once server is running:
- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

## Troubleshooting

**Server won't start:**
- Check MySQL is running
- Verify DB credentials in `.env`
- Check port 5000 is free

**DB connection errors:**
- Verify MySQL is running
- Check credentials match your DB
- Ensure `projex_wfm` database exists

**Auth errors (prod mode):**
- Ensure `JWT_SECRET_KEY` is set
- Check `FRONTEND_API_KEY` and `FRONTEND_API_SECRET` match
- Verify token in `Authorization: Bearer <token>` header

## Project Structure

```
backend/
├── main.py
├── .env
├── api/
│   ├── auth.py
│   ├── dependencies.py
│   └── project_analytics.py
└── core/
    ├── config.py
    ├── database.py
    └── security.py
```
