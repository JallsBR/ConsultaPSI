from flask import Blueprint, render_template, request, redirect
from database.models.status_consulta_model import StatusConsulta
from database.models.convenio_model import Convenio
from flask_login import current_user


blueprint_adm= Blueprint("adm", __name__, template_folder="templates")



@blueprint_adm.route('/recovery')
def recovery():
    if current_user:
        convenio = Convenio.query.all()
        status_consultas = StatusConsulta.query.all()
        
        return render_template ('adm_recovery.html', convenio=convenio, status_consultas=status_consultas)
    return redirect('/login')

