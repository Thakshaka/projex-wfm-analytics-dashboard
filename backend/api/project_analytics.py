"""
Project analytics endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
from datetime import date
from mysql.connector.connection import MySQLConnection
from api.dependencies import get_db, get_current_user
from core.database import get_db_cursor

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.get("/health")
async def health_check(current_user: dict = Depends(get_current_user)):
    return {"status": "healthy", "service": "Project Analytics API"}

@router.get("")
async def get_projects(
    status_filter: Optional[int] = Query(None, description="Filter by project status"),
    db: MySQLConnection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all projects with budget info"""
    try:
        cursor = get_db_cursor(db)
        if not cursor:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB error.")

        query = """
            SELECT 
                p.project_id, p.project_name, p.client_id, c.client_name,
                p.project_manager, CONCAT(e.first_name, ' ', e.last_name) as manager_name,
                p.start_date, p.end_date, p.status, p.created_at, p.updated_at
            FROM projects p
            LEFT JOIN clients c ON p.client_id = c.client_id
            LEFT JOIN employees e ON p.project_manager = e.employee_id
        """
        
        if status_filter is not None:
            query += " WHERE p.status = %s"
            cursor.execute(query, (status_filter,))
        else:
            cursor.execute(query)

        projects = cursor.fetchall()
        today = date.today()

        for project in projects:
            # Get budget totals
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(allocated_amount), 0) as total_allocated,
                    COALESCE(SUM(burnt_amount), 0) as total_burnt,
                    COALESCE(SUM(remaining_amount), 0) as total_remaining
                FROM budgets WHERE project_id = %s
            """, (project['project_id'],))
            budget = cursor.fetchone()
            
            project['total_allocated'] = float(budget['total_allocated'] or 0)
            project['total_burnt'] = float(budget['total_burnt'] or 0)
            project['total_remaining'] = float(budget['total_remaining'] or 0)
            
            # Calculate variance
            if project['total_allocated'] > 0:
                project['budget_variance'] = ((project['total_burnt'] - project['total_allocated']) / project['total_allocated']) * 100
            else:
                project['budget_variance'] = 0
            
            # Status category
            if project['status'] == 0:
                project['status_category'] = 'completed'
            elif project['end_date'] and project['end_date'] < today:
                project['status_category'] = 'overdue'
            else:
                project['status_category'] = 'active'
            
            # Days overdue
            if project['end_date'] and project['end_date'] < today and project['status'] != 0:
                project['days_overdue'] = (today - project['end_date']).days
            else:
                project['days_overdue'] = 0

        cursor.close()
        return projects

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch projects: {str(e)}")

@router.get("/summary")
async def get_projects_summary(
    db: MySQLConnection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get project summary stats"""
    try:
        cursor = get_db_cursor(db)
        if not cursor:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB error.")
        
        today = date.today()

        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status != 0 AND end_date < %s THEN 1 ELSE 0 END) as overdue,
                SUM(CASE WHEN status != 0 AND (end_date >= %s OR end_date IS NULL) THEN 1 ELSE 0 END) as active
            FROM projects
        """, (today, today))
        summary = cursor.fetchone()

        cursor.execute("""
            SELECT 
                COALESCE(SUM(allocated_amount), 0) as total_allocated,
                COALESCE(SUM(burnt_amount), 0) as total_burnt,
                COALESCE(SUM(remaining_amount), 0) as total_remaining
            FROM budgets
        """)
        budget = cursor.fetchone()

        cursor.close()
        return {
            'total_projects': summary['total'],
            'active_projects': summary['active'],
            'overdue_projects': summary['overdue'],
            'completed_projects': summary['completed'],
            'total_budget_allocated': float(budget['total_allocated']),
            'total_budget_burnt': float(budget['total_burnt']),
            'total_budget_remaining': float(budget['total_remaining'])
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch summary: {str(e)}")

@router.get("/{project_id}/budget")
async def get_project_budget(
    project_id: int,
    db: MySQLConnection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get budget details for a project"""
    try:
        cursor = get_db_cursor(db)
        if not cursor:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB error.")

        cursor.execute("""
            SELECT budget_id, budget_name, budget_type, allocated_amount,
                   burnt_amount, remaining_amount, status
            FROM budgets WHERE project_id = %s
        """, (project_id,))

        budgets = cursor.fetchall()
        for budget in budgets:
            budget['allocated_amount'] = float(budget['allocated_amount'] or 0)
            budget['burnt_amount'] = float(budget['burnt_amount'] or 0)
            budget['remaining_amount'] = float(budget['remaining_amount'] or 0)

        cursor.close()
        return budgets

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch budget: {str(e)}")

