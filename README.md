# Cloud File Editor

A Flask web application that allows you to work directly with CSV and TSV files stored in Amazon S3 buckets.

## Features

- Direct S3 integration for file management
  - Browse folders and files in S3 buckets
  - View and edit TSV files directly from S3
  - Changes saved as new files with _latest suffix
- Interactive data table with:
  - In-place row editing
  - Search functionality
  - Cancel/save operations
- Responsive web UI
- Modular architecture with separated views and URLs

## Requirements

- Python 3.8+
- AWS account with S3 bucket access
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository or download the source code.

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure AWS credentials:

   Set the following environment variables:

   ```bash
   export S3_BUCKET_NAME=your-bucket-name
   export AWS_ACCESS_KEY_ID=your-access-key
   export AWS_SECRET_ACCESS_KEY=your-secret-key
   export AWS_REGION=your-region  # e.g., us-east-1
   ```

   Or create a `.env` file with these variables.

## S3 Structure Requirements

This application expects a specific S3 structure:

```
bucket-name/
└── test/
    ├── process_id_1/
    │   ├── file1.tsv
    │   ├── file2.tsv
    │   └── ...
    ├── process_id_2/
    │   ├── file1.tsv
    │   └── ...
    └── ...
```

- A parent folder named `test` 
- Inside `test`, multiple subfolders named after process IDs
- Each process ID folder contains `.tsv` files

## Running the Application

Start the application:

```bash
flask run
```

or

```bash
python app.py
```

Visit http://127.0.0.1:8080/ in your browser to access the application.

## Usage

1. **Browse S3 Files**:
   - Click on "S3 Browser" in the navigation menu
   - Select a process folder
   - Choose a TSV file to view and edit

2. **Edit S3 Files**:
   - Click on any cell in the table to edit its value
   - Use the "Save" button to commit changes
   - Use the "Cancel" button to discard changes
   - When saved, changes will be written to a new file with "_latest" appended to the name

3. **Search Within Files**:
   - Use the search box to filter data within a file

## Project Structure

```
flask_csv_app/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── s3_utils.py          # S3 utility functions
│   ├── routes/              # URL routing
│   │   ├── __init__.py
│   │   └── s3_urls.py       # S3 URL definitions
│   ├── views/               # View functions
│   │   ├── __init__.py
│   │   └── s3_views.py      # S3 view logic
│   ├── static/              # Static files
│   │   └── css/             # CSS stylesheets
│   │       └── styles.css   # Main stylesheet
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template
│   │   └── s3/              # S3 Templates
│   │       ├── processes.html # Process folders list
│   │       ├── files.html     # TSV files list
│   │       └── view_file.html # TSV file viewer/editor
│   └── utils.py             # Utility functions
├── venv/                     # Virtual environment
├── app.py                    # Application entry point
├── requirements.txt          # Project dependencies
└── README.md                 # This file
```

## Environment Variables

- `S3_BUCKET_NAME`: Name of your S3 bucket
- `AWS_ACCESS_KEY_ID`: AWS access key with S3 permissions
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_REGION`: AWS region where your bucket is located
- `SECRET_KEY`: Secret key for session security

## License

This project is licensed under the MIT License.
