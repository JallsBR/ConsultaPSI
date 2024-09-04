from flask import Blueprint, render_template, request, redirect, flash, url_for,  jsonify
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
        id_consulta = request.args.get('id_consulta')
        consultas, error = TranscricaoService.get_transcricao_faltantes()
        if error:
            flash(error)
            return redirect('/transcricoes/recovery')
        return render_template('transcricoes_create.html', consultas=consultas, id_consulta=id_consulta)
    
    if request.method == 'POST':
        id_consulta = request.form.get('id_consulta')
        transcricao = request.form.get('transcricao')
        psi_id = request.form.get('psi_id')
        data_transcricao = str(datetime.utcnow())

        success, message = TranscricaoService.create_transcricao(id_consulta=id_consulta, psi_id=psi_id, transcricao=transcricao, data_transcricao=data_transcricao)
        if success:
            return redirect(request.referrer or url_for('index'))
        else:
            flash(message)
            return render_template('transcricoes_create.html', id_consulta=id_consulta)





@blueprint_transcricoes.route('/update/<int:id>', methods=['POST'])
def update(id):
    transcricao, error = TranscricaoService.get_transcricao_by_id(id)
    if error:
        return jsonify({'success': False, 'message': error}), 500

    id_consulta = transcricao.id_consulta
    nova_transcricao = request.form.get('transcricao')
    data_transcricao = str(agora)
    psi_id = transcricao.psi_id

    success, message = TranscricaoService.update_transcricao(
        id=id,
        id_consulta=id_consulta,
        nova_transcricao=nova_transcricao,
        data_transcricao=data_transcricao,
        psi_id=psi_id
    )
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': message}), 500
    



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
        


@blueprint_transcricoes.route('/start/<int:id_consulta>', methods=['GET', 'POST'])
def start_transcricao(id_consulta):
    consulta, error = ConsultaService.get_consulta_by_id(id_consulta)
    if error:
        flash(error, 'danger')
        return redirect(url_for('some_error_handling_route'))

    if consulta.transcricao:
        flash('A transcrição já existe para esta consulta.', 'warning')
        return redirect(url_for('transcricoes.view', id=consulta.transcricao.id))
    
    if request.method == 'POST':
        transcricao_texto = request.form.get('transcricao')
        data_transcricao = str(datetime.utcnow())

        sucesso, mensagem = TranscricaoService.create_transcricao(
            id_consulta=consulta.id,
            transcricao=transcricao_texto,
            data_transcricao=data_transcricao
        )

        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('transcricoes.view', id=consulta.transcricao.id))
        else:
            flash(mensagem, 'danger')

    return render_template('transcricoes_create.html', id_consulta=id_consulta)


@blueprint_transcricoes.route('/view/<int:transcricao_id>', methods=['GET'])
def view_transcricao(transcricao_id):
    transcricao, error = TranscricaoService.get_transcricao_by_id(transcricao_id)
    
    if error:
        return jsonify({'error': error}), 500
    
    if transcricao:
        return jsonify({'transcricao': transcricao.transcricao})
    else:
        return jsonify({'error': 'Transcrição não encontrada'}), 404
