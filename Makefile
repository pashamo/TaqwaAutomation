setup: requirements.txt
	pip3 install -r requirements.txt
run: 
	python3 integrated.py
clean:
	rm -rf __pycache__