setup:
	python src/poetry2setup.py > setup.py

build: setup shiv

clean:
	rm setup.py

shiv:
	shiv -c utils -o utils .
