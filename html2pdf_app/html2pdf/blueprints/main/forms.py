# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, URL


class DocumentForm(FlaskForm):
    nom = StringField(
        "Nom",
        validators=[DataRequired(), Length(max=50)],
        render_kw={"placeholder": "Votre nom"},
        description="Votre nom complet.",
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
        render_kw={"placeholder": "exemple@email.com"},
        description="Adresse email valide.",
    )
    titre = StringField(
        "Titre du document",
        validators=[DataRequired(), Length(max=100)],
        render_kw={"placeholder": "Titre du document"},
        description="Titre affiché en en-tête.",
    )
    corps = TextAreaField(
        "Corps du document",
        validators=[DataRequired(), Length(max=2000)],
        render_kw={
            "placeholder": "Contenu riche (balises <b>, <i>, <ul>, <li>, <br> autorisées)"
        },
        description="Vous pouvez utiliser <b>, <i>, <ul>, <li>, <br>.",
    )
    submit = SubmitField("Prévisualiser")


class UrlToPdfForm(FlaskForm):
    url = StringField(
        "Adresse de la page",
        validators=[
            DataRequired(message="Saisissez l’URL à convertir."),
            URL(require_tld=True, message="URL invalide."),
            Length(max=2048),
        ],
        render_kw={"placeholder": "https://exemple.com/page"},
        description="L’URL doit être accessible publiquement.",
    )
    filename = StringField(
        "Nom du fichier (optionnel)",
        validators=[Optional(), Length(max=80)],
        render_kw={"placeholder": "nom_du_document"},
        description="Sans extension; .pdf sera ajouté.",
    )
    submit = SubmitField("Convertir")
