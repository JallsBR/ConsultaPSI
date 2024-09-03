from database.database import db

class PalavrasChave(db.Model):
    __tablename__ = 'palavras_chave'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_transcricao = db.Column(db.Integer, db.ForeignKey('transcricao.id'), nullable=False)
    palavra = db.Column(db.String(30))
    psi_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    transcricao = db.relationship("Transcricao", back_populates="palavras_chave")

    def __init__(self, id_transcricao, palavra, psi_id):
        self.id_transcricao = id_transcricao
        self.palavra = palavra
        self.psi_id = psi_id

    

    def __repr__(self):
        return f"Palavra: {self.palavra}"
