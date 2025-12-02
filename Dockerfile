FROM python:3.11-slim

WORKDIR /app

# 1) Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy source code
COPY app/ ./app/

# 3) Run FastAPI with uvicorn on port 8000 inside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]