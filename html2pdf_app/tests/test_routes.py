# test_routes.py
import pytest
from flask import url_for
from html2pdf import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Ajoute cette ligne
    with app.test_client() as client:
        yield client

def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Bienvenue" in resp.data.decode("utf-8")

def test_form_get(client):
    resp = client.get("/form")
    assert resp.status_code == 200
    assert "Créer un document" in resp.data.decode("utf-8")

def test_preview_post_valid(client):
    data = {
        "nom": "Test User",
        "email": "test@example.com",
        "titre": "Titre Test",
        "corps": "<b>Corps</b> du document"
    }
    resp = client.post("/form", data=data, follow_redirects=True)
    assert "Aperçu du document" in resp.data.decode("utf-8")

def test_preview_post_invalid(client):
    data = {"nom": "", "email": "bad", "titre": "", "corps": ""}
    resp = client.post("/form", data=data)
    html = resp.data.decode("utf-8")
    print(html)
    assert "Créer un document" in html
    assert (
        "Ce champ est obligatoire" in html
        or "Ce champ est obligatoire." in html
        or "Adresse email non valide" in html
        or "Adresse email non valide." in html
        or "This field is required." in html
        or "Invalid email address." in html
    )

def test_pdf_generation(client):
    data = {
        "nom": "Test User",
        "email": "test@example.com",
        "titre": "Titre Test",
        "corps": "<b>Corps</b> du document"
    }
    client.post("/form", data=data)
    resp = client.post("/pdf")
    assert resp.status_code == 200
    assert resp.mimetype == "application/pdf"
    assert resp.data.startswith(b'%PDF')
