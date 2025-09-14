.PHONY: clean venv install test

venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip

install: venv
	. .venv/bin/activate && pip install -r requirements.txt
	. .venv/bin/activate && pip install pytest

test: install
	. .venv/bin/activate && python -m pytest tests/

clean:
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
