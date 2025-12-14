FROM python:3.12-slim

WORKDIR /app
RUN useradd -m appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Build metadata (set at build time by CI)
ARG GIT_SHA=local
ARG BUILD_TIME=local
ARG IMAGE_TAG=local
ENV GIT_SHA=$GIT_SHA
ENV BUILD_TIME=$BUILD_TIME
ENV IMAGE_TAG=$IMAGE_TAG

ENV PYTHONUNBUFFERED=1
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
