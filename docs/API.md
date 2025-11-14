# API Reference

Base URL: `http://localhost:5000/api`

## Authentication

**Dev mode**: No auth required  
**Prod mode**: JWT token required (see [FRONTEND_AUTH.md](FRONTEND_AUTH.md))

## Endpoints

### Auth

**POST /api/auth/login**
```json
// Request
{
  "api_key": "your-key",
  "api_secret": "your-secret"
}

// Response
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**GET /api/auth/me**
Returns current authenticated service info.

### Projects

**GET /api/projects/health**
Health check endpoint.

**GET /api/projects**
Get all projects with budget info.

Query params:
- `status` (optional): Filter by status code

Response:
```json
[
  {
    "project_id": 1,
    "project_name": "Website Redesign",
    "client_name": "ABC Corp",
    "manager_name": "John Doe",
    "start_date": "2024-01-15",
    "end_date": "2024-06-30",
    "status": 1,
    "total_allocated": 50000.0,
    "total_burnt": 35000.0,
    "total_remaining": 15000.0,
    "budget_variance": -30.0,
    "status_category": "active",
    "days_overdue": 0
  }
]
```

**GET /api/projects/summary**
Get summary statistics.

Response:
```json
{
  "total_projects": 45,
  "active_projects": 28,
  "overdue_projects": 5,
  "completed_projects": 12,
  "total_budget_allocated": 2500000.0,
  "total_budget_burnt": 1800000.0,
  "total_budget_remaining": 700000.0
}
```

**GET /api/projects/{project_id}/budget**
Get detailed budget for a project.

**GET /api/projects/manager-leaderboard**
Get PM performance leaderboard.

**GET /api/projects/timeline**
Get timeline data for Gantt chart.

**GET /api/projects/risks**
Get projects with risk alerts (overdue or over budget).

## Error Responses

**401 Unauthorized**
```json
{
  "detail": "Missing auth token."
}
```

**500 Internal Server Error**
```json
{
  "detail": "Failed to fetch projects: <error>"
}
```

## Interactive Docs

- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

Test endpoints directly from the browser.

