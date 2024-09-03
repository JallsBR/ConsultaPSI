from flask import Blueprint, render_template, request, redirect, flash, url_for
from service.transcricoes_service import TranscricaoService
from service.consulta_service import ConsultaService
from flask_login import current_user
import locale
from datetime import datetime




blueprint_transcricoes = Blueprint("transcricoes", __name__, template_folder="templates")
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
agora = datetime.now().strftime('%d/%m/%Y')


@blueprint_transcricoes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':        
        consultas, error = TranscricaoService.get_transcricao_faltantes()
        if error:
            flash(error)
            return redirect('/transcricoes/recovery')
        return render_template('transcricoes_create.html', consultas=consultas)
    
    if request.method == 'POST':
        id_consulta = int(request.form.get('id_consulta'))
        transcricao = request.form.get('transcricao')
        data_transcricao = str(agora)

        success, message = TranscricaoService.create_transcricao(id_consulta, transcricao, data_transcricao)
        if success:
            return redirect('/transcricoes/recovery')
        else:
            flash(message)
            return render_template('transcricoes_create.html')




@blueprint_transcricoes.route('/recovery')
def recovery():
    transcricoes, error = TranscricaoService.get_all_transcricoes()
    if error:
        flash(error)
        return redirect('/transcricoes/recovery') 
    if transcricoes is None:
        transcricoes = []
    
    return render_template('transcricoes_recovery.html', transcricoes=transcricoes)


@blueprint_transcricoes.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    transcricao, error = TranscricaoService.get_transcricao_by_id(id)
    if error:
        flash(error)
        return redirect('/transcricoes/recovery')

    if request.method == 'GET':
        consultas = ConsultaService.get_consulta_pacientes()
        return render_template('transcricoes_update.html', transcricao=transcricao, consultas=consultas)

    if request.method == 'POST':
        id_consulta = request.form.get('id_consulta')
        nova_transcricao = request.form.get('transcricao')
        data_transcricao = str(agora)

        success, message = TranscricaoService.update_transcricao(id, id_consulta, nova_transcricao, data_transcricao)
        if success:
            return redirect('/transcricoes/recovery')
        else:
            flash(message)
            return render_template('transcricoes_update.html', transcricao=transcricao, consultas=consultas)

@blueprint_transcricoes.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    transcricao, error = TranscricaoService.get_transcricao_by_id(id)
    if error:
        flash(error)
        return redirect('/transcricoes/recovery')

    if request.method == 'GET':
        return render_template('transcricoes_delete.html', transcricao=transcricao)
    
    if request.method == 'POST':
        success, message = TranscricaoService.delete_transcricao(id)
        if success:
            return redirect('/transcricoes/recovery')
        else:
            flash(message)
            return render_template('transcricoes_delete.html', transcricao=transcricao)
        
