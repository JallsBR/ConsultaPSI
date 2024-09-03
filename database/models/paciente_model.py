from database.database import db

class Paciente(db.Model):
    __tablename__ = 'paciente'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    nascimento = db.Column(db.Date, nullable=False)  
    genero = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    ocupacao = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    endereco = db.Column(db.String(150), nullable=False)
    endereco_complemento = db.Column(db.String(150), nullable=False)
    fone = db.Column(db.String(15), nullable=False)
    datainicio = db.Column(db.Date, nullable=False)  
    convenios_id = db.Column(db.Integer, db.ForeignKey('convenio.id'), nullable=True)  
    
    def __init__(self, nome, sobrenome, cpf, nascimento, genero, email, ocupacao, cep,endereco, endereco_complemento, fone, datainicio):
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf
        self.nascimento = nascimento
        self.genero = genero
        self.email = email
        self.ocupacao = ocupacao
        self.cep = cep
        self.endereco = endereco
        self.endereco_complemento = endereco_complemento
        self.fone = fone
        self.datainicio = datainicio


    

    def __repr__(self):
        return f"Paciente(id={self.id}, nome={self.nome}, sobrenome={self.sobrenome}, cpf={self.cpf})"