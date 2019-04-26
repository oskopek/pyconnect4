clean:
	yapf -r -i .

check: clean
	flake8 .

types: check
	mypy main.py 2>&1

conda:
	# Make sure to install miniconda first.
	conda update conda
	conda create -n connect4 python=3.7
	conda install -n connect4 numpy flake8 yapf mypy

run:
	python main.py
