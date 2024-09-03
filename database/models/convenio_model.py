from database.database import db

class Convenio(db.Model):
    __tablename__ = "convenio"
    
    id = db.Column(db.Integer, primary_key=True)
    convenio = db.Column('convenio', db.String(150), unique=True, nullable=False)
    valor_consulta = db.Column('valor_consulta', db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, convenio, valor_consulta, user_id):
        self.convenio = convenio
        self.valor_consulta = valor_consulta
        self.user_id = user_id

   

    def __repr__(self):
        return f"Convênio: {self.convenio}, Valor Consulta: {self.valor_consulta}"
