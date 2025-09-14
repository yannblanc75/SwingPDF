.PHONY: venv install test clean re

venv:
	python3 -m venv html2pdf_app/.venv
	. html2pdf_app/.venv/bin/activate && pip install --upgrade pip

install: venv
	. html2pdf_app/.venv/bin/activate && pip install -r requirements.txt
	. html2pdf_app/.venv/bin/activate && pip install pytest flask weasyprint

test: install
	. html2pdf_app/.venv/bin/activate && python -m pytest html2pdf_app/tests/

clean:
	rm -rf html2pdf_app/.venv/
	find html2pdf_app -type d -name "__pycache__" -exec rm -rf {} +
	find html2pdf_app -type f -name "*.pyc" -delete
	find html2pdf_app -type d -name ".pytest_cache" -exec rm -rf {} +

re: clean test