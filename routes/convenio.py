from flask import Blueprint, render_template, request, redirect, flash
from service.convenio_service import ConvenioService
from flask_login import current_user

blueprint_convenio = Blueprint("convenio", __name__, template_folder="templates")




@blueprint_convenio.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('convenio_create.html')
    
    if request.method == 'POST':
        convenio_nome = request.form.get('convenio')
        valor_consulta = request.form.get('valor_consulta')
        user_id = current_user.id

        success, message = ConvenioService.create_convenio(convenio_nome, valor_consulta, user_id)
        if success:
            return redirect('/adm/recovery')
        else:
            flash(message)
            return render_template('convenio_create.html')
        




@blueprint_convenio.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    convenio, error = ConvenioService.get_convenio_by_id(id)
    if error:
        flash(error)
        return redirect('/adm/recovery')

    if request.method == 'GET':
        return render_template('convenio_update.html', convenio=convenio)
    
    if request.method == 'POST':
        convenio_nome = request.form.get('convenio')
        valor_consulta = request.form.get('valor_consulta')

        success, message = ConvenioService.update_convenio(id, convenio_nome, valor_consulta)
        if success:
            return redirect('/adm/recovery')
        else:
            flash(message)
            return render_template('convenio_update.html', convenio=convenio)

@blueprint_convenio.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    convenio, error = ConvenioService.get_convenio_by_id(id)
    if error:
        flash(error)
        return redirect('/adm/recovery')

    if request.method == 'GET':
        return render_template('convenio_delete.html', convenio=convenio)
    
    if request.method == 'POST':
        success, message = ConvenioService.delete_convenio(id)
        if success:
            return redirect('/adm/recovery')
        else:
            flash(message)
            return redirect('/adm/recovery')
