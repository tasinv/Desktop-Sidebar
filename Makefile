.PHONY: venv install run build test clean

venv:
	python3 -m venv .venv

install: venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	. .venv/bin/activate && python -m desktop_sidebar

build:
	pyinstaller --noconfirm --clean --name desktop_sidebar --onefile src/desktop_sidebar/__main__.py

test:
	. .venv/bin/activate && pytest -q

clean:
	rm -rf build dist *.spec .venv
