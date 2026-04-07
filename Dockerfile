FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app
COPY --from=builder /app /app
EXPOSE 5000

CMD ["run.py"]