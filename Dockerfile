FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --target=/install --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app
COPY --from=builder /install /usr/lib/python3.11/site-packages/
COPY --chown=nonroot:nonroot . .

USER nonroot
EXPOSE 5000

CMD ["/usr/bin/python", "/app/run.py"]