from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, ValidationError, TextAreaField, RadioField
from wtforms.validators import Email, EqualTo, DataRequired, Length
from wtforms.fields import BooleanField
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Felhasználónév:', validators=[DataRequired(message='Mező kitöltése kötelező!'), Length(min=3, max=30, message='Felhasználónévnek 3 és 30 karakter között kell lennie!')])
    email = EmailField('Email cím:', validators=[DataRequired(message='Mező kitöltése kötelező!'), Email(message='Nem érvényes Email cím!')])
    password = PasswordField('Jelszó:', validators=[DataRequired(message='Mező kitöltése kötelező!'), Length(min=6, message='Minimum 6 karakternek kell lennie!')])
    confirm_password = PasswordField('Jelszó megerősítés', validators=[DataRequired(message='Kitöltése kötelező!'), EqualTo('password', message='Jelszavak nem egyeznek!')])
    submit = SubmitField('Küldés')
    
    def validate_email(self, check_email):
        if check_email.data == self.email:
            raise ValidationError('Már létezik ez az email cím.')
        
    def validate_username(self, check_username):
        if check_username.data == self.username:
            raise ValidationError('Már létezik ez a felhasználónév.')
    
class LoginForm(FlaskForm):
    username = StringField('Felhasználónév:', validators=[DataRequired(message='Mező kitöltése kötelező!')])
    password = PasswordField('Jelszó:', validators=[DataRequired(message='Mező kitöltése kötelező!')])
    submit = SubmitField('Küldés')
    
class AccountForm(FlaskForm):
    username = StringField('Felhasználónév:', validators=[DataRequired(message='Mező kitöltése kötelező!'), Length(min=3, max=30, message='Felhasználónévnek 3 és 30 karakter között kell lennie!')])    
    email = EmailField('Email cím:', validators=[DataRequired(message='Mező kitöltése kötelező!'), Email(message='Nem érvényes Email cím!')])
    image = FileField('Profilkép feltöltése', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    default_image = BooleanField('Alapértelemezett kép')
    submit = SubmitField('Küldés')
    
    def validate_user(self, check_user):
        if (check_user.data != self.user.data):
            raise ValidationError('Nincs ilyen felhasználónév vagy email cím.')
        
class PostForm(FlaskForm):
    title = StringField('Cím:', validators=[DataRequired(), Length(min=3)])
    content = TextAreaField('Tartalom:', validators=[DataRequired(), Length(min=3)])
    new_category = StringField('Új kategória:')
    submit = SubmitField('Küldés')
    
class LearnForm(FlaskForm):
    desc = StringField('Új anyag:')
    add = SubmitField('+')
    