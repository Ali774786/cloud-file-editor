from app import create_app, db
from app.models.csv_data import CSVData

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Add database and models to flask shell context"""
    return {'db': db, 'CSVData': CSVData}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 