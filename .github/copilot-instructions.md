# Copilot Instructions for devops-project

## Project Overview
This repository is a containerized FastAPI application with Postgres, Uvicorn, and Traefik, supporting both development and production deployments. Infrastructure is managed via Docker Compose and Helm charts, with Kubernetes manifests for cloud-native orchestration.

## Architecture
- **FastAPI app**: Located in `app/`, main entrypoint is `main.py`. Configuration in `config.py`.
- **Database**: Postgres, exposed via Helm service templates (see `helm/fastapi/templates/db-service.yaml`).
- **Reverse Proxy**: Traefik, configured for both dev and prod (`traefik.dev.toml`, `traefik.prod.toml`).
- **Containerization**: Multiple Dockerfiles for different environments (`Dockerfile`, `Dockerfile.prod`, `Dockerfile.aws`, `Dockerfile.traefik`).
- **Orchestration**: Use `docker-compose.yml` for local/dev, `docker-compose.prod.yml` for production. Helm charts in `helm/fastapi/` and `helm-aws/fastapi/` for Kubernetes.

## Developer Workflows
- **Build & Run (Dev)**:
  ```sh
  docker-compose up -d --build
  ```
- **Build & Run (Prod)**:
  ```sh
  docker-compose -f docker-compose.prod.yml up -d --build
  ```
- **Kubernetes Deploy**:
  - Helm charts: `helm install fastapi ./helm/fastapi -f ./helm/fastapi/values-dev.yaml`
  - AWS: Use `helm-aws/fastapi/` and `values-prod.yaml`
- **Testing**:
  - Tests in `tests/` (e.g., `test_root.py`).
  - Run with `pytest` from project root.

## Patterns & Conventions
- **Helm templates** use Go templating (`{{ ... }}`) for dynamic values.
- **Service naming**: Database service is always named `db` for internal references.
- **Environment separation**: Use distinct Dockerfiles and Helm values files for dev/prod/cloud.
- **Secrets**: Managed via Helm templates (`secret-db.yaml`).
- **Traefik**: All ingress is routed through Traefik; update domain/email in `traefik.prod.toml` for production.

## Integration Points
- **External DB**: Postgres connection details are templated via Helm values.
- **Reverse Proxy**: Traefik configures HTTPS and routing for FastAPI.
- **Cloud**: For AWS, use `Dockerfile.aws` and `helm-aws/fastapi/`.

## Key Files & Directories
- `app/`: FastAPI source code
- `Dockerfile*`: Container build instructions
- `docker-compose*.yml`: Compose configs
- `helm/fastapi/`: Helm chart for Kubernetes
- `helm-aws/fastapi/`: Helm chart for AWS
- `traefik.*.toml`: Traefik configs
- `tests/`: Pytest tests

## Example: Adding a New Service
1. Create a new FastAPI route in `app/main.py`.
2. Add any required DB tables in `app/db.py`.
3. Update Helm templates if new service exposure is needed.
4. Rebuild containers and redeploy.

---
For questions about build, deployment, or architecture, see the README or relevant Helm chart templates.
