from flask import render_template, jsonify, request, flash, redirect, url_for
from app.s3_utils import (
    list_process_folders, 
    list_tsv_files, 
    read_tsv_file, 
    save_updated_tsv
)
import pandas as pd

def list_processes():
    """
    Display a list of all process ID folders
    """
    process_folders = list_process_folders()
    
    return render_template(
        's3/processes.html',
        process_folders=process_folders
    )

def list_files(process_id):
    """
    Display a list of TSV files for a specific process
    """
    files = list_tsv_files(process_id)
    
    return render_template(
        's3/files.html',
        process_id=process_id,
        files=files
    )

def view_file():
    """
    View the contents of a TSV file
    """
    file_path = request.args.get('file_path')
    if not file_path:
        flash('No file path provided', 'error')
        return redirect(url_for('s3.list_processes'))
    
    df = read_tsv_file(file_path)
    
    if df is None:
        flash('Error loading file from S3', 'error')
        # Extract process ID from file path to redirect back to files list
        path_parts = file_path.split('/')
        if len(path_parts) >= 3:
            process_id = path_parts[1]  # Assuming path format: test/process_id/filename.tsv
            return redirect(url_for('s3.list_files', process_id=process_id))
        else:
            return redirect(url_for('s3.list_processes'))
    
    # Get column names and prepare data for the template
    columns = df.columns.tolist()
    records = df.to_dict('records')
    
    # Get file name for display
    file_name = file_path.split('/')[-1]
    
    # Extract process_id from file_path
    path_parts = file_path.split('/')
    process_id = path_parts[1] if len(path_parts) >= 3 else "unknown"
    
    return render_template(
        's3/view_file.html',
        file_path=file_path,
        file_name=file_name,
        process_id=process_id,
        columns=columns,
        records=records,
        df_json=df.to_json(orient='records')
    )

def update_file():
    """
    Update a record in a file and save as a new file
    """
    if request.method != 'POST':
        return jsonify({'success': False, 'message': 'Method not allowed'}), 405
    
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    file_path = data.get('file_path')
    row_index = data.get('row_index')
    updated_row = data.get('updated_row')
    
    if not all([file_path, isinstance(row_index, int), updated_row]):
        return jsonify({'success': False, 'message': 'Missing required parameters'}), 400
    
    # Read the original file
    df = read_tsv_file(file_path)
    if df is None:
        return jsonify({'success': False, 'message': 'Failed to read file'}), 500
    
    # Update the specific row
    try:
        for column, value in updated_row.items():
            df.at[row_index, column] = value
        
        # Save the updated dataframe to a new file
        success, new_file_path = save_updated_tsv(file_path, df)
        
        if success:
            return jsonify({
                'success': True, 
                'message': 'File updated successfully',
                'new_file_path': new_file_path
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to save updated file'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error updating file: {str(e)}'}), 500 