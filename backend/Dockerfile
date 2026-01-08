FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy the rest of the code
COPY . .

# Expose port
EXPOSE 8000

# Run the server
CMD ["uv", "run", "uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]