"""
Database connection utilities
"""
import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse, parse_qs, unquote
from core.config import settings

def parse_connection_string(conn_str: str) -> dict:
    """Parse MySQL connection string into connection config"""
    try:
        parsed = urlparse(conn_str)
        
        auth_part = parsed.netloc.split("@")
        if len(auth_part) == 2:
            user_pass = auth_part[0]
            host_port = auth_part[1]
        elif len(auth_part) == 3:
            user_pass = f"{auth_part[0]}@{auth_part[1]}"
            host_port = auth_part[2]
        else:
            raise ValueError("Invalid connection string format")
        
        if ":" in user_pass:
            user, password = user_pass.rsplit(":", 1)
            user = unquote(user)
            password = unquote(password)
        else:
            user = unquote(user_pass)
            password = ""
        
        if ":" in host_port:
            host, port_str = host_port.rsplit(":", 1)
            port = int(port_str)
        else:
            host = host_port
            port = 3306
        
        config = {
            "host": host,
            "user": user,
            "password": password,
            "database": unquote(parsed.path.lstrip("/")) if parsed.path else "",
            "port": port
        }
        
        query_params = parse_qs(parsed.query)
        
        ssl_mode = query_params.get("ssl-mode", [None])[0]
        if ssl_mode and ssl_mode.upper() in ["REQUIRED", "PREFERRED"]:
            config["ssl_disabled"] = False
            config["ssl_verify_cert"] = True
            config["ssl_verify_identity"] = True
        
        return config
    except Exception as e:
        raise ValueError(f"Failed to parse connection string: {e}")

def get_db_connection():
    """Get a MySQL database connection"""
    try:
        connection_config = {}
        
        if settings.DB_CONNECTION_STRING:
            connection_config = parse_connection_string(settings.DB_CONNECTION_STRING)
            if "mysql.database.azure.com" in connection_config.get("host", "").lower():
                connection_config["ssl_disabled"] = False
                connection_config["ssl_verify_cert"] = True
                connection_config["ssl_verify_identity"] = True
        elif settings.DB_HOST and settings.DB_USER and settings.DB_PASSWORD and settings.DB_NAME:
            connection_config = {
                "host": settings.DB_HOST,
                "user": settings.DB_USER,
                "password": settings.DB_PASSWORD,
                "database": settings.DB_NAME,
                "port": settings.DB_PORT
            }
        else:
            raise ValueError("DB configuration must be set")
        
        return mysql.connector.connect(**connection_config)
    except Error as e:
        print(f"DB connection error: {e}")
        return None
    except Exception as e:
        print(f"DB configuration error: {e}")
        return None

def get_db_cursor(conn):
    """Get a dictionary cursor from connection"""
    if conn:
        return conn.cursor(dictionary=True)
    return None
