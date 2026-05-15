VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

build: venv install

venv:
	python3 -m venv $(VENV)


install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PY) lightcurve_app.py

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
