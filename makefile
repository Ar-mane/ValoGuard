
.PHONY: dev build install clean

dev:
	python3 src/main.py

build:
	pyinstaller main.spec

install:
	pip install pythonnet --pre && pip install pywebview keyboard

clean:
	rm -rf dist build __pycache__ *.spec
