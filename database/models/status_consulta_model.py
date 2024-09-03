from database.database import db

class StatusConsulta(db.Model):
    __tablename__ = 'status_consulta'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(50), nullable=False)
    
    def __init__(self, status):
        self.status = status

    

    def __repr__(self):
        return f"Status: {self.status}"
