from flask import Flask, render_template, redirect, url_for, flash, request, abort
import flask.cli
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from hashlib import sha256
import argparse
from urllib.parse import urlparse, urljoin
import logging

from src.logger import Logger
from src.forms import LoginForm, RegisterForm
from src.data import Database
from src.config import Config
from src.minecraftrcon import MinecraftRcon
# ======================================================================================================================
app = Flask(__name__)
secretKey = sha256(datetime.now().strftime("%d%m%Y").encode()).hexdigest()
logger = Logger().info("Server started with secret key: " + secretKey)
app.config['SECRET_KEY'] = secretKey
login_manager = LoginManager()
login_manager.init_app(app)
# ======================================================================================================================

class User(UserMixin):
    def __init__(self, id=None):
        self.id = id
    
    def get_id(self):
        return self.id

def readArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Run in debug mode", action="store_true")
    parser.add_argument("-p", "--port", help="Port to run on", type=int)
    parser.add_argument("-ho", "--host", help="Host to run on", type=str)
    args = parser.parse_args()
    return args

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    logger.info(f"Unauthorized access to {request.path} from {request.remote_addr}")
    flash('Vous devez être connecté pour accèder à cette page !', 'warning')
    return redirect('/login?next=' + request.path)

@app.route('/')
def index():
    return render_template('index.html', PageName="Home")

@app.route('/register', methods=['GET', 'POST'])
def register():
    logger.info(f"Unregistered Access to {request.path} from {request.remote_addr}")
    if current_user.is_authenticated:
        flash("Vous êtes déjà connecté.", 'warning')
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if form.passwordRegister.data != form.confirmPasswordRegister.data:
            flash('Les mots de passe sont différents.', 'danger')
        elif data.checkIfExist(form.usernameRegister.data):
            flash("Un compte avec le même nom d'utilisateur existe déjà.", 'danger')
        else:
            data.insertUser(form.usernameRegister.data, form.passwordRegister.data)
            flash('Compte enregistré !', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logger.info(f"Unregistered Access to {request.path} from {request.remote_addr}")
    if current_user.is_authenticated:
        flash("Vous êtes déjà connecté.", 'warning')
        return redirect(url_for('index'))
    next = request.args.get('next')
    if not is_safe_url(next):
        return abort(400)
    form = LoginForm()
    if form.validate_on_submit():
        if data.loginUser(form.usernameLogin.data, form.passwordLogin.data):
            user = User(form.usernameLogin.data)
            user.id = form.usernameLogin.data
            login_user(user)
            logger.info(f"[={current_user.id} Login from {request.remote_addr}")
            return redirect(next or url_for('index'))
        else:
            flash("Mauvais nom d'utilisateur ou mot de passe.", 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logger.info(f"{current_user.id} Logout from {request.remote_addr}")
    logout_user()
    flash("Vous êtes déconnecté.", 'success')
    return redirect(url_for('index'))

@app.route('/stats')
@login_required
def stats():
    logger.info(f"{current_user.id} Access to {request.path} from {request.remote_addr}")
    flash("Page en construction.", 'warning')
    return redirect(url_for('index'))

@app.route('/mj')
@login_required
def mj():
    logger.info(f"{current_user.id} Access to {request.path} from {request.remote_addr}")
    if not data.getUser(current_user.id).is_admin:
        flash("Vous n'êtes pas MJ.", 'danger')
        return redirect(url_for('index'))
    return render_template('mj.html', PageName="Maitre du jeu")

@app.route('/mjAction')
@login_required
def mjAction():
    logger.info(f"{current_user.id} Access to {request.path} from {request.remote_addr}")
    if not data.getUser(current_user.id).is_admin:
        flash("Vous n'êtes pas MJ.", 'danger')
        return redirect(url_for('index'))
    action = request.args.get('action')
    if action == 'gamemode':
        mode = request.args.get('mode')
        pseudo = request.args.get('pseudo')
        response = rcon.send_command(f"gamemode {mode} {pseudo}")
        flash(response, 'success')
        return response


if __name__ == '__main__':
    config = Config("./config.yml")
    logger = Logger()
    rcon = MinecraftRcon()
    data = Database(f"{config.getDBHost()}", config.getDBUser(), config.getDBPassword(), config.getDBDatabase())
    args = readArgs()
    logger.info("Starting program")
    port = 9123
    host = '0.0.0.0'
    if args.port != None:
        port = args.port
    if args.host != None:
        host = args.host
    flaskLog = logging.getLogger('werkzeug')
    flaskLog.disabled = True
    flask.cli.show_server_banner = lambda *args: None
    logger.info(f"Starting web server on {host}:{port}")
    app.run(port=port,host=host,debug=args.debug)

