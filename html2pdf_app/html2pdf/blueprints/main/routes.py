# routes.py
from flask import (
    render_template, redirect, url_for, session,
    current_app, send_from_directory, flash, request, abort
)
import os
import datetime
from pathlib import Path
from markupsafe import Markup

from . import main_bp
from .forms import DocumentForm, UrlToPdfForm
from .services import PdfService, StorageService


@main_bp.route("/")
def index():
    # Page d’accueil avec le formulaire URL → PDF
    return render_template("index.html", url_form=UrlToPdfForm())


@main_bp.route("/form", methods=["GET", "POST"])
def form():
    form = DocumentForm()
    if form.validate_on_submit():
        preview = {
            "nom": form.nom.data,
            "email": form.email.data,
            "titre": form.titre.data,
            "corps": form.corps.data,
            "date": datetime.datetime.now().strftime("%d %B %Y"),
        }
        session["preview"] = preview
        return redirect(url_for("main.preview"))
    return render_template("form.html", form=form)


@main_bp.route("/preview", methods=["GET"])
def preview():
    data = session.get("preview")
    if not data:
        flash("Veuillez remplir le formulaire avant de prévisualiser.", "warning")
        return redirect(url_for("main.form"))

    form = DocumentForm(data=data)

    return render_template(
        "preview.html",
        form=form,
        nom=data["nom"],
        email=data["email"],
        titre=data["titre"],
        corps=Markup(data["corps"]),
        date=data["date"],
    )


@main_bp.route("/pdf", methods=["POST"])
def generate_pdf():
    data = session.get("preview")
    if not data:
        flash("La prévisualisation a expiré. Merci de recommencer.", "warning")
        return redirect(url_for("main.form"))

    html = render_template("pdf_template.html", **data)
    pdf_bytes = PdfService.render_html_to_pdf(html)

    generated_dir = Path(current_app.instance_path) / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    filename = StorageService.unique_filename(data.get("titre", "document"))
    (generated_dir / filename).write_bytes(pdf_bytes)

    session.pop("preview", None)
    flash("PDF généré avec succès.", "success")
    return redirect(url_for("main.history"))


@main_bp.route("/convert/url", methods=["POST"])
def convert_url():
    """
    Conversion d'une URL en PDF via Chromium headless (Playwright)
    """
    form = UrlToPdfForm()
    if not form.validate_on_submit():
        flash("Requête invalide. Vérifiez l’URL saisie.", "danger")
        return abort(400)

    url = form.url.data.strip()
    # Optionnel : restreindre aux schémas http/https
    if not (url.startswith("http://") or url.startswith("https://")):
        flash("Seules les URLs http(s) sont acceptées.", "danger")
        return abort(400)

    # Nom de fichier
    base_name = form.filename.data.strip() if form.filename.data else "document"
    filename = StorageService.unique_filename(base_name)

    # Rendu PDF (navigateur)
    pdf_bytes = PdfService.render_url_to_pdf(url)

    # Sauvegarde
    generated_dir = Path(current_app.instance_path) / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    (generated_dir / filename).write_bytes(pdf_bytes)

    flash("PDF généré à partir de l’URL.", "success")
    return redirect(url_for("main.history"))


@main_bp.route("/history")
def history():
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
