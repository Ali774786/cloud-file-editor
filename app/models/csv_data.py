from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

class CSVData(db.Model):
    __tablename__ = 'csv_data'

    id = db.Column(db.Integer, primary_key=True)
    rank_by_target = db.Column(db.Integer, nullable=False)
    target_system = db.Column(db.String(255), nullable=False)
    target_code = db.Column(db.Integer, nullable=False)
    target_name = db.Column(db.String(255), nullable=False)
    n_record = db.Column(db.Integer, nullable=False)
    n_patient = db.Column(db.Integer, nullable=False)
    rank_by_source = db.Column(db.Integer, nullable=False)
    source_system = db.Column(db.String(255), nullable=False)
    source_code = db.Column(db.String(255), nullable=False)
    source_name = db.Column(db.String(255), nullable=False)
    n_record_by_source = db.Column(db.Integer, nullable=False)
    n_patient_by_source = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CSVData {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'rank_by_target': self.rank_by_target,
            'target_system': self.target_system,
            'target_code': self.target_code,
            'target_name': self.target_name,
            'n_record': self.n_record,
            'n_patient': self.n_patient,
            'rank_by_source': self.rank_by_source,
            'source_system': self.source_system,
            'source_code': self.source_code,
            'source_name': self.source_name,
            'n_record_by_source': self.n_record_by_source,
            'n_patient_by_source': self.n_patient_by_source,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
