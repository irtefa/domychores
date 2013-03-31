.PHONY: all init clean

all: clean
	python server.py 8888

init:
	pip install -r requirements.txt

clean:
	rm -rf dist *egg*
