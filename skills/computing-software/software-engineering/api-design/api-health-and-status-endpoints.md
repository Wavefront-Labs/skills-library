---
id: computing-software.software-engineering.api-design.api-health-and-status-endpoints
name: api-health-and-status-endpoints
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-health-endpoint, api-sla, status-page, health-checks, liveness-readiness]
level: practitioner
status: verified
description: "Expose health endpoints for infrastructure and API consumers, publish an SLA and status page, and keep internal checks separate from public ones."
sources: ["https://datatracker.ietf.org/doc/html/draft-inadarei-api-health-check", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/", "https://sre.google/sre-book/service-level-objectives/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Health and status endpoints for API consumers

## Three audiences, three endpoints
The `/livez` and `/readyz` names come from the Kubernetes API server, which documents `/livez` (restart decision) and `/readyz` (route traffic away) and deprecated `/healthz` since v1.16; use them as a naming convention for your own services.
| Endpoint | For | Checks | Auth |
|---|---|---|---|
| `/livez` | orchestrator restart decision | process responsive only, no dependencies | internal |
| `/readyz` | load balancer routing | can serve: DB pool, required config, warm caches | internal |
| `/health` (public) or status page | API consumers | aggregated component status | public, cached |

Liveness that checks the database restarts every pod when the DB blips: keep it dependency-free.

## Response format (draft-inadarei-api-health-check)
Note: this is an expired, archived Internet-Draft (version 06, expired 19 April 2022) with no IETF standing; treat it as a convention.
```json
Content-Type: application/health+json
{"status":"pass","version":"2","releaseId":"2026.10.18-1",
 "checks":{"postgres:responseTime":[{"status":"pass","observedValue":4,"observedUnit":"ms"}]}}
```
`status`: `pass` / `warn` / `fail` (case-insensitive). The draft requires 2xx-3xx for pass, 4xx-5xx for fail, and 2xx-3xx for warn with additional information; 200 and 503 are sensible choices. `checks` keys are `componentName:measurementName`, mapping to arrays; `observedUnit` should accompany `observedValue`. The draft itself warns that health details can help attackers and may need authentication: don't expose hostnames, dependency versions or error strings publicly.

## SLA and status page
- Publish an SLA for GA surfaces: availability target (e.g. 99.9% monthly, illustrative), how it's measured
  (server-side 5xx and timeouts over valid requests), exclusions, and credits.
- Run internal SLOs tighter than the SLA so you have warning.
- Status page (Statuspage, Instatus, self-hosted) per component and region, with incident history
  and RSS/webhook subscriptions. Update it from incident tooling, not by hand at 3am.
- Synthetic checks from outside your network hit real public endpoints with a test key.

## Gotchas
Health endpoints must be cheap and rate-limited, excluded from auth middleware that itself depends
on the DB, and not counted in latency SLOs.
