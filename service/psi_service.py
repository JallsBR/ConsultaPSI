from database.models.convenio_model import Convenio
from database.models.user_model import User
from database.models.paciente_model import Paciente
from database.models.consulta_model import Consulta
from werkzeug.security import generate_password_hash
from database.database import db

class PsiService:
    
      

    @staticmethod
    def update_psi(id, nome=None, sobrenome=None, crp=None, abordagem=None, email=None, telefone=None, login=None, senha=None):
        try:
            psi = User.query.get(id)
            if not psi or psi.tipo != "psicólogo":
                return False, "Psicólogo não encontrado"

            if nome and nome != psi.nome:
                psi.nome = nome
            if sobrenome and sobrenome != psi.sobrenome:
                psi.sobrenome = sobrenome
            if crp and crp != psi.crp:
                psi.crp = crp
            if abordagem and abordagem != psi.abordagem:
                psi.abordagem = abordagem
            if email and email != psi.email: 
                psi.email = email
            if telefone and telefone != psi.telefone:
                psi.telefone = telefone
            if login and login != psi.login:
                psi.login = login
            if senha and generate_password_hash(senha) != psi.senha:
                psi.senha = generate_password_hash(senha)

            db.session.commit()
            return True, "Psicólogo alterado com sucesso"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def serialize_psi(psi):
        return {
            "id": psi.id,
            "nome": psi.nome,
            "sobrenome": psi.sobrenome,
            "crp": psi.crp,
            "abordagem": psi.abordagem,
            "email": psi.email,
            "telefone": psi.telefone,
            "login": psi.login,
            "tipo": psi.tipo
        }

    @staticmethod
    def get_all_psis(id=None):
        try:
            if id:
                psi = User.query.filter_by(id=id, tipo="psicólogo").first()
                if psi:
                    return PsiService.serialize_psi(psi), None
                else:
                    return None, "Psicólogo não encontrado"
            else:
                psis = User.query.filter_by(tipo="psicólogo").all()
                serialized_psis = [PsiService.serialize_psi(psi) for psi in psis]
                return serialized_psis, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_pacientes_do_psi(id):  
    
        try:

            psi = User.query.filter_by(id=id, tipo="psicologo").first()
            if not psi:
                return None, "Psicólogo não encontrado."

            # Busca os pacientes que têm consultas associadas ao psicólogo
            pacientes = db.session.query(
                Paciente.id,
                Paciente.nome,
                Paciente.sobrenome,
                Paciente.convenios_id,
                Convenio.convenio,
                User.nome.label("psi_nome")
            ).join(Consulta, Paciente.id == Consulta.id_paciente) \
            .join(Convenio, Paciente.convenios_id == Convenio.id) \
            .join(User, Consulta.psi_id == User.id) \
            .filter(Consulta.psi_id == id) \
            .all()
            
            return pacientes, None
        
        except Exception as e:
            return None, str(e)