import pandas as pd
from app import db
from app.models.csv_data import CSVData

def parse_file(file_path):
    """
    Parse a CSV or TSV file and return a pandas DataFrame
    """
    try:
        # Check file extension
        if file_path.lower().endswith('.tsv'):
            # Parse as TSV (tab-separated)
            df = pd.read_csv(file_path, sep='\t')
        else:
            # Default to CSV (comma-separated)
            df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise Exception(f"Error parsing file: {str(e)}")

def save_data_to_db(df):
    """
    Save data to the database
    """
    # Convert DataFrame to list of dicts
    records = df.to_dict(orient='records')
    
    try:
        # Clear existing data if needed
        # db.session.query(CSVData).delete()
        
        # Add new data
        for record in records:
            csv_data = CSVData(
                rank_by_target=record['rank_by_target'],
                target_system=record['target_system'],
                target_code=record['target_code'],
                target_name=record['target_name'],
                n_record=record['n_record'],
                n_patient=record['n_patient'],
                rank_by_source=record['rank_by_source'],
                source_system=record['source_system'],
                source_code=record['source_code'],
                source_name=record['source_name'],
                n_record_by_source=record['n_record_by_source'],
                n_patient_by_source=record['n_patient_by_source']
            )
            db.session.add(csv_data)
        
        db.session.commit()
        return len(records)
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error saving to database: {str(e)}")

def update_data(data_id, updated_data):
    """
    Update a specific data record
    """
    try:
        csv_data = CSVData.query.get(data_id)
        if not csv_data:
            return False, "Record not found"
        
        # Update each attribute directly, skip id field
        for key, value in updated_data.items():
            if key != 'id' and hasattr(csv_data, key):
                setattr(csv_data, key, value)
        
        db.session.commit()
        return True, "Record updated successfully"
    except Exception as e:
        db.session.rollback()
        return False, f"Error updating record: {str(e)}"

def get_all_data(page=1, per_page=10, search=None):
    """
    Get all data with pagination and optional search
    """
    query = CSVData.query
    
    # Implement search functionality if provided
    if search:
        # Search in multiple columns
        search_term = f"%{search}%"
        query = query.filter(
            (CSVData.target_system.ilike(search_term)) |
            (CSVData.target_name.ilike(search_term)) |
            (CSVData.source_system.ilike(search_term)) |
            (CSVData.source_code.ilike(search_term)) |
            (CSVData.source_name.ilike(search_term))
        )
    
    # Apply pagination
    pagination = query.order_by(CSVData.id).paginate(page=page, per_page=per_page, error_out=False)
    
    return pagination
