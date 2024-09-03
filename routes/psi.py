from flask import Blueprint, render_template, request, redirect, flash
from service.psi_service import PsiService
from service.user_service import UserService
from service.paciente_service import PacienteService

blueprint_psi = Blueprint("psi", __name__, template_folder="templates")

@blueprint_psi.route('/recovery')
def recovery():
    
    psis, error = PsiService.get_all_psis()
    if error:
        flash(error)
        return render_template('psi_recovery.html', psi=[])
    
    return render_template('psi_recovery.html', psi=psis)

@blueprint_psi.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    psi, error = PsiService.get_all_psis(id)
    if error:
        flash(error)
        return redirect('/psi/recovery')

    if request.method == 'GET':
        return render_template('psi_update.html', psi=psi)
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        crp = request.form.get('crp')
        abordagem = request.form.get('abordagem')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        login = request.form.get('login')
        senha = request.form.get('senha')
        csenha = request.form.get('csenha')

        
        if senha or csenha:
            if senha != csenha:
                flash("As senhas não coincidem.")
                return render_template('psi_update.html', psi=psi)
        
        # Chama o serviço para atualizar o psi
        success, message = PsiService.update_psi(id=id, nome=nome, sobrenome=sobrenome, crp=crp, abordagem = abordagem,email=email, telefone=telefone, login=login, senha=senha)
        if success:
            return redirect('/psi/recovery')
        else:
            print(f"Erro ao atualizar psi: {message}")
            print(id, nome, sobrenome, abordagem, crp, email, telefone, login)  
            flash(message)
            return render_template('psi_update.html', psi=psi)
