# Use the official Rust image as a builder
FROM rust:1.75-slim as builder

# Install dependencies for building
RUN apt-get update && apt-get install -y pkg-config libssl-dev git

# Set working directory
WORKDIR /app

# Clone the repository
RUN git clone https://github.com/reacherhq/check-if-email-exists.git .

# Build the project in release mode
RUN cargo build --release

# Use a tiny runtime image
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y libssl3 ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the built binary from the builder stage
COPY --from=builder /app/target/release/check-if-email-exists-cli /usr/local/bin/reacher-cli

# Copy your Python API code
COPY main.py .

# Install Python for the FastAPI wrapper
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install fastapi uvicorn --break-system-packages

# Expose the port Railway expects
EXPOSE 8080

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
