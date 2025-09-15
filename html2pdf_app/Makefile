# Makefile
VENV?=.venv
PYTHON?=$(VENV)/bin/python
PIP?=$(VENV)/bin/pip

.PHONY: venv install run test format lint typecheck docker-build docker-up clean re

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	# Installe le navigateur headless requis par Playwright
	$(PYTHON) -m playwright install chromium
	# Si tu es sous Linux/WSL et qu’il manque des libs systèmes, décommente :
	# $(PYTHON) -m playwright install-deps

run:
	PYTHONPATH=. FLASK_APP=app FLASK_DEBUG=1 $(PYTHON) -m flask run --port=8000

test:
	PYTHONPATH=. $(PYTHON) -m pytest tests/

format:
	$(VENV)/bin/black html2pdf/ tests/

lint:
	$(VENV)/bin/ruff check html2pdf/ tests/

typecheck:
	$(VENV)/bin/mypy html2pdf/

docker-build:
	docker build -t html2pdf_app .

docker-up:
	docker compose up --build

clean:
	rm -rf $(VENV) __pycache__ *.pyc

re: clean test

deps:
	# Installe les bibliothèques système nécessaires à Chromium de Playwright
	sudo $(PYTHON) -m playwright install-deps