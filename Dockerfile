
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    PORT=8000

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /uvx /bin/

WORKDIR /app

# Install dependencies dari uv.lock
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

# Salin source code
COPY . .

# Siapkan direktori media dan static
RUN mkdir -p /app/media /app/staticfiles \
    && cp -a /app/core/seed_media/. /app/media/

# Collect static files
RUN SECRET_KEY=dummy-build-secret-key \
    DEBUG=False \
    ALLOWED_HOSTS=localhost \
    uv run --no-sync python manage.py collectstatic --noinput

# Buat user non-root
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Migrasi database dan jalankan Gunicorn
CMD ["sh", "-c", "uv run --no-sync python manage.py migrate && exec uv run --no-sync gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
