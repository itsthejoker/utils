setup:
	.venv/bin/python src/poetry2setup.py > setup.py

build: setup shiv

clean:
	rm setup.py

shiv:
	.venv/bin/shiv -c utils -o utils .