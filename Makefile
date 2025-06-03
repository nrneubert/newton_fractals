
.PHONY : install

VENV_NAME := "virtualenv"
REQUIREMENTS := "requirements.txt"

install:
	python3 -m venv $(VENV_NAME)
	./$(VENV_NAME)/bin/pip install -r $(REQUIREMENTS)


