---
id: computing-software.ai-ml-engineering.mastra.split-workers-deployment
name: split-workers-deployment
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, deploy, workers, orchestration, scheduler, pubsub, docker, kubernetes]
level: sme
status: docs-checked
description: "Split Mastra into API, orchestration, scheduler and background-task worker processes using MASTRA_WORKERS, a distributed PubSub, Docker Compose or Kubernetes."
sources:
  - https://mastra.ai/docs/deployment/workers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run workflow orchestration, cron scheduling and background tool calls in dedicated worker processes. The page marks this beta: breaking changes may occur without a major bump. Skip it for light traffic; the default in-process setup (in-memory PubSub, workers started by the `mastra build` server, or `mastra.startWorkers()` after your adapter server listens) needs no extra infrastructure but does not survive crashes or scale per component.

## Worker types
- Orchestration: subscribes to workflow events on PubSub and runs step transitions. In a split deployment it pulls from PubSub and delegates step execution to the API over HTTP. Needs a pull-capable PubSub: `RedisStreamsPubSub`, `ValkeyStreamsPubSub` or `GoogleCloudPubSub`.
- Scheduler: polls storage for due cron schedules and publishes `workflow.start`; reads declarative `schedule` fields from workflows. With no schedules at boot, one `listSchedules()` check and no polling (can scale to zero). Runtime-created schedules publish a wake event on PubSub (processes must share it). Force polling with `scheduler: { enabled: true }` or `MASTRA_WORKERS=scheduler`. Run exactly one, or schedules fire duplicates. Split: scheduled workflows run on the evented engine; in-process: default engine.
- Background task: executes tools marked `background: { enabled: true }`; manages concurrency, lifecycle and result delivery over PubSub.

## Configure
```typescript
export const mastra = new Mastra({
  storage: new PostgresStore({ connectionString: process.env.DATABASE_URL! }),
  pubsub: new RedisStreamsPubSub({ url: process.env.REDIS_URL! }),
})
```
(GCP variant: `GoogleCloudPubSub({ projectId })` with `LibSQLStore`.) Needs a distributed PubSub, shared storage and network connectivity between orchestration worker and API.

## Select workers with `MASTRA_WORKERS`
`false` (none; use on the API in a fully split deployment), `orchestration`, `scheduler`, `backgroundTasks`, or a comma list such as `orchestration,backgroundTasks`. CLI: `mastra worker start orchestration` (sets the variable; without a name it does not). Set it on every process including `false` on the API: any value moves workflows with `schedule` to the evented engine, and all processes must use the same engine.

## Network
Only the API is public. Workers listen on `PORT` (default 4111) for internal `/health` and `/config`; keep it private. The orchestration worker calls the API at `MASTRA_STEP_EXECUTION_URL` (include `/api`, e.g. `http://api:4111/api`); without it the worker tries to run steps itself without the full runtime. If the API has an auth provider, set `MASTRA_WORKER_AUTH_TOKEN` (sent as `Authorization: Bearer`) to a token the provider accepts.

## Build
```bash
mastra build
mastra worker build --output-dir .mastra/worker
```
API artifact `.mastra/output/`, worker artifact `.mastra/worker/`. One Dockerfile takes either via `ARG MASTRA_OUTPUT=.mastra/output`: `FROM node:22-alpine`, copy `package.json` and `.npmrc*`, `npm install --omit=dev`, copy the directory, `EXPOSE 4111`, `CMD ["node", "index.mjs"]`.

## Docker Compose shape
Services: `postgres:16-alpine`, `redis:7-alpine` (with healthchecks), `api` (build arg `.mastra/output`, port `4111:4111`, `MASTRA_WORKERS: 'false'`, `WORKER_TOKEN`), and three worker services built with `MASTRA_OUTPUT: .mastra/worker`: `orchestration-worker` (`MASTRA_WORKERS: orchestration`, `MASTRA_STEP_EXECUTION_URL: http://api:4111/api`, `MASTRA_WORKER_AUTH_TOKEN: ${WORKER_TOKEN}`), `scheduler-worker` (`scheduler`), `background-task-worker` (`backgroundTasks`). Shared env: `DATABASE_URL`, `REDIS_URL`. Put `POSTGRES_PASSWORD` and `WORKER_TOKEN` in `.env`; configure the API auth provider to accept `WORKER_TOKEN`. Only the orchestration worker needs the token. Verify: `docker compose up -d`, `docker compose ps`, `curl http://localhost:4111/api/agents`.

## Kubernetes
One Deployment each for API, orchestration, scheduler, background tasks; same image and Secret (`envFrom: secretRef`), role-specific `MASTRA_WORKERS` env; API gets `MASTRA_WORKERS: 'false'` and a Service. A `mastra-projects` Helm chart renders these. Verify with `kubectl apply -f k8s/`, `kubectl get pods`, `kubectl port-forward svc/api 4111:4111`, `curl http://localhost:4111/api/agents`.

## Scaling and health
Orchestration and background-task workers scale horizontally (PubSub consumer groups): `docker compose up -d --scale orchestration-worker=3`, `kubectl scale deployment/orchestration-worker --replicas=3`. Scheduler: exactly one. Worker artifacts expose `GET /health` on `PORT`: `503` while `startWorkers()` initializes, `200` once all selected workers started; use a startup probe or initial delay if used for liveness.

## Crash recovery and limits
Distributed PubSub redelivers unacknowledged events (and failed step requests), so make handlers idempotent. The scheduler recomputes next fire from restart time and does not replay missed schedules. If the API crashes mid-step the run can stay `running` with no automatic retry; for durable agents set `recovery.durableAgents: 'auto'`. No dead-letter queue; scheduler is single-instance.

## Checked
Method: 2026-11-08 read the Mastra Workers deployment docs page in full (served as markdown). Worker types, MASTRA_WORKERS values, network rules, build/Docker/Compose/Kubernetes shapes, scaling, health and crash-recovery limits all match the page; its verify commands are the page's own. No content changed.
