# Nanobot Gateway Dockerfile
FROM harbor.pg.innopolis.university/docker-hub-cache/astral/uv:python3.14-bookworm-slim

WORKDIR /app

# Copy entire project
COPY . .

# Sync all dependencies
RUN uv sync --frozen

# Run via uv
CMD ["uv", "run", "python", "/app/nanobot/entrypoint.py"]
