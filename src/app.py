# Importar librerías
from flask import Flask, render_template, redirect, request, url_for, flash, get_flashed_messages, abort
from flask_mysqldb import MySQL
from models.ModelUsers import ModelUsers
from models.entities.users import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from config import config

# Creación de instancias
app = Flask(__name__)
db = MySQL(app)
login_manager_app = LoginManager(app)

# Definición de rutas y funciones
# Página de inicio de sesión
@app.route("/")
def index():
    # Redirige a la página de login, genera la dirección /login
    return redirect("login")

# Página de login, que usa los métodos GET y POST del protocolo http
@app.route("/login", methods=["GET", "POST"])
def login():
    # Se revisa si se viene de usar el formulario, que activa el método post
    if request.method == "POST":
        # Si se entró usando el POST, entonces se crea un usuario de la plantilla usando los datos enviados con el formulario
        user = User(0, request.form['username'], request.form['password'],0)
        # Se busca en la base de datos un usuario que tenga los datos mandados por el formulario y se guarda en una variable
        logged_user = ModelUsers.login(db, user)
        # Si el usuario no existe, el objeto sera None
        if logged_user != None:
            # Redirigir a la página /home
            login_user(logged_user)
            if current_user.usertype != 1:
                return redirect(url_for("home"))
            else:
                return redirect(url_for("admin"))
        else:
            # Si el usuario no existe, muestra el mensaje Acceso rechazado y redirige a la página /login
            flash("Acceso rechazado...")
            return render_template("auth/login.html")
    else:
        # Si no se entró después de enviar el formulario, entonces carga la página
        return render_template("auth/login.html")

@app.route("/home")
@login_required
def home():
    return render_template("auth/home.html")

# Crear método para cargar el usuario
@login_manager_app.user_loader
def load_user(id):
    # Regresa los datos del usuario de la base de datos usando su ID
    return ModelUsers.get_by_id(db, id)

# Definir ruta de salida de sesión
@app.route("/logout")
# Fuerza a que el usuario tenga una sesión activa
# @login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("login"))


# Crear decorador personalizado que verifica si el usuario es de usertype=1
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.usertype != 1:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view

# Definir la ruta para página de administración
@app.route("/admin")
@login_required
@admin_required
def admin():
    return render_template("auth/admin.html")

# Si la aplicación se ejecutó directamente desde el cmd, entonces usa las configuraciones de config.py
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()