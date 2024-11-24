from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Paciente(db.Model):
    id_paciente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(10))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    endereco = db.Column(db.String(255))
    consultas = db.relationship('Consulta', backref='paciente', lazy=True)

class Medico(db.Model):
    id_medico = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    especialidade = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    anos_experiencia = db.Column(db.Integer)
    consultas = db.relationship('Consulta', backref='medico', lazy=True)

class Consulta(db.Model):
    id_consulta = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('paciente.id_paciente'), nullable=False)
    id_medico = db.Column(db.Integer, db.ForeignKey('medico.id_medico'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    descricao = db.Column(db.String(500))
    pagamentos = db.relationship('Pagamento', backref='consulta', lazy=True)

class Pagamento(db.Model):
    id_pagamento = db.Column(db.Integer, primary_key=True)
    id_consulta = db.Column(db.Integer, db.ForeignKey('consulta.id_consulta'), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    metodo_pagamento = db.Column(db.String(50), nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pendente')

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128))
    cargo = db.Column(db.String(20), default='usuario')
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
        
    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)