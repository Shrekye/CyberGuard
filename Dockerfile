FROM python:3.11-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY requirements.txt .

RUN pip install \
    --target=/install \
    --no-cache-dir \
    --no-compile \
    -r requirements.txt

COPY . /app-src

RUN find /app-src -name "*.pyc" -delete && \
    find /app-src -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

FROM gcr.io/distroless/python3-debian12:nonroot

COPY --from=builder /install /usr/lib/python3.11/site-packages/

COPY --from=builder --chown=nonroot:nonroot /app-src /app

WORKDIR /app

ENV PYTHONPATH=/usr/lib/python3.11/site-packages
ENV PYTHONUNBUFFERED=1

USER nonroot

EXPOSE 5000

CMD ["/usr/bin/python3.11", "/app/run.py"]