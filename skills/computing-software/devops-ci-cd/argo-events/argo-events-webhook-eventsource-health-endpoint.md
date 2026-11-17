---
id: computing-software.devops-ci-cd.argo-events.argo-events-webhook-eventsource-health-endpoint
name: argo-events-webhook-eventsource-health-endpoint
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, webhook, health-check, ingress, loadbalancer, probe]
level: practitioner
status: docs-checked
description: "Use the automatic /health endpoint on every port of webhook-type EventSources for load balancer and Ingress health checks."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/webhook-health-check.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events webhook eventsource health endpoint

For `webhook` EventSources and the extended webhook types (`github`, `gitlab`, `sns`, `slack`, StorageGRID and `stripe`), Argo Events adds an extra endpoint `:${port}/health` besides the endpoint in your spec. It exists for load balancers and Ingress controllers that require a health check path.

An HTTP GET to the health endpoint returns the text `OK` with status code 200.

Example: this EventSource gets four endpoints, `:12000/example1`, `:12000/health`, `:13000/example2` and `:13000/health`.

```yaml
spec:
  webhook:
    example:
      port: "12000"
      endpoint: /example1
      method: POST
    example-foo:
      port: "13000"
      endpoint: /example2
      method: POST
```

One `/health` endpoint is created per configured port, as the four endpoints above show.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/eventsources/webhook-health-check.md. Confirmed: extended webhook types, /health endpoint per port, OK with 200, four-endpoint example. Removed or changed: the invented 'practical use' paragraph (Ingress readiness annotation, interaction with auth). The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
