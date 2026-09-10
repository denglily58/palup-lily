FROM python:3.12-slim

WORKDIR /app

# Install deps first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Copy seed data (needed by tools/catalog.py etc.)
# In prod, this becomes read-only reference data
COPY --from=..seed /app/seed || true

EXPOSE 8080

# Uvicorn with 1 worker (free tier VM has limited memory)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
