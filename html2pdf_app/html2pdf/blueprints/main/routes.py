# routes.py
from flask import (
    render_template, redirect, url_for, session,
    current_app, send_from_directory, flash
)
import os
import datetime
from markupsafe import Markup
from . import main_bp
from .forms import DocumentForm
from .services import PdfService, StorageService


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/form", methods=["GET", "POST"])
def form():
    form = DocumentForm()
    if form.validate_on_submit():
        # On fabrique un payload propre pour l’aperçu (et le PDF)
        preview = {
            "nom": form.nom.data,
            "email": form.email.data,
            "titre": form.titre.data,
            "corps": form.corps.data,  # stocké brut; on le marquera safe à l’affichage
            "date": datetime.datetime.now().strftime("%d %B %Y"),
        }
        session["preview"] = preview
        return redirect(url_for("main.preview"))
    return render_template("form.html", form=form)


@main_bp.route("/preview", methods=["GET"])
def preview():
    data = session.get("preview")
    if not data:
        flash("Veuillez remplir le formulaire avant de prévisualiser.")
        return redirect(url_for("main.form"))

    # On repasse un formulaire juste pour avoir un csrf_token disponible
    form = DocumentForm(data=data)

    return render_template(
        "preview.html",
        form=form,
        nom=data["nom"],
        email=data["email"],
        titre=data["titre"],
        corps=Markup(data["corps"]),  # rendu HTML autorisé
        date=data["date"],
    )


@main_bp.route("/pdf", methods=["POST"])
def generate_pdf():
    data = session.get("preview")
    if not data:
        flash("La prévisualisation a expiré. Merci de recommencer.")
        return redirect(url_for("main.form"))

    # Générer le HTML du PDF depuis un template dédié
    html = render_template("pdf_template.html", **data)

    # Générer le PDF (bytes)
    pdf_bytes = PdfService.render_html_to_pdf(html)

    # Dossier de sortie
    generated_dir = os.path.join(current_app.instance_path, "generated")
    os.makedirs(generated_dir, exist_ok=True)

    # Nom de fichier
    filename = StorageService.unique_filename(data.get("titre", "document"))
    StorageService.save_pdf(pdf_bytes, filename, generated_dir)

    # Nettoyage optionnel
    session.pop("preview", None)

    flash("PDF généré avec succès.")
    return redirect(url_for("main.history"))


@main_bp.route("/history")
def history():
    from pathlib import Path
    generated_dir = Path(current_app.instance_path) / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    files = sorted((f.name for f in generated_dir.glob("*.pdf")), reverse=True)
    return render_template("history.html", files=files)


@main_bp.route("/download/<filename>")
def download(filename):
    from werkzeug.utils import secure_filename
    filename = secure_filename(filename)
    generated_dir = os.path.join(current_app.instance_path, "generated")
    return send_from_directory(generated_dir, filename, as_attachment=True)
