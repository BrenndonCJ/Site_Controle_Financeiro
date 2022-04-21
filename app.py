from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

import uuid

# Inicializando o APP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'w9ga41h8r74s374kcb4jf6jad62m9dytd'              # Definindo a configuração do app: Chave secreta para envio de bytes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/db/db.sqlite3'    # Definindo a configuração do app: caminho do banco de dados

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

# Inicializando o Banco de Dados
db = SQLAlchemy(app)

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=str(user_id)).first()

# Definindo modelo da tabela de Usuarios
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)



# Definindo modelo da tabela de Débitos
class Debitos(db.Model):
    id = db.Column(db.String, primary_key=True, nullable=False)
    descricao = db.Column(db.String, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    username = db.Column(db.String, nullable=False)


    def __init__(self, id, descricao, valor, username):
        self.id = id
        self.descricao = descricao
        self.valor = valor
        self.username = username


# Inicializando as Rotas
# Rotas de Login / Registro
@app.route('/', methods=['GET','POST'])
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        try:
            user = User(username, pwd)
            db.session.add(user)
            db.session.commit()
            flash("Cadastrado com sucesso")
            return redirect(url_for('login'))
        except:
            flash("Nome de usuario indisponivel")
            redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not user.verify_password(pwd):
            flash("Usuario ou senha incorretos")
            return redirect('login')

        login_user(user)
        return redirect(url_for('home'))
        # return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Rotas de navegação
@app.route('/home')
@login_required
def home():
    debitos = Debitos.query.filter_by(username=current_user.username).all()
    total = db.session.query(db.func.sum(Debitos.valor)).filter_by(username=current_user.username).all()
    total = total[0][0]
    return render_template('debitos.html', data=debitos, total=total)

@app.post('/save')
@login_required
def save_data():
    if request.method == "POST":
        desc = request.form['desc']
        valor = request.form['valor']
        debito = Debitos(str(uuid.uuid4()), desc, valor, current_user.username)
        db.session.add(debito)
        db.session.commit()

    return redirect(url_for("home"))

@app.route('/update/<string:id>', methods=['GET', 'POST'])
@login_required
def update_data(id):
    debito = Debitos.query.get(id)
    if request.method == "POST":
        desc = request.form['desc']
        valor = request.form['valor']
        debito.descricao = desc
        debito.valor = valor
        db.session.commit()

    return redirect(url_for("home"))

@app.route('/delete/<string:id>')
@login_required
def delete_data(id):
    debito = Debitos.query.get(id)
    db.session.delete(debito)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    db.create_all()                         # Criando as Tabelas do banco de Dados caso não tenham sido criadas
    app.run(threaded=True , debug=True)
    