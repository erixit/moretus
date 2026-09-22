#!/usr/bin/env python3
"""
Script to import playerlist_130_2627.xlsx into a new playerlist table in moretus.db
"""

import pandas as pd
import sqlite3
import os


def import_playerlist():
    """Import Excel data into SQLite database"""
    
    # Paths
    excel_path = os.path.join(os.path.dirname(__file__), 'data', 'playerlist_130_2627.xlsx')
    db_path = os.path.join(os.path.dirname(__file__), 'moretus.db')
    
    print(f"Reading Excel file: {excel_path}")
    
    # Read Excel file
    try:
        df = pd.read_excel(excel_path)
        print(f"Loaded {len(df)} rows with columns: {df.columns.tolist()}")
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return False
    
    # Connect to database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(f"Connected to database: {db_path}")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False
    
    # Drop table if it already exists (to start fresh)
    cursor.execute("DROP TABLE IF EXISTS playerlist")
    conn.commit()
    
    # Create new playerlist table with appropriate schema
    create_table_sql = """
    CREATE TABLE playerlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        club INTEGER,
        idnumber INTEGER,
        name TEXT,
        cluborig INTEGER,
        rating INTEGER,
        f_elo INTEGER,
        b_elo INTEGER,
        titular TEXT
    )
    """
    
    try:
        cursor.execute(create_table_sql)
        conn.commit()
        print("Created playerlist table")
    except Exception as e:
        print(f"Error creating table: {e}")
        conn.close()
        return False
    
    # Prepare data for insertion
    # Clean column names (remove spaces and special characters)
    column_mapping = {
        'club': 'club',
        'idnumber': 'idnumber',
        'name': 'name',
        'cluborig': 'cluborig',
        'rating': 'rating',
        'F ELO': 'f_elo',
        'B ELO': 'b_elo',
        'Titular': 'titular'
    }
    
    # Rename columns to match database schema
    df_clean = df.rename(columns=column_mapping)
    
    # Convert data types appropriately
    # For the 'name' column, handle encoding issues (like Tomßs)
    df_clean['name'] = df_clean['name'].astype(str)
    
    # Replace NaN with None for database insertion
    df_clean = df_clean.where(pd.notnull(df_clean), None)
    
    # Insert data row by row
    insert_sql = """
    INSERT INTO playerlist (club, idnumber, name, cluborig, rating, f_elo, b_elo, titular)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    try:
        for index, row in df_clean.iterrows():
            cursor.execute(insert_sql, (
                int(row['club']) if row['club'] is not None else None,
                int(row['idnumber']) if row['idnumber'] is not None else None,
                row['name'],
                int(row['cluborig']) if row['cluborig'] is not None else None,
                int(row['rating']) if row['rating'] is not None else None,
                int(row['f_elo']) if row['f_elo'] is not None else None,
                int(row['b_elo']) if row['b_elo'] is not None else None,
                row['titular']
            ))
        
        conn.commit()
        print(f"Successfully inserted {len(df_clean)} rows into playerlist table")
        
        # Verify data
        cursor.execute("SELECT COUNT(*) FROM playerlist")
        count = cursor.fetchone()[0]
        print(f"Verification: {count} rows in playerlist table")
        
        # Show sample data
        cursor.execute("SELECT * FROM playerlist LIMIT 5")
        sample = cursor.fetchall()
        print("\nSample data from playerlist table:")
        for row in sample:
            print(row)
        
        return True
        
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
        print("Database connection closed")


if __name__ == "__main__":
    print("Starting playerlist import...\n")
    success = import_playerlist()
    if success:
        print("\nImport completed successfully!")
    else:
        print("\nImport failed!")
