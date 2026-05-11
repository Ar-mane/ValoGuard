
.PHONY: dev build install clean

dev:
	python src/main.py

build:
	python -m PyInstaller main.spec

install:
	pip install pythonnet --pre && pip install -r requirements.txt

clean:
	python -c "import shutil; [shutil.rmtree(d, ignore_errors=True) for d in ['dist', 'build', '__pycache__']]"
