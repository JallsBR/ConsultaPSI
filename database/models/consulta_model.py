from database.database import db
from datetime import datetime

class Consulta(db.Model):
    __tablename__ = 'consulta'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_marcacao = db.Column('data_marcacao', db.String(50), nullable=False)
    data_consulta = db.Column('data_consulta', db.Date, nullable=False)
    hora_consulta = db.Column('hora_consulta', db.Time, nullable=False)
    duracao = db.Column('duracao', db.String(8), nullable=False, default="00:50:00")
    consulta_status_id = db.Column('consulta_status_id', db.Integer, db.ForeignKey('status_consulta.id'), nullable=False)
    convenios_id = db.Column('convenios_id', db.Integer, db.ForeignKey('convenio.id'), nullable=False)
    id_paciente = db.Column('id_paciente', db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    psi_id = db.Column('psi_id', db.Integer, db.ForeignKey('user.id'), nullable=False)

    paciente = db.relationship('Paciente', backref='consultas')
    convenio = db.relationship('Convenio', backref='consultas')
    psi = db.relationship('User', backref='consultas')
    status = db.relationship('StatusConsulta', backref='consultas')


    def __init__(self, data_marcacao, data_consulta, hora_consulta, duracao, consulta_status_id, id_paciente, convenios_id, psi_id):
        self.data_marcacao = data_marcacao
        self.data_consulta = data_consulta
        self.hora_consulta = hora_consulta
        self.duracao = duracao
        self.consulta_status_id = consulta_status_id
        self.id_paciente = id_paciente
        self.convenios_id = convenios_id
        self.psi_id = psi_id
    

    def __repr__(self):
        return f"Consulta(id={self.id}, data_marcacao={self.data_marcacao}, data_consulta={self.data_consulta}, hora_consulta={self.hora_consulta}, duracao={self.duracao}, consulta_status_id={self.consulta_status_id}, convenios_id={self.convenios_id}, id_paciente={self.id_paciente}, psi_id={self.psi_id})"
