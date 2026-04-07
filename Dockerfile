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
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --prefix=/install -r requirements.txt

FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

USER nonroot

EXPOSE 5000

CMD ["/usr/bin/python", "run.py"]
