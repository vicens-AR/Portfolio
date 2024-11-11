from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin

app = Flask(__name__)
app.secret_key = 'SMHvYzo8dnjWs49Gzvjr'  # Cambia esta clave por algo seguro
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://uypspzas3lbrauuj:SMHvYzo8dnjWs49Gzvjr@brfj39ld4kifwyrcpnzj-mysql.services.clever-cloud.com:3306/brfj39ld4kifwyrcpnzj'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Ruta de inicio de sesión

# Modelo de usuario
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Cargar usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('modo_edicion'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

# Ruta de modo edición (protegida)
@app.route('/modo_edicion')
@login_required
def modo_edicion():
    return render_template('modo_edicion.html')

# Ruta de cierre de sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

# Página principal
@app.route('/')
def principal():
    return render_template('Inicio.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea la base de datos si no existe
    app.run(debug=True, port=3500)
