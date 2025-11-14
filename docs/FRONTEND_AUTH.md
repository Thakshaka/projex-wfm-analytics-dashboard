# Frontend Authentication Guide

How to integrate your frontend service with the backend API.

## Overview

Backend requires frontend service authentication in production. Frontend authenticates once, gets a JWT token, then uses it for all API calls.

## Flow

```
Frontend → POST /api/auth/login (api_key, api_secret)
         ← JWT token
         
Frontend → All API calls with Authorization: Bearer <token>
         ← Data
```

## Setup

### Backend Configuration

In `backend/.env` (values from team lead):

```env
ENVIRONMENT=prod
JWT_SECRET_KEY=secret-from-team-lead
FRONTEND_API_KEY=key-from-team-lead
FRONTEND_API_SECRET=secret-from-team-lead
CORS_ORIGINS=https://yourfrontend.com
```

### Frontend Integration

#### 1. Authenticate on startup

```javascript
async function authenticate() {
  const res = await fetch('http://backend:5000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      api_key: process.env.FRONTEND_API_KEY,
      api_secret: process.env.FRONTEND_API_SECRET
    })
  });
  
  const data = await res.json();
  localStorage.setItem('backend_token', data.access_token);
  localStorage.setItem('token_expiry', Date.now() + (data.expires_in * 1000));
  return data.access_token;
}
```

#### 2. Use token in API calls

```javascript
function getAuthHeaders() {
  const token = localStorage.getItem('backend_token');
  const expiry = localStorage.getItem('token_expiry');
  
  if (!token || Date.now() > expiry) {
    await authenticate();
    return getAuthHeaders();
  }
  
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };
}

// Example
async function getProjects() {
  const res = await fetch('http://backend:5000/api/projects', {
    headers: getAuthHeaders()
  });
  return res.json();
}
```

#### 3. Auto-refresh token

```javascript
setInterval(async () => {
  const expiry = localStorage.getItem('token_expiry');
  if (Date.now() > expiry - 5 * 60 * 1000) { // 5 min before expiry
    await authenticate();
  }
}, 60000);
```

## React Example

```javascript
// authService.js
const API_BASE = 'http://backend:5000/api';

export async function getToken() {
  const stored = localStorage.getItem('backend_token');
  const expiry = localStorage.getItem('token_expiry');
  
  if (!stored || Date.now() > expiry) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        api_key: process.env.REACT_APP_API_KEY,
        api_secret: process.env.REACT_APP_API_SECRET
      })
    });
    const data = await res.json();
    localStorage.setItem('backend_token', data.access_token);
    localStorage.setItem('token_expiry', Date.now() + (data.expires_in * 1000));
    return data.access_token;
  }
  
  return stored;
}

export async function apiCall(endpoint, options = {}) {
  const token = await getToken();
  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options.headers
    }
  });
  
  if (res.status === 401) {
    await getToken(); // Refresh
    return apiCall(endpoint, options);
  }
  
  return res.json();
}
```

## Dev vs Prod

**Dev mode** (`ENVIRONMENT=dev`):
- No auth required
- Skip authentication, call APIs directly

**Prod mode** (`ENVIRONMENT=prod`):
- Must authenticate first
- Include token in all requests
- Token expires after 30 minutes

## Troubleshooting

**"Missing auth token" error:**
- Ensure frontend authenticated
- Check token in Authorization header
- Token might be expired (re-authenticate)

**"Invalid API credentials" error:**
- Check `FRONTEND_API_KEY` and `FRONTEND_API_SECRET` in `.env`
- Verify frontend is sending correct values
- Credentials are case-sensitive

**CORS errors:**
- Set `CORS_ORIGINS` to your frontend domain in `.env`
- No trailing slashes
- Restart backend after changing

## Summary

- Authenticate once with API key/secret
- Store JWT token securely
- Include token in all API calls
- Auto-refresh before expiration
- Team lead provides credentials

