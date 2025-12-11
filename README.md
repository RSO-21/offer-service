# Offer Service

Offer Service manages discount offers created by partners in the FRI Food RSO project.

It exposes:

- **HTTP REST API** on port **8000**
- **gRPC CLIENT** that validates partners via the Partner Service
- **Prometheus `/metrics` endpoint**

---

## 🚀 Features

- Create, update, retrieve, list and delete offers
- Validates partner existence/active status via **gRPC call**
- PostgreSQL storage
- Docker-ready
- Observability via Prometheus metrics

---

## 📦 Project Structure
```
offer-service/
├─ app/
│ ├─ api/offers.py # Business logic & gRPC integration
│ ├─ grpc_generated/ # Generated protobuf client files
│ ├─ models.py
│ ├─ schemas.py
│ ├─ db.py
│ ├─ config.py
│ └─ main.py
├─ Dockerfile
├─ requirements.txt
└─ .env.example
```

---

## ⚙️ Environment Variables

Create `.env` file:

```env
PGHOST=your_postgres_host
PGUSER=your_postgres_user
PGPASSWORD=your_postgres_password
PGPORT=5432
PGDATABASE=offer_service

# gRPC connection to Partner Service
PARTNER_GRPC_HOST=partner-service
PARTNER_GRPC_PORT=50051
```
> Create the database once on your Postgres server, e.g. `CREATE DATABASE offer_service;`, and grant the `PGUSER` account rights to it. Repeat the pattern for other microservices so each one owns its own database.
---

## ▶️ Running Locally (without Docker)

### Start FastAPI HTTP server:
uvicorn app.main:app --reload --port 8001

### If running locally (not Docker), set:
PARTNER_GRPC_HOST=localhost

---

## 🐳 Running with Docker

### Build the container:
docker build -t offer-service .

### Run the container (HTTP + gRPC):
docker run --name offer-service --network fri-net --env-file .env -p 8001:8000 offer-service

---

## 🌐 Docker Network Requirement

For gRPC communication between microservices to work inside Docker, a shared Docker network is required.

Create the network once on your machine:

docker network create fri-net

Both partner-service and offer-service must run on this shared network:

docker run --network fri-net ...

---

## 🌉 gRPC Integration

# Offer Service validates partner via:
partner = get_partner_via_grpc(partner_id)

# The target is resolved from:
- PARTNER_GRPC_HOST=partner-service
- PARTNER_GRPC_PORT=50051

## 📡 HTTP API Documentation

### When running:
http://localhost:8001/docs

---

## 📊 Metrics

### Prometheus metrics available at:
 /metrics

---

## 🧪 Health Check

GET /health

