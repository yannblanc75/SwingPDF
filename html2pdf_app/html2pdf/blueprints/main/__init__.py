# html2pdf/blueprints/main/__init__.py
from flask import Blueprint

# Le nom DOIT être "main"
main_bp = Blueprint("main", __name__, template_folder="../../templates", static_folder="../../static")

from . import routes  # noqa: E402,F401  (importe les routes pour les enregistrer)
