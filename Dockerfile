FROM python:3.11-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app
COPY --from=builder /app /app

EXPOSE 5000

CMD ["run.py"]