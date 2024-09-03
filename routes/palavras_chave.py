from flask import Blueprint, render_template, request, redirect
from database.models.user_model import User
from database.database import db

blueprint_usuarios= Blueprint("usuarios", __name__, template_folder="templates")


@blueprint_usuarios.route('/create', methods=['GET','POST'])
def create():
    if request.method=='GET':
        return render_template('usuarios_create.html')
    if request.method=='POST':
        nome = request.form.get('nome')
        email = request.form.get('email')        
        senha = request.form.get('senha')
        csenha = request.form.get('csenha')   

        usuario=User(nome,email, senha)
        db.session.add(usuario)
        db.session.commit()

        return redirect('/usuarios/recovery')
    
@blueprint_usuarios.route('/recovery')
def recovery():
    usuarios = User.query.all()
    return render_template ('usuarios_recovery.html', usuarios=usuarios)

@blueprint_usuarios.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    usuario= User.query.get(id)

    if request.method=='GET':
        return render_template('usuarios_update.html', usuario = usuario)
    
    if request.method=='POST':
        nome = request.form.get('nome')
        email = request.form.get('email')        
        senha = request.form.get('senha')

        usuario.nome= nome
        usuario.email= email
        usuario.senha= senha

        db.session.add(usuario)
        db.session.commit()  
        return redirect('/usuarios/recovery')
       

@blueprint_usuarios.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    usuario= User.query.get(id)
    if request.method=='GET':
        return render_template('usuarios_delete.html', usuario = usuario)
    if request.method=='POST':
        db.session.delete(usuario) 
        db.session.commit() 
        return redirect('/usuarios/recovery')