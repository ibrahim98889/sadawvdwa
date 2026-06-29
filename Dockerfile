# Build Stage
FROM rust:1.75-slim-bookworm as builder
RUN apt-get update && apt-get install -y pkg-config libssl-dev git g++
WORKDIR /app
RUN git clone https://github.com/reacherhq/check-if-email-exists.git .
RUN cargo build --release

# Runtime Stage
FROM python:3.11-slim-bookworm
RUN apt-get update && apt-get install -y libssl3 ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# Copy Reacher binary
COPY --from=builder /app/target/release/check-if-email-exists-cli /usr/local/bin/reacher-cli
RUN chmod +x /usr/local/bin/reacher-cli

# Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Copy API code
COPY main.py .

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
