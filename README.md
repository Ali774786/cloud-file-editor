# Cloud File Editor

A Flask web application that allows you to import CSV and TSV files, store the data in a PostgreSQL database, and perform CRUD operations through a web interface.

## Features

- File upload and import (supports CSV and TSV formats)
- PostgreSQL database integration
- Interactive data table with:
  - In-place row editing
  - Pagination
  - Search functionality
- Responsive web UI
- Modular architecture with separated views and URLs

## Requirements

- Python 3.8+
- PostgreSQL
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

4. Set up the PostgreSQL database:
   - Create a database named `flask_csv`
   - Make sure the database user credentials match those in the app config:

     ```python
     # Default in app/__init__.py
     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/flask_csv'
     ```

   - Or set the `DATABASE_URL` environment variable to your connection string

5. Initialize the database:

   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

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

1. **Upload File**:
   - Navigate to "Upload File" in the navigation menu
   - Select a CSV (.csv) or TSV (.tsv) file from your computer
   - Click "Upload and Process"

2. **View and Edit Data**:
   - The home page displays your data in a table
   - Click on any cell to edit its value
   - Use the "Save" button to commit changes
   - Use the "Cancel" button to discard changes

3. **Search and Pagination**:
   - Use the search box to filter data
   - Use pagination controls to navigate through large datasets

## Supported File Formats

- **CSV** (Comma-Separated Values): Files with `.csv` extension where values are separated by commas
- **TSV** (Tab-Separated Values): Files with `.tsv` extension where values are separated by tabs

## Project Structure

```
flask_csv_app/
├── app/
│   ├── __init__.py           # Flask application factory
│   ├── models/               # Database models
│   │   ├── __init__.py
│   │   └── csv_data.py       # Data model
│   ├── routes/               # URL routing
│   │   ├── __init__.py
│   │   └── urls.py           # URL definitions
│   ├── views/                # View functions
│   │   ├── __init__.py
│   │   └── views.py          # View logic
│   ├── templates/            # HTML templates
│   │   ├── base.html         # Base template
│   │   ├── index.html        # Data display page
│   │   └── upload.html       # File upload page
│   └── utils.py              # Utility functions
├── migrations/               # Database migrations
├── venv/                     # Virtual environment
├── app.py                    # Application entry point
├── requirements.txt          # Project dependencies
└── README.md                 # This file
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for session security

## License

This project is licensed under the MIT License. 

