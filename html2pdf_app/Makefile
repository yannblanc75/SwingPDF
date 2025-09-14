# Makefile
VENV?=.venv
PYTHON?=$(VENV)/bin/python
PIP?=$(VENV)/bin/pip

.PHONY: venv install test clean re

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	FLASK_APP=app FLASK_DEBUG=1 $(PYTHON) -m flask run --port=8000

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
