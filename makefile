install: venv
	. venv/bin/activate; pip3 install -Ur requirements.txt;

venv :
	test -d venv || python3 -m venv venv

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
	rm K-means.txt

test:
	. venv/bin/activate; python3 main.py