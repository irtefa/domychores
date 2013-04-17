.PHONY: all test db init clean

all: clean
	python server.py

test:
	python test/all_tests.py

db:
	python models.py

init:
	pip install -r requirements.txt

clean:
	rm -rf dist *egg* *.pyc
