from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, _calling_context
import sqlalchemy
from sqlalchemy import exc


app = Flask(__name__, template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
db = SQLAlchemy(app)

class Clientes(db.Model):
    __tablename__ = "tb_clientes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.DateTime, default=db.func.current_timestamp())
    nome = db.Column(db.String(50))
    telefone = db.Column(db.Float(50))

    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

class Servico(db.Model):
    __tablename__ = "tb_servico"
    id_servico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(10))
    nome_cli = db.Column(db.String(50))
    servico = db.Column(db.String(50))
    preco = db.Column(db.Float(10))
    observacao = db.Column(db.String(50))

    def __init__(self, nome_cli, servico, preco, status, observacao):
        self.nome_cli = nome_cli
        self.servico = servico
        self.status = status
        self.preco = preco
        self.observacao = observacao

    
@app.route("/")
def index():
    return render_template("index.html")

########### CRUD CLIENTES ###########   
#        CADASTRAR CLIENTE ok funcionando
@app.route("/cad_cliente", methods=['GET', 'POST'])
def cadastrar_cliente():
    try:
        if request.method == 'POST':
            cliente = Clientes(
                request.form['nome_cli'],
                request.form['tel_cli'],)
            db.session.add(cliente)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('cad_cliente.html')
    except exc.SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        if error == "UNIQUE constraint failed: tb_cliente.id_cliente":
            return error
        elif error == "datatype mismatch":
            return "Incompatibilidade do tipos de dados"
        return 'Erro na programação, entre em contato com o desenvolvedor'

#       LISTAR clientes ok funcionando
@app.route("/listar_clientes")
def listar_clientes():
    cliente = Clientes.query.all()
    return render_template('/listar_clientes.html', cliente=cliente)

#       EDITAR cliente ok funcionando
@app.route("/editar_cliente/<int:id>", methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Clientes.query.get(id) 
    if request.method == 'POST':
        cliente.nome = request.form['nome_cli']
        cliente.telefone = request.form['tel_cli']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar_cliente.html', cliente=cliente)

########## DELETAR UM cliente ok funcionando
@app.route("/listar_clientes/delete/<int:id>", methods=['GET', 'POST'])
def delete_cliente(id):
    cliente = Clientes.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('index'))

###### REGISTRAR UM SERVIÇO ok funcionando
@app.route("/cadastrar_servico", methods=['GET', 'POST'])
def cadastrar_servico():
    try:
        if request.method == 'POST':
            servico = Servico(
                request.form['nome_cli'],
                request.form['servico'],
                request.form['preco'],
                request.form['status'],
                request.form['observacao'],)
            db.session.add(servico)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('cadastrar_servico.html')
    except exc.SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        if error == "UNIQUE constraint failed: tb_cliente.id_cliente":
            return error
        elif error == "datatype mismatch":
            return "Incompatibilidade do tipos de dados"
        return 'Erro na programação, tem coisa errada'

####### LISTAR TODOS OS SERVIÇOS ok funcionando
@app.route("/listar_servicos", methods=['GET'])
def listar_servicos():
    servico = Servico.query.all()
    return render_template('/listar_servicos.html', servico=servico)

@app.route("/editar_servico/<int:id>", methods=['GET', 'POST'])
def editar_servico(id):
    servico = Servico.query.get(id)
    if request.method == 'POST':
        servico.nome_cli = request.form['nome_cli']
        servico.status = request.form['status']
        servico.servico = request.form['servico']
        servico.preco = request.form['preco']
        servico.observacao = request.form['observacao']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar_servico.html', servico=servico)


@app.route("/listar_servicos/delete/<int:id>", methods=['GET', 'POST'])
def delete_servico(id):
    servico = Servico.query.get(id)
    db.session.delete(servico)
    db.session.commit()
    return redirect(url_for('index'))


######## METODO MAIN
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
