from database.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from database.models.user_model import User
from database.models.paciente_model import Paciente
from database.models.consulta_model import Consulta
from database.models.convenio_model import Convenio

class UserService:
    
    @staticmethod
    def create_user(nome, sobrenome, email, telefone, login, senha, tipo):
        try:
            user = User(
                nome=nome,
                sobrenome=sobrenome,                
                email=email,
                telefone=telefone,
                login=login,
                senha=senha,
                tipo=tipo,
                crp= '',
                abordagem= ''
            )
            db.session.add(user)
            db.session.commit()
            return True, "Usuário cadastrado com sucesso!"
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def update_user(id, nome=None, sobrenome=None, crp=None, abordagem=None, email=None, telefone=None, login=None, senha=None,  tipo=None):
        
        try:
            user = User.query.get(id)
            if not user:
                return False, "Usuário não encontrado"

            if nome:
                user.nome = nome
            if sobrenome:
                user.sobrenome = sobrenome
            if crp:
                user.crp = crp
            if abordagem:
                user.abordagem = abordagem
            if email:
                user.email = email
            if telefone:
                user.telefone = telefone
            if login:
                user.login = login
            if senha:
                user.senha = generate_password_hash(senha)
            if tipo:
                user.tipo = tipo

            db.session.commit()
            return True, "Usuário alterado com sucesso"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def serialize_user(user):
        return {
            "id": user.id,
            "nome": user.nome,
            "sobrenome": user.sobrenome,
            "crp": user.crp,
            "abordagem": user.abordagem,
            "email": user.email,
            "telefone": user.telefone,
            "login": user.login,
            "tipo": user.tipo
        }

    @staticmethod
    def get_all_users(id=None):
        try:
            if id:
                user = User.query.get(id)
                if user:
                    return UserService.serialize_user(user), None
                else:
                    return None, "Usuário não encontrado"
            else:
                users = User.query.all()
                serialized_users = [UserService.serialize_user(user) for user in users]
                return serialized_users, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def delete_user(id):
        try:
            user = User.query.get(id)
            if not user:
                return False, "Usuário não encontrado"
            
            db.session.delete(user)
            db.session.commit()
            return True, "Usuário excluído com sucesso"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_pacientes_do_user(id):
        try:
            # Verifica se o usuário existe
            user = User.query.get(id)
            if not user:
                return None, "Usuário não encontrado."

            # Busca os pacientes que têm consultas associadas ao usuário
            pacientes = db.session.query(
                Paciente.id,
                Paciente.nome,
                Paciente.sobrenome,
                Paciente.convenios_id,
                Convenio.convenio,
                User.nome.label("user_nome")
            ).join(Consulta, Paciente.id == Consulta.id_paciente) \
            .join(Convenio, Paciente.convenios_id == Convenio.id) \
            .join(User, Consulta.psi_id == User.id) \
            .filter(Consulta.psi_id == id) \
            .all()
            
            return pacientes, None
        
        except Exception as e:
            return None, str(e)
