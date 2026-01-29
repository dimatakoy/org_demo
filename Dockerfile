# ------------------------------------------------------------------------------------
# Stage 1: Builder
# ------------------------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder

# Force uv to copy files into the venv instead of symlinking.
# This makes the /app/.venv folder portable to the next stage.
ENV UV_COMPILE_BYTECODE=1 
ENV UV_LINK_MODE=copy 
ENV UV_PYTHON_DOWNLOADS=0

# Install build dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Install dependencies (Cached layer)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# 2. Copy source code
COPY . /app

# 3. Install the project (creates the actual venv with source code linked/installed)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# ------------------------------------------------------------------------------------
# Stage 2: Runtime
# ------------------------------------------------------------------------------------
FROM python:3.13-slim-trixie

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Create a non-root user
RUN groupadd -r app_user && useradd -r -g app_user -d /app -s /sbin/nologin app_user

# Install runtime dependencies (no gcc/g++ needed here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the application from the builder
COPY --from=builder --chown=app_user:app_user /app /app

# Switch to non-root user
USER app_user
