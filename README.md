# textmood-lite

A tiny keyword-based mood detector for text. Given a sentence, it tells you whether it sounds **happy**, **sad**, **angry**, **anxious**, or **neutral**.

This project was built as a hands-on way to learn the full modern Python package ecosystem — from a blank file in VS Code all the way through CI/CD, containerization, and publishing to PyPI. This document is a **complete, reproducible build log**: every command run and every file's full content, in the order they happened.

```bash
pip install textmood-lite
```

---

## Table of Contents

- [Ecosystem Roadmap](#ecosystem-roadmap)
- [Project Structure](#project-structure)
- [Phase 1 — Project Setup](#phase-1--project-setup)
- [Phase 2 — Core Logic](#phase-2--core-logic)
- [Phase 3 — Formatting, Linting, Type Checking](#phase-3--formatting-linting-type-checking)
- [Phase 4 — Testing](#phase-4--testing)
- [Phase 5 — Git & GitHub](#phase-5--git--github)
- [Phase 6 — CI/CD with GitHub Actions](#phase-6--cicd-with-github-actions)
- [Phase 7 — Documentation (MkDocs)](#phase-7--documentation-mkdocs)
- [Phase 8 — Pre-commit Hooks](#phase-8--pre-commit-hooks)
- [Phase 9 — CLI with Typer](#phase-9--cli-with-typer)
- [Phase 10 — Runtime Server (FastAPI + Uvicorn)](#phase-10--runtime-server-fastapi--uvicorn)
- [Phase 11 — Package Publishing (PyPI)](#phase-11--package-publishing-pypi)
- [Phase 12 — Docker](#phase-12--docker)
- [Phase 13 — Makefile & CI Caching](#phase-13--makefile--ci-caching)
- [Final pyproject.toml](#final-pyprojecttoml-complete-all-phases-merged)
- [All Setup Commands, In Order](#all-setup-commands-in-order-copy-paste-reference)
- [Errors Faced & How They Were Fixed](#errors-faced--how-they-were-fixed)

---

## Ecosystem Roadmap

| # | Phase | Tools | Status |
|---|-------|-------|--------|
| 1 | Project Templating | Cookiecutter, Jinja | ✅ |
| 2 | Project Management | `pyproject.toml`, venv, src-layout | ✅ |
| 3 | Formatting | Black | ✅ |
| 4 | Linting | Ruff | ✅ |
| 5 | Type Checking | mypy | ✅ |
| 6 | Pre-Commit Checks | pre-commit | ✅ |
| 7 | Testing | pytest, unit + integration tests | ✅ |
| 8 | CLI Upgrade | Typer | ✅ |
| 9 | Runtime Server | FastAPI, Uvicorn | ✅ |
| 10 | CI/CD | GitHub Actions (matrix, caching) | ✅ |
| 11 | Documentation | MkDocs Material, GitHub Pages | ✅ |
| 12 | Package Publishing | `build`, `twine`, PyPI Trusted Publisher | ✅ |
| 13 | Containerization | Docker, multi-stage build, docker-compose | ✅ |
| 14 | Deployment | AWS / GCP / Azure / Render | ⬜ |
| 15 | Orchestration | Kubernetes, Helm | ⬜ |
| 16 | Monitoring | Prometheus, Grafana | ⬜ |
| 17 | Logging & Tracing | OpenTelemetry, Loki | ⬜ |
| 18 | Security | Dependabot, Snyk, Gitleaks | ⬜ |
| 19 | Release Management | Commitizen, semantic-release | ⬜ |
| 20 | Production Platform Engineering | Docker + Kubernetes + Helm + KEDA | ⬜ |
| 21 | Plugin Ecosystem | Pluggy, Entry Points | ⬜ |
| 22 | Parallel Testing | pytest-xdist | ⬜ |

---

## Project Structure

```
textmood-lite/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── index.md
│   ├── usage.md
│   └── api.md
├── src/
│   └── textmood_lite/
│       ├── __init__.py
│       ├── core.py
│       ├── cli.py
│       └── api.py
├── tests/
│   ├── test_core.py
│   ├── test_cli.py
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile
├── mkdocs.yml
├── pyproject.toml
└── README.md
```

---

## Phase 1 — Project Setup

```bash
mkdir textmood-lite
cd textmood-lite
code .

git init
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1

mkdir -p src/textmood_lite tests
touch src/textmood_lite/__init__.py src/textmood_lite/core.py src/textmood_lite/cli.py tests/test_core.py
touch README.md pyproject.toml
```

**`.gitignore`**
```
__pycache__/
*.pyc
.venv/
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
build/
*.egg-info/
.coverage
```

**`pyproject.toml`** (initial version)
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "textmood-lite"
version = "0.1.0"
description = "A tiny keyword-based mood detector for text"
authors = [{name = "Your Name", email = "you@example.com"}]
readme = "README.md"
requires-python = ">=3.9"
license = "MIT"

[project.scripts]
textmood = "textmood_lite.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/textmood_lite"]
```

```bash
pip install -e .
```

---

## Phase 2 — Core Logic

**`src/textmood_lite/core.py`**
```python
"""Core mood-detection logic for textmood-lite."""

import re

_LEXICON = {
    "happy": {"happy", "joy", "great", "excited", "love", "wonderful", "glad"},
    "sad": {"sad", "down", "unhappy", "depressed", "cry", "miserable", "lonely"},
    "angry": {"angry", "mad", "furious", "annoyed", "hate", "rage"},
    "anxious": {"worried", "nervous", "anxious", "scared", "afraid", "stressed"},
}


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z']+", text.lower())


def analyze(text: str) -> dict[str, int]:
    """Return a score for each mood found in the text."""
    tokens = _tokenize(text)
    scores = {mood: 0 for mood in _LEXICON}
    for token in tokens:
        for mood, words in _LEXICON.items():
            if token in words:
                scores[mood] += 1
    return scores


def dominant_mood(text: str) -> str:
    """Return the single mood with the highest score, or 'neutral'."""
    scores = analyze(text)
    if not any(scores.values()):
        return "neutral"
    return max(scores, key=lambda mood: scores[mood])
```

**`src/textmood_lite/__init__.py`**
```python
from .core import analyze, dominant_mood

__all__ = ["analyze", "dominant_mood"]
```

```bash
textmood "I am so happy and excited today"
# happy
```

---

## Phase 3 — Formatting, Linting, Type Checking

```bash
pip install black ruff mypy
pip install -e ".[dev]"
```

**Additions to `pyproject.toml`**
```toml
[project.optional-dependencies]
dev = ["black", "ruff", "mypy", "pytest"]

[tool.black]
line-length = 88
target-version = ["py310"]

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.mypy]
python_version = "3.10"
warn_unused_ignores = true
```

```bash
black .
ruff check .
ruff check --fix .
mypy src
```

---

## Phase 4 — Testing

```bash
pytest -v
```

**`tests/test_core.py`**
```python
from textmood_lite.core import dominant_mood


def test_happy_text():
    assert dominant_mood("I am so happy and excited today") == "happy"


def test_empty_text():
    assert dominant_mood("") == "neutral"


def test_no_keywords():
    assert dominant_mood("The sky is blue") == "neutral"
```

**`tests/test_cli.py`** (integration test — runs the CLI as a real subprocess)
```python
import subprocess
import sys


def test_cli_outputs_mood():
    result = subprocess.run(
        [sys.executable, "-m", "textmood_lite.cli", "I am happy and excited"],
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "happy"


def test_cli_detailed_flag():
    result = subprocess.run(
        [sys.executable, "-m", "textmood_lite.cli", "I am happy", "--detailed"],
        capture_output=True,
        text=True,
    )
    assert "happy" in result.stdout
    assert "sad" in result.stdout


def test_cli_no_args_exits_with_error():
    result = subprocess.run(
        [sys.executable, "-m", "textmood_lite.cli"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
```

**Additions to `pyproject.toml`**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v"
```

```bash
pytest
```

---

## Phase 5 — Git & GitHub

```bash
git add .
git commit -m "Initial project skeleton for textmood-lite"
git branch -M main
git remote add origin https://github.com/<your-username>/textmood-lite.git
git push -u origin main

git checkout -b dev
git push -u origin dev
```

---

## Phase 6 — CI/CD with GitHub Actions

```bash
mkdir -p .github/workflows
```

**`.github/workflows/ci.yml`** (final version, with caching and publish job — see Phase 13 too)
```yaml
name: CI

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install black ruff mypy pytest httpx2
          pip install "typer[all]" fastapi uvicorn
          pip install -e .

      - name: Check formatting with Black
        run: black --check .

      - name: Lint with Ruff
        run: ruff check .

      - name: Type check with mypy
        run: mypy src

      - name: Run tests
        run: pytest

  publish:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: pypi
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install build tools
        run: pip install build

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

```bash
git add .github/workflows/ci.yml
git commit -m "Add CI workflow: format, lint, type-check, test"
git push
```

---

## Phase 7 — Documentation (MkDocs)

```bash
pip install mkdocs mkdocs-material "mkdocstrings[python]"
```

**Additions to `pyproject.toml`**
```toml
[project.optional-dependencies]
docs = ["mkdocs", "mkdocs-material", "mkdocstrings[python]"]
```

**`mkdocs.yml`**
```yaml
site_name: textmood-lite
theme:
  name: material
nav:
  - Home: index.md
  - Usage: usage.md
  - API Reference: api.md
plugins:
  - mkdocstrings
```

**`docs/index.md`**
```markdown
# textmood-lite

A tiny keyword-based mood detector for text. Given a sentence, it tells you whether it sounds happy, sad, angry, anxious, or neutral.
```

**`docs/usage.md`**
````markdown
# Usage

## As a command-line tool

```bash
textmood "I am so happy and excited today"
# happy
```

## As a Python library

```python
from textmood_lite import dominant_mood

dominant_mood("I am so happy and excited today")
# "happy"
```
````

**`docs/api.md`**
```markdown
# API Reference

::: textmood_lite.core
```

```bash
mkdocs serve
mkdocs gh-deploy
```

---

## Phase 8 — Pre-commit Hooks

```bash
pip install pre-commit
```

**Additions to `pyproject.toml`**
```toml
dev = ["black", "ruff", "mypy", "pytest", "pre-commit", "httpx2"]
```

**`.pre-commit-config.yaml`**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.1
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        args: [--ignore-missing-imports]
        additional_dependencies: []
```

```bash
pre-commit install
pre-commit run --all-files
```

---

## Phase 9 — CLI with Typer

```bash
pip install "typer[all]"
```

**Additions to `pyproject.toml`**
```toml
[project]
dependencies = ["typer[all]>=0.9.0"]
```

**`src/textmood_lite/cli.py`**
```python
"""CLI interface for textmood-lite."""

import typer
from textmood_lite.core import analyze, dominant_mood

app = typer.Typer(help="Detect the mood of any text.")


@app.command()
def detect(
    text: str = typer.Argument(..., help="The text to analyze"),
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show all mood scores"),
):
    """Detect the dominant mood of the given text."""
    if detailed:
        scores = analyze(text)
        for mood, score in scores.items():
            typer.echo(f"{mood}: {score}")
    else:
        mood = dominant_mood(text)
        typer.echo(mood)


def main():
    app()


if __name__ == "__main__":
    main()
```

```bash
textmood "I am so happy today"
textmood "I am so happy today" --detailed
textmood --help
```

---

## Phase 10 — Runtime Server (FastAPI + Uvicorn)

```bash
pip install fastapi uvicorn httpx2
```

**Additions to `pyproject.toml`**
```toml
[project]
dependencies = ["typer[all]>=0.9.0", "fastapi>=0.100.0", "uvicorn>=0.23.0"]
```

**`src/textmood_lite/api.py`**
```python
"""FastAPI web server for textmood-lite."""

from fastapi import FastAPI
from pydantic import BaseModel
from textmood_lite.core import analyze, dominant_mood

app = FastAPI(
    title="textmood-lite",
    description="A tiny keyword-based mood detector for text",
    version="0.1.0",
)


class TextInput(BaseModel):
    text: str


class MoodResponse(BaseModel):
    text: str
    dominant_mood: str
    scores: dict[str, int]

    model_config = {"from_attributes": True}


@app.get("/")
def root() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "textmood-lite"}


@app.post("/analyze", response_model=MoodResponse)
def analyze_post(input: TextInput) -> MoodResponse:
    """Analyze mood via POST request with JSON body."""
    return MoodResponse(
        text=input.text,
        dominant_mood=dominant_mood(input.text),
        scores=analyze(input.text),
    )


@app.get("/analyze", response_model=MoodResponse)
def analyze_get(text: str) -> MoodResponse:
    """Analyze mood via GET request with query parameter."""
    return MoodResponse(
        text=text,
        dominant_mood=dominant_mood(text),
        scores=analyze(text),
    )
```

**`tests/test_api.py`**
```python
from textmood_lite.api import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_post():
    response = client.post(
        "/analyze",
        json={"text": "I am so happy today"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["dominant_mood"] == "happy"
    assert "scores" in data


def test_analyze_get():
    response = client.get("/analyze?text=I%20am%20happy")
    assert response.status_code == 200
    assert response.json()["dominant_mood"] == "happy"
```

```bash
uvicorn textmood_lite.api:app --reload
# → http://127.0.0.1:8000

curl "http://127.0.0.1:8000/analyze?text=I%20am%20happy"

curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "I am happy"}'
```
Interactive docs: `http://127.0.0.1:8000/docs` and `http://127.0.0.1:8000/redoc`

---

## Phase 11 — Package Publishing (PyPI)

```bash
pip install build twine
```

**Additions to `pyproject.toml`**
```toml
dev = ["black", "ruff", "mypy", "pytest", "pre-commit", "httpx2", "build", "twine"]
```

```bash
python -m build
echo "dist/" >> .gitignore
```

**Manual upload (initial method, replaced by Trusted Publisher below):**
```bash
twine upload dist/*
# username: __token__
# password: pypi-xxxxxxxxxxxx
```

**Trusted Publisher setup (no token needed — used in production):**
On `pypi.org` → Account settings → Publishing → Add a new pending publisher:
- PyPI Project Name: `textmood-lite`
- Owner: `<your-github-username>`
- Repository name: `textmood-lite`
- Workflow name: `ci.yml`
- Environment name: `pypi`

On GitHub: **Settings → Environments → New environment** named `pypi`.

The `publish` job shown in Phase 6's `ci.yml` handles the rest automatically via `pypa/gh-action-pypi-publish@release/v1`.

```bash
pip install textmood-lite   # verify it's live
```

---

## Phase 12 — Docker

```bash
docker --version
# if missing (Ubuntu/WSL):
sudo apt-get update
sudo apt-get install docker.io -y
sudo systemctl start docker
sudo usermod -aG docker $USER
# then fully restart the shell session (or `wsl --shutdown` on Windows)
```

**`Dockerfile`**
```dockerfile
# Stage 1: Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Copy dependency files first (better layer caching)
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install the package
RUN pip install --no-cache-dir .

# Stage 2: Runtime stage
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/src ./src

# Expose port for FastAPI
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "textmood_lite.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`.dockerignore`**
```
.venv/
.git/
.github/
__pycache__/
*.pyc
*.egg-info/
dist/
.pytest_cache/
.mypy_cache/
.ruff_cache/
tests/
docs/
```
> Note: do **not** add `*.md` here — the `Dockerfile` explicitly needs `README.md` to exist in the build context.

**`docker-compose.yml`**
```yaml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

```bash
docker build -t textmood-lite:latest .
docker run -p 8000:8000 textmood-lite:latest

# or
docker compose up
docker compose down

# useful commands
docker ps
docker images
docker stop <container_id>
docker rmi textmood-lite:latest
docker run -d -p 8000:8000 textmood-lite:latest
docker logs <container_id>

curl "http://localhost:8000/analyze?text=I%20am%20happy"
```

---

## Phase 13 — Makefile & CI Caching

**`Makefile`** (recipe lines must use a real **tab**, not spaces)
```makefile
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
```

If `make` fails with files created via an editor that auto-converts tabs to spaces, recreate it from the terminal to guarantee real tabs:
```bash
cat > Makefile << 'EOF'
install:
	pip install -e ".[dev]"
EOF
```

**Pip caching in CI** — added to both `setup-python` steps in `ci.yml`:
```yaml
- name: Set up Python ${{ matrix.python-version }}
  uses: actions/setup-python@v5
  with:
    python-version: ${{ matrix.python-version }}
    cache: "pip"
```

```bash
make install
make format
make lint
make typecheck
make test
make check
make build
make run
make docker-build
make docker-run
make clean
```

---

## Final `pyproject.toml` (complete, all phases merged)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "textmood-lite"
version = "0.1.0"
description = "A tiny keyword-based mood detector for text"
authors = [{name = "Your Name", email = "you@example.com"}]
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
dependencies = ["typer[all]>=0.9.0", "fastapi>=0.100.0", "uvicorn>=0.23.0"]

[project.scripts]
textmood = "textmood_lite.cli:main"

[project.optional-dependencies]
dev = ["black", "ruff", "mypy", "pytest", "pre-commit", "httpx2", "build", "twine"]
docs = ["mkdocs", "mkdocs-material", "mkdocstrings[python]"]

[tool.hatch.build.targets.wheel]
packages = ["src/textmood_lite"]

[tool.black]
line-length = 88
target-version = ["py310"]

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.mypy]
python_version = "3.10"
warn_unused_ignores = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v"
```

---

## All Setup Commands, In Order (copy-paste reference)

```bash
# 1. Project init
mkdir textmood-lite && cd textmood-lite
code .
git init
python -m venv .venv
source .venv/bin/activate
mkdir -p src/textmood_lite tests
touch src/textmood_lite/__init__.py src/textmood_lite/core.py src/textmood_lite/cli.py tests/test_core.py
touch README.md pyproject.toml
pip install -e .

# 2. Formatting / Linting / Type checking
pip install black ruff mypy
pip install -e ".[dev]"
black .
ruff check --fix .
mypy src

# 3. Testing
pytest -v

# 4. Git / GitHub
git add .
git commit -m "Initial project skeleton for textmood-lite"
git branch -M main
git remote add origin https://github.com/<your-username>/textmood-lite.git
git push -u origin main
git checkout -b dev
git push -u origin dev

# 5. CI/CD
mkdir -p .github/workflows
git add .github/workflows/ci.yml
git commit -m "Add CI workflow"
git push

# 6. Docs
pip install mkdocs mkdocs-material "mkdocstrings[python]"
mkdocs serve
mkdocs gh-deploy

# 7. Pre-commit
pip install pre-commit
pre-commit install
pre-commit run --all-files

# 8. Typer CLI
pip install "typer[all]"

# 9. FastAPI + Uvicorn
pip install fastapi uvicorn httpx2
uvicorn textmood_lite.api:app --reload

# 10. Publishing
pip install build twine
python -m build
twine upload dist/*
pip install textmood-lite

# 11. Docker
sudo apt-get install docker.io -y
sudo systemctl start docker
sudo usermod -aG docker $USER
docker build -t textmood-lite:latest .
docker run -p 8000:8000 textmood-lite:latest

# 12. Makefile
make check
make docker-build
make clean
```

---

## Errors Faced & How They Were Fixed

### 1. Black warning about Python version mismatch
```
Warning: Python 3.14 cannot parse code formatted for Python 3.15...
```
**Fix:** Pin an explicit target version in `pyproject.toml`:
```toml
[tool.black]
target-version = ["py310"]
```

### 2. Ruff: unsorted imports
```
I001 Import block is un-sorted or un-formatted
```
**Fix:** `ruff check --fix .`

### 3. mypy: unsupported Python version target
```
pyproject.toml: [mypy]: python_version: Python 3.9 is not supported (must be 3.10 or higher)
```
**Fix:** `[tool.mypy] python_version = "3.10"`

### 4. mypy: `max()` with `dict.get` as key function
```
error: Argument "key" to "max" has incompatible type ... [arg-type]
```
**Fix:**
```python
return max(scores, key=lambda mood: scores[mood])
```

### 5. CI failing: `black: command not found`
**Cause:** Local `pyproject.toml` changes (dev extras) were never committed/pushed.
**Fix:** `git status` → commit and push everything before assuming CI sees it.

### 6. CI: un-formatted test file
```
would reformat tests/test_cli.py
```
**Fix:** Run `black .` (not `--check`) locally before pushing.

### 7. Ruff: `F811` redefinition of a function
```
F811 Redefinition of unused `test_cli_no_args_shows_usage` from line 14
```
**Cause:** Duplicate test function pasted twice; also a `rext=True` typo (should be `text=True`).
**Fix:** Removed duplicate, fixed typo.

### 8. pre-commit blocking a commit (expected behavior)
```
black....................................................................Failed
- files were modified by this hook
```
**Fix:**
```bash
git add .
git commit -m "..."
```

### 9. FastAPI response missing fields
```json
{"text":"I am happy"}
```
**Cause:** Typo (`score=` instead of `scores=`), missing `response_model=`, and a duplicate `@app.get("/analyze")` route overriding the real one.
**Fix:** Removed duplicate route, fixed typo, added `response_model` consistently.

### 10. `curl: (3) URL rejected: Malformed input`
**Fix:** URL-encode spaces:
```bash
curl "http://127.0.0.1:8000/analyze?text=I%20am%20happy"
```

### 11. CI: `TypeError: Field 'project.dependencies' must be an array`
**Cause:** Two `[project]` table headers in `pyproject.toml` (TOML disallows duplicates).
**Fix:** Merge into a single `[project]` block.

### 12. Accidentally committed nested git repositories
```
warning: adding embedded git repository: Python-Boilerplate
```
**Fix:**
```bash
mv Python-Boilerplate ~/projects/Python-Boilerplate
mv textmood_lite ~/projects/textmood_lite
git rm -r --cached Python-Boilerplate textmood_lite
git commit -m "Remove accidentally added submodules"
```

### 13. PyPI: "Two-factor authentication must be enabled"
**Fix:** Enable 2FA via an authenticator app before generating tokens or trusted publishers.

### 14. PyPI Trusted Publisher: "Invalid GitHub user or organization name"
**Fix:** Copy the exact GitHub username (case-sensitive) from the GitHub profile page.

### 15. `git push` → "has no upstream branch"
```
fatal: The current branch feature/publish has no upstream branch.
```
**Fix:**
```bash
git push --set-upstream origin feature/publish
```

### 16. Docker: permission denied on socket
```
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
```
**Fix (immediate):** `sudo docker build ...`
**Fix (permanent, WSL):** `wsl --shutdown` in PowerShell, then reopen VS Code.

### 17. Docker build: `COPY failed: README.md does not exist`
**Cause:** `.dockerignore` had a blanket `*.md` rule, blocking `README.md` even though `Dockerfile` needed it.
**Fix:** Remove `*.md` from `.dockerignore`.

### 18. `make`: "No rule to make target"
**Cause:** Recipe lines indented with spaces instead of a real tab character.
**Fix:** Recreate the file via a heredoc in the terminal to guarantee literal tabs.

---

## License

MIT
