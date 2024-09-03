from flask import Blueprint, render_template, request, redirect, flash
from database.models.user_model import User
from database.models.convenio_model import Convenio
from service.paciente_service import PacienteService
from service.psi_service import PsiService
from service.convenio_service import ConvenioService
from database.database import db
import locale
from datetime import datetime

blueprint_pacientes = Blueprint("pacientes", __name__, template_folder="templates")
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
agora = datetime.now().strftime('%d/%m/%Y')

@blueprint_pacientes.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        paciente, paciente_error = PacienteService.get_all_pacientes()
        if paciente_error:
            return render_template('error.html', error=paciente_error)
        return render_template('pacientes_create.html', paciente=paciente)

    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        cpf = request.form.get('cpf')
        nascimento = request.form.get('nascimento')
        genero = request.form.get('genero')
        email = request.form.get('email')
        ocupacao = request.form.get('ocupacao')
        cep= request.form.get('cep')
        endereco = request.form.get('endereco')
        endereco_complemento = request.form.get('endereco_complemento')
        fone = request.form.get('fone')
        datainicio = agora

        success, message = PacienteService.create_paciente(nome = nome, sobrenome = sobrenome, cpf = cpf, nascimento = nascimento, genero = genero, email = email, ocupacao=ocupacao, cep=cep, 
                                                           endereco=endereco, endereco_complemento=endereco_complemento,
                                                           fone=fone, datainicio= datainicio)
        if success:
            return redirect('/pacientes/recovery')
        else:
            flash(message)
            return render_template('pacientes_create.html')
        

@blueprint_pacientes.route('/recovery')
def recovery():
    pacientes, error = PacienteService.get_all_pacientes()
    if error:
        flash(error)
        return render_template('pacientes_recovery.html', pacientes=[])
    
    return render_template('pacientes_recovery.html', pacientes=pacientes)

@blueprint_pacientes.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    paciente, error = PacienteService.get_paciente_by_id(id)
    if error:
        flash(error)
        return redirect('/pacientes/recovery')

    if request.method == 'GET':
        return render_template('pacientes_update.html', paciente=paciente)
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        cpf = request.form.get('cpf')
        nascimento = request.form.get('nascimento')
        genero = request.form.get('genero')
        email = request.form.get('email')
        ocupacao = request.form.get('ocupacao')
        cep= request.form.get('cep')
        endereco = request.form.get('endereco')
        endereco_complemento = request.form.get('endereco_complemento')
        fone = request.form.get('fone')

        success, message = PacienteService.update_paciente( id, nome, sobrenome, cpf, nascimento, genero, email, ocupacao, 
                                                           cep, endereco, endereco_complemento, fone)
        if success:
            return redirect('/pacientes/recovery')
        else:
            flash(message)
            return render_template('pacientes_update.html', paciente=paciente)

@blueprint_pacientes.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    paciente, error = PacienteService.get_paciente_by_id(id)
    if error:
        flash(error)
        return redirect('/pacientes/recovery')

    if request.method == 'GET':
        return render_template('pacientes_delete.html', paciente=paciente)
    
    if request.method == 'POST':
        success, message = PacienteService.delete_paciente(id)
        if success:
            return redirect('/pacientes/recovery')
        else:
            flash(message)
            return redirect('/pacientes/recovery')


