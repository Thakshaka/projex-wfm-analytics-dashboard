# Postman Testing Guide

Quick guide for testing APIs with Postman.

## Setup

1. Start the backend:
   ```bash
   cd backend
   python main.py
   ```

2. Create a Postman collection:
   - New → Collection
   - Name: "Project Analytics API"
   - Add variables:
     - `base_url`: `http://localhost:5000`
     - `project_id`: `1`

## Testing Endpoints

### 1. Health Check

- Method: GET
- URL: `{{base_url}}/api/projects/health`
- Expected: `200 OK` with status message

### 2. Get Projects

- Method: GET
- URL: `{{base_url}}/api/projects`
- Optional: Add query param `status=1`
- Expected: Array of projects

### 3. Get Summary

- Method: GET
- URL: `{{base_url}}/api/projects/summary`
- Expected: Summary stats object

### 4. Get Budget

- Method: GET
- URL: `{{base_url}}/api/projects/{{project_id}}/budget`
- Expected: Array of budget objects

### 5. Get Leaderboard

- Method: GET
- URL: `{{base_url}}/api/projects/manager-leaderboard`
- Expected: Array of manager objects

### 6. Get Timeline

- Method: GET
- URL: `{{base_url}}/api/projects/timeline`
- Expected: Array of timeline objects

### 7. Get Risks

- Method: GET
- URL: `{{base_url}}/api/projects/risks`
- Expected: Array of risk alerts

## Production Mode Testing

If `ENVIRONMENT=prod`:

1. **Login first:**
   - Method: POST
   - URL: `{{base_url}}/api/auth/login`
   - Body (JSON):
     ```json
     {
       "api_key": "your-key",
       "api_secret": "your-secret"
     }
     ```
   - Copy the `access_token` from response

2. **Add token to all requests:**
   - Headers tab
   - Key: `Authorization`
   - Value: `Bearer <your-token>`

3. **Auto-set token (optional):**
   Add this to Tests tab in login request:
   ```javascript
   if (pm.response.code === 200) {
       var json = pm.response.json();
       pm.collectionVariables.set("auth_token", json.access_token);
   }
   ```
   Then use `{{auth_token}}` in Authorization header.

## Quick Tips

- Use collection variables for URLs
- Save token as variable after login
- Check response status codes
- Use Postman console for debugging

## Troubleshooting

**401 errors:**
- In prod mode, ensure you're logged in
- Check token in Authorization header
- Verify token hasn't expired

**500 errors:**
- Check backend logs
- Verify DB connection
- Check `.env` configuration

**Connection refused:**
- Ensure backend is running
- Check port 5000 is correct
- Verify firewall settings

