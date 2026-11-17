---
id: computing-software.web-development.fastify.container-deploy-cloud-run-vercel
name: container-deploy-cloud-run-vercel
category: computing-software
field: web-development
product: fastify
tags: [fastify, deployment, docker, cloud-run, kubernetes]
level: practitioner
status: docs-checked
description: "Deploy Fastify in containers: listen on 0.0.0.0 and the platform PORT, set trustProxy, and probe readiness correctly."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Serverless.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Recommendations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cloud Run is a serverless container environment, so Fastify needs little change beyond the address and port:

```js
const fastify = Fastify({ trustProxy: true })
const IS_GOOGLE_CLOUD_RUN = process.env.K_SERVICE !== undefined
const port = process.env.PORT || 3000
const host = IS_GOOGLE_CLOUD_RUN ? '0.0.0.0' : undefined
await fastify.listen({ port, host })
```

A basic Dockerfile: `FROM node:lts`, `WORKDIR /usr/src/app`, `COPY package*.json ./`, `RUN npm i --production`, `COPY . .`, `CMD [ "npm", "start" ]`, with a `.dockerignore` of Dockerfile, README.md, node_modules, npm-debug.log. Build with `gcloud builds submit --tag gcr.io/PROJECT-ID/APP-NAME`, then `gcloud beta run deploy --image gcr.io/PROJECT-ID/APP-NAME --platform managed`.

Kubernetes readiness probe: the probe uses the pod IP by default and Fastify listens on 127.0.0.1, so it cannot connect. Listen on `0.0.0.0` or set a custom host in `readinessProbe.httpGet`:

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 4000
  initialDelaySeconds: 30
  periodSeconds: 30
  timeoutSeconds: 3
  successThreshold: 1
  failureThreshold: 5
```

Vercel supports Fastify and, with Fluid compute (explicit opt-in), combines server-like concurrency with autoscaling.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Serverless.md, Recommendations.md) and confirmed. Removed or corrected: a trustProxy gotcha the pages do not state; the invented Verify step.

Method: documentation only; no commands were run.