@router.get("/manager-leaderboard")
async def get_manager_leaderboard(
    db: MySQLConnection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get PM leaderboard"""
    try:
        cursor = get_db_cursor(db)
        if not cursor:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB error.")
        
        today = date.today()

        cursor.execute("""
            SELECT 
                p.project_manager,
                CONCAT(e.first_name, ' ', e.last_name) as manager_name,
                COUNT(DISTINCT p.project_id) as total_projects,
                COUNT(DISTINCT CASE WHEN p.status = 0 THEN p.project_id END) as completed_projects,
                COUNT(DISTINCT CASE WHEN p.status != 0 AND p.end_date < %s THEN p.project_id END) as overdue_projects,
                COUNT(DISTINCT CASE WHEN p.status != 0 AND (p.end_date >= %s OR p.end_date IS NULL) THEN p.project_id END) as active_projects,
                COALESCE(SUM(b.allocated_amount), 0) as total_budget_managed,
                COALESCE(SUM(b.burnt_amount), 0) as total_burnt,
                AVG(CASE 
                    WHEN b.allocated_amount > 0 
                    THEN ((b.burnt_amount - b.allocated_amount) / b.allocated_amount) * 100 
                    ELSE 0 
                END) as avg_budget_variance
            FROM projects p
            LEFT JOIN employees e ON p.project_manager = e.employee_id
            LEFT JOIN budgets b ON p.project_id = b.project_id
            WHERE p.project_manager IS NOT NULL
            GROUP BY p.project_manager, e.first_name, e.last_name
            ORDER BY completed_projects DESC, total_projects DESC
        """, (today, today))

        leaderboard = cursor.fetchall()
        for manager in leaderboard:
            manager['total_budget_managed'] = float(manager['total_budget_managed'] or 0)
            manager['total_burnt'] = float(manager['total_burnt'] or 0)
            manager['avg_budget_variance'] = float(manager['avg_budget_variance'] or 0)

        cursor.close()
        return leaderboard

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch leaderboard: {str(e)}")

@router.get("/timeline")
async def get_projects_timeline(
    db: MySQLConnection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get project timeline for Gantt chart"""
    try:
        cursor = get_db_cursor(db)
        if not cursor:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB error.")

        cursor.execute("""
            SELECT 
                p.project_id, p.project_name, c.client_name,
                CONCAT(e.first_name, ' ', e.last_name) as manager_name,
                p.start_date, p.end_date, p.status,
                COALESCE(SUM(b.allocated_amount), 0) as budget_allocated,
                COALESCE(SUM(b.burnt_amount), 0) as budget_burnt
            FROM projects p
            LEFT JOIN clients c ON p.client_id = c.client_id
            LEFT JOIN employees e ON p.project_manager = e.employee_id
            LEFT JOIN budgets b ON p.project_id = b.project_id
            GROUP BY p.project_id, p.project_name, c.client_name, e.first_name, e.last_name, 
                     p.start_date, p.end_date, p.status
            ORDER BY p.start_date
        """)

        projects = cursor.fetchall()
        timeline = []
        for p in projects:
            timeline.append({
                'id': p['project_id'],
                'name': p['project_name'],
                'client': p['client_name'] or 'N/A',
                'manager': p['manager_name'] or 'N/A',
                'start': p['start_date'].isoformat() if p['start_date'] else None,
                'end': p['end_date'].isoformat() if p['end_date'] else None,
                'status': 'completed' if p['status'] == 0 else 'active',
                'budget_allocated': float(p['budget_allocated']),
                'budget_burnt': float(p['budget_burnt'])
            })

        cursor.close()
        return timeline

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch timeline: {str(e)}")

@router.get("/risks")
async def get_project_risks(
    db: MySQLConnection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get projects with risk alerts"""
    try:
        cursor = get_db_cursor(db)
        if not cursor:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB error.")
        
        today = date.today()

        cursor.execute("""
            SELECT 
                p.project_id, p.project_name, c.client_name,
                CONCAT(e.first_name, ' ', e.last_name) as manager_name,
                p.start_date, p.end_date, p.status,
                COALESCE(SUM(b.allocated_amount), 0) as allocated_amount,
                COALESCE(SUM(b.burnt_amount), 0) as burnt_amount,
                CASE 
                    WHEN p.end_date < %s AND p.status != 0 THEN (DATEDIFF(%s, p.end_date))
                    ELSE 0
                END as days_overdue,
                CASE 
                    WHEN COALESCE(SUM(b.allocated_amount), 0) > 0 
                    THEN ((COALESCE(SUM(b.burnt_amount), 0) - COALESCE(SUM(b.allocated_amount), 0)) / COALESCE(SUM(b.allocated_amount), 0)) * 100
                    ELSE 0
                END as budget_variance_pct
            FROM projects p
            LEFT JOIN clients c ON p.client_id = c.client_id
            LEFT JOIN employees e ON p.project_manager = e.employee_id
            LEFT JOIN budgets b ON p.project_id = b.project_id
            GROUP BY p.project_id, p.project_name, c.client_name, e.first_name, e.last_name, 
                     p.start_date, p.end_date, p.status
            HAVING (days_overdue > 0) OR (budget_variance_pct > 10)
            ORDER BY days_overdue DESC, budget_variance_pct DESC
        """, (today, today))

        risks = cursor.fetchall()
        alerts = []
        for risk in risks:
            messages = []
            if risk['days_overdue'] > 0:
                messages.append(f"Project is {risk['days_overdue']} days overdue")
            if risk['budget_variance_pct'] > 10:
                messages.append(f"Project is {risk['budget_variance_pct']:.1f}% over budget")

            alerts.append({
                'project_id': risk['project_id'],
                'project_name': risk['project_name'],
                'client_name': risk['client_name'] or 'N/A',
                'manager_name': risk['manager_name'] or 'N/A',
                'days_overdue': risk['days_overdue'],
                'budget_variance_pct': float(risk['budget_variance_pct']),
                'allocated_amount': float(risk['allocated_amount']),
                'burnt_amount': float(risk['burnt_amount']),
                'alerts': messages,
                'risk_level': 'high' if risk['days_overdue'] > 7 or risk['budget_variance_pct'] > 20 else 'medium'
            })

        cursor.close()
        return alerts

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch risks: {str(e)}")
