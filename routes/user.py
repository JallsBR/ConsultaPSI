from flask import Blueprint, render_template, request, redirect, flash, url_for
from service.user_service import UserService
from extensions import login_manager
from flask_login import login_user, logout_user

blueprint_user = Blueprint("user", __name__, template_folder="templates")

@blueprint_user.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('user_create.html')
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        login = request.form.get('login')
        senha = request.form.get('senha')
        csenha = request.form.get('csenha')
        
        print('REQUESTS: ', nome, sobrenome, email, telefone, login, senha) 
        if nome and sobrenome and email and telefone and login and senha and csenha==senha:

            success, message = UserService.create_user(nome, sobrenome, email, telefone, login, senha)
            if success:
                print("Usuário criado com sucesso, redirecionando para /login")
                return redirect('/login')
                flash(message)
            else:
                print(f"Erro ao criar usuário: {message}")
                flash(message)
                return redirect('/login')
        else:
            print("Alguns campos estão faltando.")
            flash("Todos os campos devem ser preenchidos!")
            return redirect('/login')
        
"""        
@blueprint_user.route('/recovery')
def recovery():
    users, error = UserService.get_all_users()
    if error:
        flash(error)
        return render_template('user_recovery.html', users=[])
    
    return render_template('user_recovery.html', users=users)
"""


@blueprint_user.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user, error = UserService.get_all_users(id)
    if error:
        flash(error)
        return redirect('/psi/recovery')

    if request.method == 'GET':
        return render_template('user_update.html', user=user)
    
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

        if csenha == senha: 
            success, message = UserService.update_user(id, nome, sobrenome, email=email, telefone=telefone, login=login, senha=senha, crp=crp, abordagem=abordagem)
            if success:
                return redirect('/psi/recovery')
            else:
                flash(message)
                return render_template('user_update.html', user=user)
        else:
            flash("As senhas não coincidem.")
            return render_template('user_update.html', user=user)

"""
@blueprint_user.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'GET':
        user, error = UserService.get_all_users(id)
        if error:
            flash(error)
            return redirect('/user/recovery')

        return render_template('user_delete.html', user=user)
    
    if request.method == 'POST':
        success, message = UserService.delete_user(id)
        if success:
            return redirect('/user/recovery')
        else:
            flash(message)
            return redirect('/user/recovery')
"""

@blueprint_user.route('/finalizar/<int:id>', methods=['GET', 'POST'])
def finalizar_user(id):
    if request.method == 'GET':
        user, error = UserService.get_all_users(id)
        if error:
            print(f"GET erro: {error}")
        return render_template('finalizar_cadastro.html', user=user)

    if request.method == 'POST':
        print(f"Form data: {request.form}")
        user, error = UserService.get_all_users(id)
        if error:
            print(f"ERRO POST: {error}")
        if not user:
            return "Usuário não encontrado", 404

        tipo = request.form.get('tipo')
        crp = request.form.get('crp')
        abordagem = request.form.get('abordagem')

        if tipo and tipo != user['tipo']:  
            user['tipo'] = tipo

        if tipo == 'psicólogo':
            if crp and crp != user['crp']: 
                user['crp'] = crp

            if abordagem and abordagem != user['abordagem']:  
                user['abordagem'] = abordagem
        else:
            user['crp'] = ''
            user['abordagem'] = ''

        success, message = UserService.update_user(
            id,
            tipo=user['tipo'],
            crp=user['crp'],
            abordagem=user['abordagem']
        )

        if success:
            return redirect(url_for('index'))  
        else:
            print(f"Erro ao atualizar: {message}")
            flash("Erro ao atualizar usuário.")
            return redirect(url_for('index', id=id))