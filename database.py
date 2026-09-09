"""
SQLite Database module for Moretus application
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional
from datetime import datetime


class Database:
    """Database handler for SQLite operations"""
    
    def __init__(self, db_path: str = "moretus.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self._connect()
        self._initialize_tables()
    
    def _connect(self) -> None:
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            print(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
    
    def _initialize_tables(self) -> None:
        """Create tables if they don't exist"""
        try:
            # Load and execute schema from SQL file
            sql_file = os.path.join(os.path.dirname(__file__), "sql", "moretus_sqlite.sql")
            
            if os.path.exists(sql_file):
                with open(sql_file, "r", encoding="utf-8") as f:
                    sql_script = f.read()
                    self.cursor.executescript(sql_script)
                    self.connection.commit()
                    print(f"Schema loaded from {sql_file}")
            else:
                # Fallback: create default tables if SQL file doesn't exist
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        value REAL,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                self.connection.commit()
                print("Created default records table")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = None) -> None:
        """
        Execute INSERT, UPDATE, or DELETE query
        
        Args:
            query: SQL query string
            params: Query parameters
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            raise
    
    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        """
        Fetch a single record
        
        Args:
            query: SQL SELECT query
            params: Query parameters
            
        Returns:
            Single record as dictionary or None
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Fetch error: {e}")
            raise
    
    def fetch_all(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        Fetch all records matching query
        
        Args:
            query: SQL SELECT query
            params: Query parameters
            
        Returns:
            List of records as dictionaries
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Fetch error: {e}")
            raise
    
    def insert_record(self, table: str, data: Dict[str, Any]) -> int:
        """
        Insert a new record
        
        Args:
            table: Table name
            data: Dictionary of column-value pairs
            
        Returns:
            ID of inserted record
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            self.cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Insert error: {e}")
            raise
    
    def update_record(self, table: str, data: Dict[str, Any], where: Dict[str, Any]) -> int:
        """
        Update existing record
        
        Args:
            table: Table name
            data: Dictionary of column-value pairs to update
            where: Dictionary for WHERE clause
            
        Returns:
            Number of rows affected
        """
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        where_clause = " AND ".join([f"{k} = ?" for k in where.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        try:
            self.cursor.execute(query, tuple(list(data.values()) + list(where.values())))
            self.connection.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"Update error: {e}")
            raise
    
    def delete_record(self, table: str, where: Dict[str, Any]) -> int:
        """
        Delete record(s)
        
        Args:
            table: Table name
            where: Dictionary for WHERE clause
            
        Returns:
            Number of rows deleted
        """
        where_clause = " AND ".join([f"{k} = ?" for k in where.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        try:
            self.cursor.execute(query, tuple(where.values()))
            self.connection.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"Delete error: {e}")
            raise
    
    def close(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("Database connection closed")
    
    def __del__(self):
        """Cleanup on object destruction"""
        self.close()
