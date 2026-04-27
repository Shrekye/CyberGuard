FROM python:3.11-slim AS builder

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel

RUN openssl version

COPY requirements.txt .
RUN pip install --target=/packages --no-cache-dir -r requirements.txt
COPY . /app

FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app

COPY --from=builder /packages /usr/lib/python3.11/site-packages/

COPY --from=builder /usr/bin/openssl /usr/bin/openssl
COPY --from=builder /usr/lib/ssl /usr/lib/ssl
COPY --from=builder /usr/include/openssl /usr/include/openssl

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PYTHONPATH=/usr/lib/python3.11/site-packages

USER nonroot
EXPOSE 5000

ENTRYPOINT ["python", "/app/run.py"]