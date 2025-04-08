#!/usr/bin/env python3
"""
Database initialization script for CSV Cloud File Editor.
This script:
1. Creates the database (if it doesn't exist)
2. Creates the tables
3. Optionally loads sample data
"""

import os
import sys
from sqlalchemy_utils import database_exists, create_database
from app import create_app, db
from app.models.csv_data import CSVData
from app.utils import parse_csv, save_csv_data_to_db

def init_db(load_sample_data=False):
    """Initialize the database"""
    app = create_app()
    with app.app_context():
        # Check if database exists, if not create it
        if not database_exists(db.engine.url):
            create_database(db.engine.url)
            print(f"Created database: {db.engine.url}")
        
        # Create tables
        db.create_all()
        print("Created database tables")
        
        # Load sample data if requested
        if load_sample_data:
            # Check if there's already data
            if CSVData.query.count() > 0:
                print("Database already contains data. Skipping sample data import.")
                return
            
            # Import sample data
            try:
                sample_file = 'sample_data.csv'
                if os.path.exists(sample_file):
                    df = parse_csv(sample_file)
                    count = save_csv_data_to_db(df)
                    print(f"Imported {count} sample records")
                else:
                    print(f"Sample file {sample_file} not found")
            except Exception as e:
                print(f"Error loading sample data: {str(e)}")

if __name__ == '__main__':
    # Check if sample data should be loaded
    load_sample = len(sys.argv) > 1 and sys.argv[1] == '--with-sample-data'
    init_db(load_sample_data=load_sample) 