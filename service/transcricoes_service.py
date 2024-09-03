from database.models.transcricao_model import Transcricao
from database.models.consulta_model import Consulta
from database.models.paciente_model import Paciente
from database.database import db

class TranscricaoService:

    @staticmethod
    def create_transcricao(id_consulta, transcricao, psi_id ,data_transcricao):
        print(f"Recebido: {id_consulta}, {transcricao}, {psi_id}, {data_transcricao}")  
        try:
            nova_transcricao = Transcricao(
                id_consulta=id_consulta,
                transcricao=transcricao,
                data_transcricao=data_transcricao,
                psi_id = psi_id 
            )
            db.session.add(nova_transcricao)
            db.session.commit()
            return True, "Transcrição criada com sucesso."
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_transcricao_faltantes():
        try:
            transcritas_subquery = db.session.query(Transcricao.id_consulta).subquery()
            consultas = db.session.query(
                Consulta.id,
                Consulta.data_consulta,
                Paciente.nome
            ).join(Paciente).filter(~Consulta.id.in_(transcritas_subquery)).all()
            
            result = [{'id': c.id, 'data_consulta': c.data_consulta, 'nome_paciente': c.nome} for c in consultas]
            return result, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_all_transcricoes():
        try:
            transcricoes = db.session.query(
                Transcricao.id,
                Consulta.data_consulta,
                Paciente.nome,
                Transcricao.transcricao
            ).join(Consulta).join(Paciente, Consulta.id_paciente == Paciente.id).all()
            return transcricoes, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_transcricao_by_id(id):
        try:
            transcricao = Transcricao.query.get(id)
            return transcricao, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def update_transcricao(id, id_consulta, nova_transcricao, data_transcricao, psi_id):
        try:
            transcricao = Transcricao.query.get(id)
            if transcricao:
                transcricao.id_consulta = id_consulta
                transcricao.transcricao = nova_transcricao
                transcricao.data_transcricao = data_transcricao
                transcricao.psi_id = psi_id
                db.session.commit()
                return True, "Transcrição atualizada com sucesso."
            else:
                return False, "Transcrição não encontrada."
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_transcricao(id):
        try:
            transcricao = Transcricao.query.get(id)
            if transcricao:
                db.session.delete(transcricao)
                db.session.commit()
                return True, "Transcrição excluída com sucesso."
            else:
                return False, "Transcrição não encontrada."
        except Exception as e:
            db.session.rollback()
            return False, str(e)
