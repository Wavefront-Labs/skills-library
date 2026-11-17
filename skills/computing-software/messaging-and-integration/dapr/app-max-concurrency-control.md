---
id: computing-software.messaging-and-integration.dapr.app-max-concurrency-control
name: app-max-concurrency-control
category: computing-software
field: messaging-and-integration
product: dapr
tags: [concurrency, app-max-concurrency, rate-limit, annotations, dapr-run, pubsub, ratelimit-middleware]
level: practitioner
status: docs-checked
description: "Cap concurrent requests and events from the Dapr sidecar to your app with app-max-concurrency (default -1), via dapr run or annotation, versus ratelimit middleware."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/configuration/control-concurrency.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dapr can act as the semaphore so the app needs no code for it. `app-max-concurrency` limits how many requests and events invoke the app at the same time; the default is `-1`, meaning no limit.

Local development:

```bash
dapr run --app-max-concurrency 1 --app-port 5000 python ./app.py
```

A value of 1, as the page notes, effectively turns the app into a sequential processing service.

Kubernetes, in the pod template annotations:

```yaml
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "nodesubscriber"
        dapr.io/app-port: "3000"
        dapr.io/app-max-concurrency: "1"
```

Difference from rate limiting: `middleware.http.ratelimit` is time bound (requests per second), while `app-max-concurrency` bounds simultaneous in-flight requests and events at any moment.

Limitation: the limit is guaranteed for every event coming from Dapr to your app (pub/sub events, direct invocation from other services, binding events). Dapr cannot enforce it on requests that reach your app directly without going through the sidecar.

## Checked

2026-11-04. Flag, annotation, default and limitation confirmed on the control concurrency and rate limit page.

Method: documentation only; no commands were run.
