# README.md

# Mini-App HTML → PDF

Application Flask permettant de saisir un document via formulaire, prévisualiser en HTML, puis générer un PDF fidèle (WeasyPrint).

## Prérequis
- Python 3.11+
- (ou) Docker/Docker Compose

## Installation locale
```sh
make venv
make install
```

## Lancement (développement)
```sh
make run
```
Accès : http://localhost:8000

## Lancement avec Docker Compose
```sh
make docker-up
```

## Démo pas à pas
1. Accédez à `/form` pour saisir un document.
2. Prévisualisez le rendu HTML.
3. Générez et téléchargez le PDF.
4. Consultez l’historique des PDFs générés via `/history`.

## Arborescence
```
html2pdf_app/
  app.py
  config.py
  wsgi.py
  requirements.txt
  Makefile
  ...
```

## Commandes Makefile
- `make venv` : crée l’environnement virtuel
- `make install` : installe les dépendances
- `make run` : lance Flask (dev)
- `make test` : lance les tests
- `make format` : black
- `make lint` : ruff
- `make typecheck` : mypy
- `make docker-build` : build Docker
- `make docker-up` : run Docker Compose

## Limitations & améliorations
- Pas d’éditeur riche (balises HTML simples supportées)
- Pas d’authentification
- Pas de base de données (option bonus possible)
- Améliorations : éditeur WYSIWYG, DB, gestion utilisateurs

## Sécurité
- CSRF activé
- En-têtes HTTP de base
- Clé secrète via `.env`

## Structure
- POO : services (PDF, stockage)
- Templates Jinja2 (héritage, partials)
- Bootstrap 5 + CSS custom
- Tests unitaires et fonctionnels

---

© 2024 Mini-App HTML → PDF
