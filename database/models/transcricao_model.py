from database.database import db

class Transcricao(db.Model):
    __tablename__ = 'transcricao'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_consulta = db.Column(db.Integer, db.ForeignKey('consulta.id'), nullable=False)
    transcricao = db.Column(db.String, nullable=False)
    data_transcricao = db.Column(db.String(50), nullable=False)
    psi_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    palavras_chave = db.relationship('PalavrasChave', back_populates='transcricao', cascade="all, delete-orphan")

    def __init__(self, id_consulta, transcricao, data_transcricao, psi_id):
        self.id_consulta = id_consulta
        self.transcricao = transcricao
        self.data_transcricao = data_transcricao
        self.psi_id = psi_id

    def __repr__(self):
        return f"Transcrição: {self.id}"
