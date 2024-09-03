from flask import Blueprint, render_template, request, redirect, flash
from service.status_consultas_service import StatusConsultaService

blueprint_status_consultas = Blueprint("status_consultas", __name__, template_folder="templates")

@blueprint_status_consultas.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('status_consultas_create.html')
    
    if request.method == 'POST':
        status = request.form.get('status')

        success, message = StatusConsultaService.create_status_consulta(status)
        if success:
            return redirect('/adm/recovery')
        else:
            flash(message)
            return render_template('status_consultas_create.html')

        


@blueprint_status_consultas.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    status_consulta, error = StatusConsultaService.get_status_consulta_by_id(id)
    if error:
        flash(error)
        return redirect('/adm/recovery')

    if request.method == 'GET':
        return render_template('status_consultas_update.html', status_consultas=status_consulta)
    
    if request.method == 'POST':
        status = request.form.get('status')

        success, message = StatusConsultaService.update_status_consulta(id, status)
        if success:
            return redirect('/adm/recovery')
        else:
            flash(message)
            return render_template('status_consultas_update.html', status_consultas=status_consulta)

@blueprint_status_consultas.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    status_consulta, error = StatusConsultaService.get_status_consulta_by_id(id)
    if error:
        flash(error)
        return redirect('/adm/recovery')

    if request.method == 'GET':
        return render_template('status_consultas_delete.html', status_consultas=status_consulta)
    
    if request.method == 'POST':
        success, message = StatusConsultaService.delete_status_consulta(id)
        if success:
            return redirect('/adm/recovery')
        else:
            flash(message)
            return redirect('/adm/recovery')
