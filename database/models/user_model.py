from database.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import re
from sqlalchemy.orm import validates

class User(db.Model, UserMixin):
    __tablename__ = "user"
    
    id = db.Column('id', db.Integer, primary_key=True)  
    nome = db.Column('nome', db.String(150))
    sobrenome = db.Column('sobrenome', db.String(150))
    crp = db.Column('crp', db.String(20))
    abordagem = db.Column('abordagem', db.String(50))
    email = db.Column('email', db.String(50), unique=True)
    telefone = db.Column('telefone', db.String(15), unique=True, nullable=False)
    login = db.Column('login', db.String(50), unique=True, nullable=False)
    senha = db.Column('senha', db.String(550), nullable=False)
    tipo = db.Column('tipo', db.String(25), nullable=False, default="none")

    def __init__(self, nome, sobrenome, email, telefone, login, senha, crp=None, abordagem=None, tipo="atendente"):
        self.nome = nome
        self.sobrenome = sobrenome
        self.crp = crp or ''
        self.abordagem = abordagem or ''
        self.email = email
        self.telefone = telefone
        self.login = login
        self.senha = generate_password_hash(senha)
        self.tipo = tipo


    
    def verify_senha(self, pwd):
        return check_password_hash(self.senha, pwd)
    
    def __repr__(self):
        return f"User: {self._nome}"
    

    @validates('email')
    def validate_email(self, key, address):
        assert re.match(r'[^@]+@[^@]+\.[^@]+', address), "Email inválido."
        return address
    

    @validates('telefone')
    def validate_telefone(self, key, telefone):
        assert re.match(r'^\+?[0-9]{10,15}$', telefone), "Telefone inválido."
        return telefone
    

    def validate_crp(self, key, crp):
        if crp:
            assert re.match(r'^\d{2}/\d{3}\.\d{3}$', crp) or re.match(r'^\d{6,7}$', crp), "CRP inválido."
        return crp