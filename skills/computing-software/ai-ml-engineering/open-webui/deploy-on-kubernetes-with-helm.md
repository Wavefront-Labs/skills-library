---
id: computing-software.ai-ml-engineering.open-webui.deploy-on-kubernetes-with-helm
name: deploy-on-kubernetes-with-helm
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [helm-kubernetes, kubernetes, helm, postgresql, redis, ingress, upgrades]
level: advanced
status: docs-checked
description: "Deploy Open WebUI on Kubernetes with the official Helm chart as a single replica or a production setup with PostgreSQL, Redis and S3, including safe updates."
sources:
  - https://docs.openwebui.com/getting-started/deployment/kubernetes
  - https://docs.openwebui.com/getting-started/quick-start/tab-kubernetes/Helm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: install Open WebUI with the Helm chart (the guide pins chart 17.5.0 and app v0.13.0; chart and app versions are separate).

## Quick try (not production)
```bash
helm repo add open-webui https://open-webui.github.io/helm-charts
helm repo update
helm install openwebui open-webui/open-webui
kubectl port-forward service/openwebui-open-webui 3000:80
```
Defaults also deploy Ollama, Pipelines and Redis and a 2 GiB PVC; add `--set ollama.enabled=false --set pipelines.enabled=false` if models live elsewhere. `helm uninstall openwebui` with defaults deletes the PVC and data.

## Real install, steps
1. `kubectl create namespace openwebui`; create a secret from a private `secrets.env` (chmod 600) holding `WEBUI_SECRET_KEY` (from `openssl rand -hex 32`) and `OPENAI_API_KEY`: `kubectl -n openwebui create secret generic openwebui-secrets --from-env-file=secrets.env`.
2. `values-common.yaml`: `fullnameOverride: openwebui`, `workload.kind: Deployment`, `strategy.type: Recreate`, image `ghcr.io/open-webui/open-webui` tag `v0.13.0`, `ollama/pipelines/terminals/tika` disabled, service ClusterIP port 80, `openaiBaseApiUrl`, `openaiApiKeyExistingSecret: openwebui-secrets` with key `OPENAI_API_KEY`, resources (500m/1Gi requests, 2 CPU/4Gi limits), probes: startup `/health` (period 10, failureThreshold 60), readiness `/ready`, liveness `/health`; `extraEnvVars` with `WEBUI_SECRET_KEY` from the secret and `UVICORN_WORKERS: '1'`. `/ready` answers once startup finishes and DB/Redis respond.
3. Pick a profile.
   - Single replica: `replicaCount: 1`, `persistence` provider local, ReadWriteOnce, 10Gi, annotation `helm.sh/resource-policy: keep`, `ENABLE_DB_MIGRATIONS: 'true'`. PVC mounts at `/app/backend/data`. Use block/local storage; never put SQLite on NFS or SMB.
   - Production: pre-provision PostgreSQL with the `vector` extension, Redis, S3 bucket, an embedding API, Apache Tika, ingress with TLS. `backends.env` holds `DATABASE_URL`, `REDIS_URL` (`rediss://...`), `RAG_OPENAI_API_KEY`, `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY` (URL-encode special characters). Values: `replicaCount: 3`, `websocket.manager: redis`, `persistence.provider: s3`, ingress host/TLS, and env `WEBUI_URL`, `DATABASE_URL`, `VECTOR_DB: pgvector`, `PGVECTOR_CREATE_EXTENSION: 'false'`, `RAG_EMBEDDING_ENGINE: openai`, `RAG_EMBEDDING_MODEL`, `RAG_OPENAI_API_BASE_URL`, `CONTENT_EXTRACTION_ENGINE: tika`, `TIKA_SERVER_URL`, `ENABLE_DB_MIGRATIONS: 'false'`. Setting a Postgres URL does not migrate existing SQLite data.
4. First install with exactly one migration-enabled worker and ingress off:
```bash
helm install openwebui open-webui/open-webui --version 17.5.0 --namespace openwebui \
  -f values-common.yaml -f "$OPENWEBUI_PROFILE" \
  --set replicaCount=1 --set ingress.enabled=false \
  --set-string extraEnvVars.ENABLE_DB_MIGRATIONS=true --wait --timeout 15m
```
(render first with `helm template`). Verify via `kubectl -n openwebui port-forward service/openwebui 3000:80`, create the admin account, send a chat.
5. Production only: `helm upgrade ... -f values-common.yaml -f values-production.yaml --wait` to set replicas, ingress and disable migrations.

## Ingress
Needs WebSocket support, no response buffering, adequate timeouts and upload size. NGINX Ingress cookie affinity annotations: `nginx.ingress.kubernetes.io/affinity: 'cookie'`, `session-cookie-name: 'open-webui-session'`, expires/max-age `'172800'`. Affinity is required only with `ENABLE_WEBSOCKET_SUPPORT=false` and does not replace Redis.

## Updates (maintenance window)
Scale deployment to 0 and wait for pods to delete, take a final backup (PVC, or Postgres plus object storage), bump the tag, `helm upgrade` with one replica and migrations on, check logs, then (production) run the finish upgrade. Helm rollback (even `--atomic`) cannot undo DB migrations. Remove any HPA before updates.

## Uninstall
`helm uninstall openwebui -n openwebui`; the single-replica PVC is kept by the annotation (reuse with `persistence.existingClaim: openwebui` and the same signing key). Deleting the namespace deletes Secrets and PVCs.

## Gotchas
- Slim image works for the production profile: `image.tag: v0.13.0-slim`.
- Many settings persist after first start, so later env changes may not override them.
- Existing Secret/key names must match exactly, in the same namespace.

## Checked
2026-11-04. Confirmed against the Open WebUI docs pages getting-started/deployment/kubernetes and getting-started/quick-start/tab-kubernetes/Helm (both read in full): pinned chart 17.5.0 and app v0.13.0, quick-try commands and defaults (Ollama, Pipelines, Redis, 2 GiB PVC), secret creation, values-common keys and probe paths, single-replica and production profiles and their env vars, the one-worker bootstrap install, ingress affinity annotations, the update procedure, helm rollback limits, uninstall and PVC keep annotation, and slim image tag. Nothing removed.
Method: documentation only; no commands were run.
