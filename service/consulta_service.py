from database.models.consulta_model import Consulta
from database.models.paciente_model import Paciente  
from sqlalchemy import desc, asc
from database.database import db
from datetime import datetime

class ConsultaService:

    @staticmethod
    def create_consulta(data_marcacao, data_consulta, hora_consulta, duracao, consulta_status_id, convenios_id, id_paciente, psi_id):
        try:

            data_consulta_date = datetime.strptime(data_consulta, '%Y-%m-%d').date()
            hora_consulta_time = datetime.strptime(hora_consulta, '%H:%M').time()

            consulta = Consulta(
                data_marcacao=data_marcacao,
                data_consulta=data_consulta_date,
                hora_consulta=hora_consulta_time,
                duracao=duracao,
                consulta_status_id=consulta_status_id,
                convenios_id=convenios_id,
                id_paciente=id_paciente,
                psi_id=psi_id
            )
            print("SERVICE", consulta)
            db.session.add(consulta)
            db.session.commit()
            return True, "Consulta criada com sucesso."
        except Exception as e:
            db.session.rollback()
            print("Erro ao criar consulta:", str(e))
            return False, str(e)
        


    @staticmethod
    def get_consulta_pacientes():
        try:
            consultas = db.session.query(Consulta).join(Paciente).all()
            return consultas, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def update_consulta(id, data_consulta, hora_consulta, duracao, consulta_status_id, convenios_id):
        try:
            consulta = Consulta.query.get(id)
            if not consulta:
                return False, "Consulta não encontrada"

            consulta.data_consulta = data_consulta
            consulta.hora_consulta = hora_consulta
            consulta.duracao = duracao
            consulta.consulta_status_id = consulta_status_id
            consulta.convenios_id = convenios_id

            db.session.commit()
            return True, "Consulta atualizada com sucesso!"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_consulta(id):
        try:
            consulta = Consulta.query.get(id)
            if not consulta:
                return False, "Consulta não encontrada"

            db.session.delete(consulta)
            db.session.commit()
            return True, "Consulta excluída com sucesso!"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_all_consultas(psi_id=None):
        try:
            query = Consulta.query.order_by(desc(Consulta.id)).all()
            if psi_id:
                query = query.filter_by(psi_id=psi_id)
            consultas = query.all()
            return consultas, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_consulta_by_id(id):
        try:
            consulta = Consulta.query.get(id)
            if not consulta:
                return None, "Consulta não encontrada"
            return consulta, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_consultas_by_psi_id(psi_id):
        try:
            consultas = Consulta.query.filter_by(psi_id=psi_id).all()
            return consultas, None
        except Exception as e:
            return None, str(e)


    @staticmethod
    def get_consulta_pacientes_por_id(id_paciente):
        try:
            consultas = (
                db.session.query(Consulta)
                .join(Paciente)
                .filter(Consulta.id_paciente == id_paciente)
                .order_by(Consulta.id.desc())
                .all()
            )
            return consultas, None
        except Exception as e:
            return None, str(e)
        
        

    @staticmethod
    def get_consultas_by_date_range(start_date, end_date, psi_id=None):
        try:
            # Filtro de consultas pelo intervalo de datas e ID do psicólogo (se fornecido)
            query = Consulta.query.filter(Consulta.data_consulta.between(start_date, end_date))
            
            if psi_id:
                query = query.filter_by(psi_id=psi_id)
            
            # Ordenar os resultados pela data da consulta em ordem ascendente
            consultas = query.order_by(asc(Consulta.data_consulta)).all()
            return consultas, None
        except Exception as e:
            return None, str(e)



    @staticmethod
    def get_relatorio_convenio_e_ganhos(psi_id):
        try:
            # Obtém todas as consultas filtradas pelo psi_id
            consultas = Consulta.query.filter_by(psi_id=psi_id).all()
            relatorio = {}
            ganhos_totais = 0.0
            
            # Itera sobre as consultas para agrupar por convênio
            for consulta in consultas:
                # Se o convênio existir, usa seu nome e valor; caso contrário, usa 'Particular'
                if consulta.convenio:
                    convenio_nome = consulta.convenio.convenio
                    valor_consulta = consulta.convenio.valor_consulta
                else:
                    convenio_nome = 'Não informado'
                    valor_consulta = 'Não informado'
                # Agrupando as consultas pelo nome do convênio
                if convenio_nome not in relatorio:
                    relatorio[convenio_nome] = {'quantidade': 0, 'ganhos': 0.0}
                
                relatorio[convenio_nome]['quantidade'] += 1
                relatorio[convenio_nome]['ganhos'] += valor_consulta
                ganhos_totais += valor_consulta
            
            # Serializa o resultado
            relatorio_serializado = [
                {'convenio': convenio, 'quantidade': dados['quantidade'], 'ganhos': dados['ganhos']}
                for convenio, dados in relatorio.items()
            ]
            
            return relatorio_serializado, ganhos_totais
        except Exception as e:
            return None, str(e)