FROM python:3.11-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /install/
WORKDIR /install
RUN pip install --target=. --no-cache-dir -r requirements.txt

COPY . /app

FROM gcr.io/distroless/python3-debian12:nonroot

COPY --from=builder /install /usr/local/lib/python3.11/site-packages/
COPY --from=builder /app /app

WORKDIR /app

ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

USER nonroot

EXPOSE 5000

CMD ["/usr/bin/python3.11", "run.py"]