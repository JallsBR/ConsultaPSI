from database.database import db

class PacienteConvenio(db.Model):
    __tablename__ = "pacienteconvenio"
    
    id = db.Column(db.Integer, primary_key=True)
    id_convenio = db.Column('id_convenio', db.Integer, db.ForeignKey('convenio.id'), nullable=False)
    documento = db.Column('documento', db.Text, nullable=False)
    autoriza_convenio = db.Column('autoriza_convenio', db.String(25), nullable=False, default="aguarde")
    paciente_id = db.Column('paciente_id', db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    
    def __init__(self, id_convenio, paciente_id, documento, autoriza_convenio):
        self.id_convenio = id_convenio
        self.paciente_id = paciente_id
        self.documento = documento
        self.autoriza_convenio = autoriza_convenio   

   

    def __repr__(self):
        return f"PacienteConvenio(id_convenio={self.id_convenio}, paciente_id={self.paciente_id}, autoriza_convenio={self.autoriza_convenio})"
