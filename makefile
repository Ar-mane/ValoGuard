
.PHONY: dev build install clean

dev:
	python src/main.py

build:
	python -m PyInstaller main.spec

install:
	pip install -r requirements.txt

clean:
	powershell -Command "Remove-Item -Path dist, build, __pycache__ -Recurse -Force -ErrorAction SilentlyContinue"
