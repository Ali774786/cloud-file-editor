from flask import request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.csv_data import CSVData
from app.utils import update_data, parse_file, save_data_to_db, get_all_data
import os
import tempfile

def get_data():
    """
    Home page - display data in a table with pagination
    """
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', None)
    per_page = 10
    
    pagination = get_all_data(page=page, per_page=per_page, search=search)
    records = pagination.items
    
    # If there are records, get column names from the first record
    columns = []
    if records and len(records) > 0:
        # Get all columns but filter out internal SQLAlchemy attributes, metadata, and id 
        # (since we already display id in the first column)
        all_columns = [c for c in list(records[0].__dict__.keys()) 
                   if not c.startswith('_') and c != 'metadata' and c != 'id']
        
        # Move timestamp columns to the end
        standard_columns = [c for c in all_columns if c not in ['created_at', 'updated_at']]
        timestamp_columns = [c for c in all_columns if c in ['created_at', 'updated_at']]
        columns = standard_columns + timestamp_columns
    
    # Create a dictionary to map actual column names to title-cased display names
    column_display_names = {col: col.replace('_', ' ').title() for col in columns}
    
    return render_template('index.html', 
                          records=records, 
                          pagination=pagination,
                          columns=columns,
                          column_display_names=column_display_names,
                          search=search,
                          getattr=getattr)

def upload_csv():
    """
    Upload and process a CSV or TSV file
    """
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['csv_file']
        
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        # Check if the file is CSV or TSV
        if file and (file.filename.lower().endswith('.csv') or file.filename.lower().endswith('.tsv')):
            # Save the file temporarily
            extension = '.tsv' if file.filename.lower().endswith('.tsv') else '.csv'
            fd, temp_path = tempfile.mkstemp(suffix=extension)
            file.save(temp_path)
            
            try:
                # Parse the file
                df = parse_file(temp_path)
                
                # Save to database
                record_count = save_data_to_db(df)
                
                flash(f'Successfully imported {record_count} records', 'success')
                return redirect(url_for('api.index'))
            
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
            
            finally:
                # Clean up the temporary file
                os.close(fd)
                os.remove(temp_path)
        
        else:
            flash('File must be a CSV or TSV', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

def update_record(record_id):
    """
    Update a specific record via API
    """
    try:
        record = CSVData.query.get(record_id)
        if not record:
            return jsonify({'success': False, 'message': 'Record not found'}), 404
        
        data = request.json
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        # Update record with new data
        success, message = update_data(record_id, data)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'message': message}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500 