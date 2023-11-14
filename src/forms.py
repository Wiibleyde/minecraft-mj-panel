from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    usernameLogin = StringField('usernameLogin', validators=[DataRequired()], render_kw={"placeholder": "Nom d'utilisateur","autofocus": True, "class": "text-black"})
    passwordLogin = PasswordField('passwordLogin', validators=[DataRequired()], render_kw={"placeholder": "Mot de passe", "class": "text-black"})
    submitLogin = SubmitField('submitLogin', render_kw={"value": "Se connecter"})

class RegisterForm(FlaskForm):
    usernameRegister = StringField('usernameRegister', validators=[DataRequired()], render_kw={"placeholder": "Nom d'utilisateur","autofocus": True})
    passwordRegister = PasswordField('passwordRegister', validators=[DataRequired()], render_kw={"placeholder": "Mot de passe"})
    confirmPasswordRegister = PasswordField('confirmPasswordRegister', validators=[DataRequired()], render_kw={"placeholder": "Confirmer le mot de passe"})
    submitRegister = SubmitField('submitRegister', render_kw={"value": "S'inscrire"})