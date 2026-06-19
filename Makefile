.PHONY: install format lint typecheck test build run docker-build docker-run clean check

install:
	pip install -e ".[dev]"

format:
	black .

lint:
	ruff check .

typecheck:
	mypy src

test:
	pytest

check: format lint typecheck test

build:
	python -m build

run:
	uvicorn textmood_lite.api:app --reload

docker-build:
	docker build -t textmood-lite:latest .

docker-run:
	docker run -p 8000:8000 textmood-lite:latest

clean:
	rm -rf dist/ build/ .pytest_cache/ .mypy_cache/ .ruff_cache/ __pycache__/
