from database.models.convenio_model import Convenio
from database.database import db

class ConvenioService:

    @staticmethod
    def create_convenio(convenio_nome, valor_consulta, user_id=None):
        try:
            convenio = Convenio(convenio_nome, valor_consulta, user_id)
            db.session.add(convenio)
            db.session.commit()
            return True, "Convênio cadastrado com sucesso!"
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao cadastrar convênio: {str(e)}"
        

    @staticmethod
    def update_convenio(id, convenio_nome, valor_consulta):
        try:
            convenio = Convenio.query.get(id)
            if not convenio:
                return False, "Convênio não encontrado"
            
            convenio.convenio = convenio_nome
            convenio.valor_consulta = valor_consulta
            db.session.commit()
            return True, "Convênio atualizado com sucesso!"
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao atualizar convênio: {str(e)}"

    @staticmethod
    def delete_convenio(id):
        try:
            convenio = Convenio.query.get(id)
            if not convenio:
                return False, "Convênio não encontrado"
            
            db.session.delete(convenio)
            db.session.commit()
            return True, "Convênio excluído com sucesso!"
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao excluir convênio: {str(e)}"

    @staticmethod
    def get_all_convenios():
        try:
            convenios = Convenio.query.all()
            return convenios, None
        except Exception as e:
            return None, f"Erro ao buscar convênios: {str(e)}"
        
    @staticmethod
    def get_convenio_by_id(id):
        try:
            convenio = Convenio.query.get(id)
            if not convenio:
                return None, "Convênio não encontrado"
            return convenio, None
        except Exception as e:
            return None, f"Erro ao buscar convênio: {str(e)}"

    @staticmethod
    def get_convenios_by_user_id(user_id):
        try:
            convenios = Convenio.query.filter_by(user_id=user_id).all()
            if not convenios:
                return None, "Nenhum convênio encontrado para este usuário."
            return convenios, None
        except Exception as e:
            return None, f"Erro ao buscar convênios: {str(e)}"