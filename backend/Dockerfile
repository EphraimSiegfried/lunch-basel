FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ADD . /app
WORKDIR /app
RUN uv sync --locked
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8218", "lunchb.main:app"]
