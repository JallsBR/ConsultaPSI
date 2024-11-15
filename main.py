from flask import Flask, render_template, redirect
from flask_login import logout_user, current_user
from database.database import db
from flask_migrate import Migrate
from extensions import login_manager
from datetime import datetime, timedelta
from service.consulta_service import ConsultaService



from routes.consultas import blueprint_consultas
from routes.psi import blueprint_psi
from routes.convenio import blueprint_convenio
from routes.pacientes import blueprint_pacientes
from routes.status_consultas import blueprint_status_consultas
from routes.transcricoes import blueprint_transcricoes
from routes.adm import blueprint_adm
from routes.login import blueprint_login
from routes.user import blueprint_user

app = Flask(__name__)
login_manager.init_app(app)

conexao="sqlite:///meubanco.sqlite"

app.config['SECRET_KEY'] = 'minha-senha'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACKMODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(blueprint_consultas, url_prefix='/consultas')
app.register_blueprint(blueprint_psi, url_prefix='/psi')
app.register_blueprint(blueprint_convenio, url_prefix='/convenio')
app.register_blueprint(blueprint_pacientes, url_prefix='/pacientes')
app.register_blueprint(blueprint_status_consultas, url_prefix='/status_consultas')
app.register_blueprint(blueprint_transcricoes, url_prefix='/transcricoes')
app.register_blueprint(blueprint_adm, url_prefix='/adm')
app.register_blueprint(blueprint_login, url_prefix='/login')
app.register_blueprint(blueprint_user, url_prefix='/user')
migrate = Migrate(app, db)


@app.template_filter('format_phone')
def format_phone(phone):
    return f"({phone[:2]}) {phone[2]} {phone[3:7]}-{phone[7:]}"



@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect('/login')
    if current_user.tipo == 'não informado':
        return redirect(f'/user/finalizar/{current_user.id}')
    
    if current_user.tipo == 'psicólogo':
        hoje = datetime.today().date()
        semana_inicio = hoje - timedelta(days=hoje.weekday())
        semana_fim = semana_inicio + timedelta(days=6)
        
        consultas_semana, _ = ConsultaService.get_consultas_by_date_range(start_date=semana_inicio, end_date=semana_fim, psi_id=current_user.id)

        relatorio_convenio, ganhos = ConsultaService.get_relatorio_convenio_e_ganhos(current_user.id)

        return render_template('index.html', consultas_semana=consultas_semana, relatorio_convenio=relatorio_convenio, ganhos=ganhos)
    
    return render_template('index.html')




@app.route('/logout')
def logout():
    logout_user()
    return redirect ('/')

app.run(host='0.0.0.0', port=81, debug=True)