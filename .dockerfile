FROM python:3-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
ADD build/dist/scih*.whl /app
RUN uv pip install --system /app/scih*.whl
ENTRYPOINT ["scih"]
