env:
	python3 -m venv venv

activate:
	source ./venv/bin/activate

install:
	pip install --break-system-packages flake8 mypy build


run:
	python3 a_maze_ing.py config.txt


debug:
	python3 -m pdb a_maze_ing.py config.txt


lint:
	flake8 .
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs


build-pkg:
	python3 -m build --outdir .


clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name dist -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "Clean done."


.PHONY: install run debug lint lint-strict clean build-pkg