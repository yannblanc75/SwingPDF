# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class DocumentForm(FlaskForm):
    nom = StringField(
        "Nom",
        validators=[DataRequired(), Length(max=50)],
        render_kw={"placeholder": "Votre nom"},
        description="Votre nom complet."
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
        render_kw={"placeholder": "exemple@email.com"},
        description="Adresse email valide."
    )
    titre = StringField(
        "Titre du document",
        validators=[DataRequired(), Length(max=100)],
        render_kw={"placeholder": "Titre du document"},
        description="Titre affiché en en-tête."
    )
    corps = TextAreaField(
        "Corps du document",
        validators=[DataRequired(), Length(max=2000)],
        render_kw={"placeholder": "Contenu riche (balises <b>, <i>, <ul>, <li>, <br> autorisées)"},
        description="Vous pouvez utiliser <b>, <i>, <ul>, <li>, <br>."
    )
    submit = SubmitField("Prévisualiser")
