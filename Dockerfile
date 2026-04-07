FROM python:3.11-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
WORKDIR /app
RUN pip install --target=/packages --no-cache-dir -r requirements.txt
COPY . .

FROM gcr.io/distroless/python3-debian12:nonroot

COPY --from=builder /packages /usr/lib/python3.11/site-packages/
COPY --from=builder --chown=nonroot:nonroot /app /app

WORKDIR /app

ENV PYTHONPATH=/usr/lib/python3.11/site-packages

USER nonroot

EXPOSE 5000

CMD ["/usr/bin/python3.11", "run.py"]