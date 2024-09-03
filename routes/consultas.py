from flask import Blueprint, render_template, request, redirect, flash
from service.consulta_service import ConsultaService
from service.paciente_service import PacienteService
from service.psi_service import PsiService
from service.convenio_service import ConvenioService
from service.status_consultas_service import StatusConsultaService
import locale
from datetime import datetime


blueprint_consultas = Blueprint("consultas", __name__, template_folder="templates")
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
agora = datetime.now().strftime('%d/%m/%Y')


@blueprint_consultas.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        psicologos, error = PsiService.get_all_psis()
        pacientes, error = PacienteService.get_all_pacientes()
        status_consultas, error_status = StatusConsultaService.get_all_status_consultas()
        convenios, error_convenios = ConvenioService.get_all_convenios()
        if error or error_status or error_convenios:
            flash(error or error_status or error_convenios)
            return redirect('/consultas/recovery')
        return render_template('consulta_create.html', pacientes=pacientes, status_consultas=status_consultas, psicologos=psicologos, convenios=convenios)

    if request.method == 'POST':
        data_marcacao = agora
        data_consulta = request.form.get('data_consulta')
        hora_consulta = request.form.get('hora_consulta')
        duracao = request.form.get('duracao')
        consulta_status_id = request.form.get('consulta_status_id')
        convenios_id = request.form.get('convenios_id')
        id_paciente = request.form.get('id_paciente')
        psi_id = request.form.get('psi_id')
        print("DADOS FORMULÁRIO: ", data_marcacao, data_consulta, hora_consulta, duracao, consulta_status_id, convenios_id, id_paciente, psi_id)
        success, message = ConsultaService.create_consulta(
            data_marcacao=data_marcacao, data_consulta=data_consulta, hora_consulta=hora_consulta, duracao=duracao, 
            consulta_status_id=consulta_status_id, convenios_id=convenios_id, id_paciente=id_paciente, psi_id=psi_id
        )
        if success:
            return redirect('/consultas/recovery')
        else:
            # Recarregar dados para o formulário
            psicologos, _ = PsiService.get_all_psis()
            pacientes, _ = PacienteService.get_all_pacientes()
            status_consultas, _ = StatusConsultaService.get_all_status_consultas()
            convenios, _ = ConvenioService.get_all_convenios()
            
            flash(message)
            return render_template('consulta_create.html', pacientes=pacientes, status_consultas=status_consultas, psicologos=psicologos, convenios=convenios)





@blueprint_consultas.route('/recovery')
def recovery():
    consultas, error = ConsultaService.get_all_consultas()
    if error:
        flash(error)
        return render_template('consulta_recovery.html', consulta=[])

    consultas_dados = []
    for consulta in consultas:
        paciente = consulta.paciente
        status = consulta.status
        psi = consulta.psi  
        
        consultas_dados.append({
            'id': consulta.id,
            'data_consulta': consulta.data_consulta, 
            'hora_consulta': consulta.hora_consulta,  
            'duracao': consulta.duracao,
            'status': status.status,
            'paciente_nome': paciente.nome,
            'psi_nome': psi.nome
        })
    return render_template('consulta_recovery.html', consulta=consultas_dados)





@blueprint_consultas.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    consulta, error = ConsultaService.get_consulta_by_id(id)
    if error:
        flash(error)
        return redirect('/consultas/recovery')

    if request.method == 'GET':
        status, error_status = StatusConsultaService.get_all_status_consultas()
        if error_status:
            flash(error_status)
            return redirect('/consultas/recovery')
        return render_template('consulta_update.html', consulta=consulta, status=status)

    if request.method == 'POST':
        data_consulta = request.form.get('data_consulta')
        hora_consulta = request.form.get('hora_consulta')
        duracao = request.form.get('duracao')
        consulta_status_id = request.form.get('consulta_status_id')

        success, message = ConsultaService.update_consulta(id, data_consulta, hora_consulta, duracao, consulta_status_id)
        if success:
            return redirect('/consultas/recovery')
        else:
            flash(message)
            return render_template('consulta_update.html', consulta=consulta, status=status)

@blueprint_consultas.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    consulta, error = ConsultaService.get_consulta_by_id(id)
    if error:
        flash(error)
        return redirect('/consultas/recovery')

    if request.method == 'GET':
        return render_template('consulta_delete.html', consulta=consulta)
    
    if request.method == 'POST':
        success, message = ConsultaService.delete_consulta(id)
        if success:
            return redirect('/consultas/recovery')
        else:
            flash(message)
            return redirect('/consultas/recovery')
