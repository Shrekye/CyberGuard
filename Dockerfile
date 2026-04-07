FROM python:3.11-slim AS builder

ENV VENV=/opt/venv
RUN python -m venv $VENV

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*

ENV PATH="$VENV/bin:$PATH"
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

COPY --chown=nonroot:nonroot . .

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/opt/venv/lib/python3.11/site-packages"

USER nonroot

EXPOSE 5000

ENTRYPOINT ["python", "run.py"]