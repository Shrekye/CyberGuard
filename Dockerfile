FROM python:3.11-slim AS builder

WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*
        
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app

COPY --from=builder /install /usr/local

COPY --chown=nonroot:nonroot . .

USER nonroot

EXPOSE 5000

CMD ["python", "/app/run.py"]