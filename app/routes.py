from flask import request, redirect, url_for, render_template, flash
from app import app, db
from app.models import Paciente, Medico, Consulta, Pagamento, Usuario
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.cargo != 'admin':
            flash('Acesso negado. Você precisa ser um administrador.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_senha(senha):
            login_user(usuario)
            return redirect(url_for('index'))
        flash('Email ou senha inválidos')
    return render_template('auth/login.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        if request.form['senha'] != request.form['confirmar_senha']:
            flash('As senhas não coincidem')
            return render_template('auth/registrar.html')
            
        if Usuario.query.filter_by(email=request.form['email']).first():
            flash('Email já cadastrado')
            return render_template('auth/registrar.html')
            
        usuario = Usuario(
            nome=request.form['nome'],
            email=request.form['email']
        )
        usuario.set_senha(request.form['senha'])
        db.session.add(usuario)
        db.session.commit()
        
        login_user(usuario)
        return redirect(url_for('login'))
    return render_template('auth/registrar.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/pacientes')
@login_required
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes/index.html', pacientes=pacientes)

@app.route('/pacientes/criar', methods=['GET', 'POST'])
@login_required
def criar_paciente():
    if request.method == 'POST':
        paciente = Paciente(
            nome=request.form['nome'],
            data_nascimento=datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d'),
            sexo=request.form['sexo'],
            telefone=request.form['telefone'],
            email=request.form['email'],
            endereco=request.form['endereco']
        )
        db.session.add(paciente)
        db.session.commit()
        return redirect(url_for('listar_pacientes'))
    return render_template('pacientes/criar.html')

@app.route('/pacientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    if request.method == 'POST':
        paciente.nome = request.form['nome']
        paciente.data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d')
        paciente.sexo = request.form['sexo']
        paciente.telefone = request.form['telefone']
        paciente.email = request.form['email']
        paciente.endereco = request.form['endereco']
        db.session.commit()
        return redirect(url_for('listar_pacientes'))
    return render_template('pacientes/editar.html', paciente=paciente)

@app.route('/pacientes/deletar/<int:id>')
@login_required
def deletar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    return redirect(url_for('listar_pacientes'))

# Rotas para Médicos
@app.route('/medicos')
@login_required
def listar_medicos():
    medicos = Medico.query.all()
    return render_template('medicos/index.html', medicos=medicos)

@app.route('/medicos/criar', methods=['GET', 'POST'])
@login_required
def criar_medico():
    if request.method == 'POST':
        medico = Medico(
            nome=request.form['nome'],
            especialidade=request.form['especialidade'],
            telefone=request.form['telefone'],
            email=request.form['email'],
            anos_experiencia=request.form['anos_experiencia']
        )
        db.session.add(medico)
        db.session.commit()
        return redirect(url_for('listar_medicos'))
    return render_template('medicos/criar.html')

@app.route('/medicos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_medico(id):
    medico = Medico.query.get_or_404(id)
    if request.method == 'POST':
        medico.nome = request.form['nome']
        medico.especialidade = request.form['especialidade']
        medico.telefone = request.form['telefone']
        medico.email = request.form['email']
        medico.anos_experiencia = request.form['anos_experiencia']
        db.session.commit()
        return redirect(url_for('listar_medicos'))
    return render_template('medicos/editar.html', medico=medico)

@app.route('/medicos/deletar/<int:id>')
@login_required
def deletar_medico(id):
    medico = Medico.query.get_or_404(id)
    db.session.delete(medico)
    db.session.commit()
    return redirect(url_for('listar_medicos'))

# Rotas para Consultas
@app.route('/consultas')
@login_required
def listar_consultas():
    consultas = Consulta.query.all()
    return render_template('consultas/index.html', consultas=consultas)

@app.route('/consultas/criar', methods=['GET', 'POST'])
@login_required
def criar_consulta():
    if request.method == 'POST':
        consulta = Consulta(
            id_paciente=request.form['id_paciente'],
            id_medico=request.form['id_medico'],
            data=datetime.strptime(request.form['data'], '%Y-%m-%d'),
            hora=datetime.strptime(request.form['hora'], '%H:%M').time(),
            descricao=request.form['descricao']
        )
        db.session.add(consulta)
        db.session.commit()
        return redirect(url_for('listar_consultas'))
    
    # Busca todos os médicos e pacientes do banco de dados
    medicos = Medico.query.all()
    pacientes = Paciente.query.all()
    
    return render_template('consultas/criar.html', 
                         medicos=medicos,
                         pacientes=pacientes)

@app.route('/consultas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    if request.method == 'POST':
        consulta.id_paciente = request.form['id_paciente']
        consulta.id_medico = request.form['id_medico']
        consulta.data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        consulta.hora = datetime.strptime(request.form['hora'], '%H:%M').time()
        consulta.descricao = request.form['descricao']
        db.session.commit()
        return redirect(url_for('listar_consultas'))
    
    # Busca todos os médicos e pacientes do banco de dados
    medicos = Medico.query.all()
    pacientes = Paciente.query.all()
    
    return render_template('consultas/editar.html',
                         consulta=consulta,
                         medicos=medicos,
                         pacientes=pacientes)

@app.route('/consultas/deletar/<int:id>')
@login_required
def deletar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    db.session.delete(consulta)
    db.session.commit()
    return redirect(url_for('listar_consultas'))

# Rotas para Pagamentos
@app.route('/pagamentos')
@login_required
def listar_pagamentos():
    pagamentos = Pagamento.query.all()
    return render_template('pagamentos/index.html', pagamentos=pagamentos)

@app.route('/pagamentos/criar', methods=['GET', 'POST'])
@login_required
def criar_pagamento():
    if request.method == 'POST':
        pagamento = Pagamento(
            id_consulta=request.form['id_consulta'],
            valor=float(request.form['valor']),
            metodo_pagamento=request.form['metodo_pagamento'],
            data_pagamento=datetime.strptime(request.form['data_pagamento'], '%Y-%m-%d'),
            status=request.form['status']
        )
        db.session.add(pagamento)
        db.session.commit()
        return redirect(url_for('listar_pagamentos'))
    
    # Busca todas as consultas do banco de dados
    consultas = Consulta.query.all()
    
    return render_template('pagamentos/criar.html', consultas=consultas)

@app.route('/pagamentos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_pagamento(id):
    pagamento = Pagamento.query.get_or_404(id)
    if request.method == 'POST':
        pagamento.id_consulta = request.form['id_consulta']
        pagamento.valor = float(request.form['valor'])
        pagamento.metodo_pagamento = request.form['metodo_pagamento']
        pagamento.data_pagamento = datetime.strptime(request.form['data_pagamento'], '%Y-%m-%d')
        pagamento.status = request.form['status']
        db.session.commit()
        return redirect(url_for('listar_pagamentos'))
    
    # Busca todas as consultas do banco de dados
    consultas = Consulta.query.all()
    
    return render_template('pagamentos/editar.html', 
                         pagamento=pagamento,
                         consultas=consultas)

@app.route('/pagamentos/deletar/<int:id>')
@login_required
def deletar_pagamento(id):
    pagamento = Pagamento.query.get_or_404(id)
    db.session.delete(pagamento)
    db.session.commit()
    return redirect(url_for('listar_pagamentos'))

@app.route('/usuarios')
@login_required
@admin_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/index.html', usuarios=usuarios)

@app.route('/usuarios/criar', methods=['GET', 'POST'])
@login_required
@admin_required
def criar_usuario():
    if request.method == 'POST':
        if request.form['senha'] != request.form['confirmar_senha']:
            flash('As senhas não coincidem')
            return render_template('usuarios/criar.html')

        if Usuario.query.filter_by(email=request.form['email']).first():
            flash('Email já cadastrado')
            return render_template('usuarios/criar.html')

        usuario = Usuario(
            nome=request.form['nome'],
            email=request.form['email'],
            cargo=request.form['cargo']  # Adicione um campo para selecionar o cargo
        )
        usuario.set_senha(request.form['senha'])
        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for('listar_usuarios'))
    
    return render_template('usuarios/criar.html')

@app.route('/usuarios/deletar/<int:id>')
@login_required
@admin_required
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('listar_usuarios'))

@app.route('/')
def index():
    return render_template('index.html')