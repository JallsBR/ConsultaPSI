from database.models.paciente_model import Paciente
from database.models.consulta_model import Consulta
from database.models.transcricao_model import Transcricao
from database.database import db
from datetime import datetime

class PacienteService:

    @staticmethod
    def create_paciente(nome, sobrenome, cpf, nascimento, genero, email, ocupacao, cep, endereco, endereco_complemento, fone, datainicio):
        print(f"Recebido: {nome}, {sobrenome}, {cpf}, {nascimento}, {genero}, {email}, {ocupacao}, {cep}, {endereco}, {endereco_complemento}, {fone}, {datainicio}")
        try:
            nascimento_date = datetime.strptime(nascimento, '%Y-%m-%d').date()
            datainicio_date = datetime.strptime(datainicio, '%d/%m/%Y').date()
            paciente = Paciente(
                nome=nome,
                sobrenome=sobrenome,
                cpf=cpf,
                nascimento= nascimento_date,
                genero=genero,
                email=email,
                ocupacao=ocupacao,
                cep=cep,
                endereco=endereco,
                endereco_complemento=endereco_complemento,
                fone=fone,
                datainicio=datainicio_date
            )
            db.session.add(paciente)
            db.session.commit()
            return True, "Paciente cadastrado com sucesso!"
        except Exception as e:
            print(e)
            db.session.rollback()
            return False, str(e)
        

    def update_paciente(id, nome, sobrenome, cpf, nascimento, genero, email, ocupacao, cep, endereco, endereco_complemento, fone):
        try:
            paciente = Paciente.query.get(id)
            if not paciente:
                return False, "Paciente não encontrado"

            nascimento_date = datetime.strptime(nascimento, '%Y-%m-%d').date()

            paciente.nome = nome
            paciente.sobrenome = sobrenome
            paciente.cpf = cpf
            paciente.nascimento = nascimento_date
            paciente.genero = genero
            paciente.email = email
            paciente.ocupacao = ocupacao
            paciente.cep = cep
            paciente.endereco = endereco
            paciente.endereco_complemento = endereco_complemento
            paciente.fone = fone

            db.session.commit()
            return True, "Paciente atualizado com sucesso!"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
        
        

    @staticmethod
    def delete_paciente(id):
        try:
            paciente = Paciente.query.get(id)
            if not paciente:
                return False, "Paciente não encontrado"

            db.session.delete(paciente)
            db.session.commit()
            return True, "Paciente excluído com sucesso!"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_all_pacientes():
        try:
            return Paciente.query.all(), None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_paciente_by_id(id):
        try:
            paciente = Paciente.query.get(id)
            if not paciente:
                return None, "Paciente não encontrado"
            return paciente, None
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def get_all_pacientes_with_consultas_transcricoes():
        try:
            pacientes = db.session.query(Paciente).all()
            pacientes_com_detalhes = []
            
            for paciente in pacientes:
                consultas = db.session.query(Consulta).filter_by(id_paciente=paciente.id).all()
                for consulta in consultas:
                    transcricao = db.session.query(Transcricao).filter_by(id_consulta=consulta.id).first()
                    consulta.transcricao = transcricao 

                paciente.consultas = consultas 
                pacientes_com_detalhes.append(paciente)
            
            return pacientes_com_detalhes, None
        except Exception as e:
            return [], str(e)
    
    """
    @staticmethod
    def get_all_pacientes_with_consultas_transcricoes_por_psi(psi_id=None):
        try:
            query = db.session.query(Paciente)
            
            if psi_id:
                query = query.filter(Paciente.psi_id == psi_id)
            
            pacientes = query.all()
            pacientes_com_detalhes = []
            
            for paciente in pacientes:
                consultas = db.session.query(Consultas).filter_by(id_paciente=paciente.id).all()
                for consulta in consultas:
                    transcricao = db.session.query(Transcricoes).filter_by(id_consulta=consulta.id).first()
                    consulta.transcricao = transcricao 

                paciente.consultas = consultas 
                pacientes_com_detalhes.append(paciente)
            
            return pacientes_com_detalhes, None  
        
        except Exception as e:
            return [], str(e)

    """