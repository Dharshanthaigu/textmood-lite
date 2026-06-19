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