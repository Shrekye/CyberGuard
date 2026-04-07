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

COPY requirements.txt .
RUN $VENV/bin/pip install --upgrade pip && \
    $VENV/bin/pip install --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3-debian12:nonroot

ENV VENV=/opt/venv

WORKDIR /app

COPY --from=builder $VENV $VENV

COPY --chown=nonroot:nonroot . .

ENV PATH="$VENV/bin:$PATH"

USER nonroot

EXPOSE 5000

ENTRYPOINT ["python", "run.py"]