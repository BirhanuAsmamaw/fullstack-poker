# Use the official slim Python 3.13 base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Tell Poetry not to create a virtualenv,
# so that packages go into the global site-packages
RUN poetry config virtualenvs.create false

# Copy only pyproject.toml and poetry.lock first,
# to install dependencies in a cacheable layer
COPY pyproject.toml poetry.lock ./

# Install all dependencies (including uvicorn & fastapi)
RUN poetry install --no-interaction --no-ansi

# Now copy your application code
COPY src/ ./src/
COPY main.py ./

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the app with Uvicorn and enable auto-reload for development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]