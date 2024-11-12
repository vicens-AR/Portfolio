from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'SMHvYzo8dnjWs49Gzvjr'  # Cambia esta clave por algo seguro
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://uypspzas3lbrauuj:SMHvYzo8dnjWs49Gzvjr@brfj39ld4kifwyrcpnzj-mysql.services.clever-cloud.com:3306/brfj39ld4kifwyrcpnzj'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

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
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('modo_edicion'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

# Ruta de registro
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Encriptar la contraseña
        hashed_password = generate_password_hash(password, method='sha256')
        
        # Crear nuevo usuario
        new_user = User(username=username, password=hashed_password)
        
        # Guardar en la base de datos
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except:
            flash('El usuario ya existe. Por favor, elige otro nombre de usuario.', 'danger')
            db.session.rollback()

    return render_template('signup.html')

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
        db.create_all()
    app.run(debug=True, port=3500)
