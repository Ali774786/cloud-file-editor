import boto3
import os
import pandas as pd
from io import StringIO, BytesIO
from botocore.exceptions import ClientError
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# S3 Configuration
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'your-bucket-name')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
PARENT_FOLDER = os.environ.get('S3_PARENT_FOLDER', 'test')


def get_s3_client():
    """Create and return an S3 client"""
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

def list_process_folders():
    """List all process ID folders in the test directory"""
    try:
        s3_client = get_s3_client()
        prefix = f"{PARENT_FOLDER}/"
        response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET_NAME,
            Prefix=prefix,
            Delimiter='/'
        )

        folders = []
        if 'CommonPrefixes' in response:
            for obj in response['CommonPrefixes']:
                folder_path = obj['Prefix']
                # Extract just the folder name from the path
                folder_name = folder_path.rstrip('/').split('/')[-1]
                folders.append(folder_name)
        
        return folders
    except ClientError as e:
        logger.error(f"Error listing process folders: {e}")
        return []

def list_tsv_files(process_id):
    """List all TSV files in a specific process folder"""
    try:
        s3_client = get_s3_client()
        prefix = f"{PARENT_FOLDER}/{process_id}/"
        response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET_NAME,
            Prefix=prefix
        )

        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                file_path = obj['Key']
                # Skip if it's the folder itself or not a TSV file
                if file_path.endswith('/') or not file_path.endswith('.tsv'):
                    continue
                
                # Extract just the file name
                file_name = file_path.split('/')[-1]
                files.append({
                    'name': file_name,
                    'path': file_path,
                    'size': obj['Size'],
                    'last_modified': obj['LastModified']
                })
        
        return files
    except ClientError as e:
        logger.error(f"Error listing TSV files for process {process_id}: {e}")
        return []

def read_tsv_file(file_path):
    """Read a TSV file from S3 and return its contents as a pandas DataFrame"""
    try:
        s3_client = get_s3_client()
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_path)
        content = response['Body'].read().decode('utf-8')
        
        # Parse the TSV content
        df = pd.read_csv(StringIO(content), sep='\t')
        return df
    except ClientError as e:
        logger.error(f"Error reading TSV file {file_path}: {e}")
        return None

def save_updated_tsv(file_path, df):
    """
    Save updated DataFrame as a new TSV file with _latest appended to filename
    
    Args:
        file_path: Original file path in S3
        df: Pandas DataFrame with updated data
    
    Returns:
        bool: Success or failure
    """
    try:
        # Generate the new filename with _latest suffix
        path_parts = file_path.rsplit('.', 1)
        if len(path_parts) == 2:
            new_file_path = f"{path_parts[0]}_latest.{path_parts[1]}"
        else:
            new_file_path = f"{file_path}_latest"
        
        # Convert DataFrame to TSV string
        tsv_buffer = StringIO()
        df.to_csv(tsv_buffer, sep='\t', index=False)
        
        # Upload to S3
        s3_client = get_s3_client()
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=new_file_path,
            Body=tsv_buffer.getvalue()
        )
        
        logger.info(f"Successfully saved updated file to {new_file_path}")
        return True, new_file_path
    except Exception as e:
        logger.error(f"Error saving updated TSV file: {e}")
        return False, None 