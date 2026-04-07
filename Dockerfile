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

FROM gcr.io/distroless/python3-debian12:nonroot

COPY --from=builder /packages /usr/lib/python3.11/site-packages/

COPY --chown=nonroot:nonroot . /app

WORKDIR /app

ENV PYTHONPATH=/usr/lib/python3.11/site-packages
ENV PYTHONUNBUFFERED=1

USER nonroot

EXPOSE 5000

CMD ["python3", "run.py"]