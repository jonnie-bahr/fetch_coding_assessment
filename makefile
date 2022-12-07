run:
	uvicorn main:app
setup: requirements.txt
	pip3 install -r requirements.txt
test:
	pytest