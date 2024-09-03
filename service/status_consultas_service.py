from database.models.status_consulta_model import StatusConsulta
from database.database import db

class StatusConsultaService:

    @staticmethod
    def create_status_consulta(status):
        try:
            status_consulta = StatusConsulta(status)
            db.session.add(status_consulta)
            db.session.commit()
            return True, "Status de consulta cadastrado com sucesso!"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def update_status_consulta(id, status):
        try:
            status_consulta = StatusConsulta.query.get(id)
            if not status_consulta:
                return False, "Status de consulta não encontrado"

            status_consulta.status = status
            db.session.commit()
            return True, "Status de consulta atualizado com sucesso!"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_status_consulta(id):
        try:
            status_consulta = StatusConsulta.query.get(id)
            if not status_consulta:
                return False, "Status de consulta não encontrado"
            
            db.session.delete(status_consulta)
            db.session.commit()
            return True, "Status de consulta excluído com sucesso!"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_status_consulta_by_id(id):
        try:
            status_consulta = StatusConsulta.query.get(id)
            if not status_consulta:
                return None, "Status de consulta não encontrado"
            return status_consulta, None
        except Exception as e:
            return None, str(e)
    @staticmethod
    def get_all_status_consultas():
        try:
            status_consultas = StatusConsulta.query.all()
            return status_consultas, None
        except Exception as e:
            return None, str(e)
