---
id: computing-software.cloud-infrastructure-engineering.linkerd.proxy-graceful-shutdown
name: proxy-graceful-shutdown
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, graceful-shutdown, prestop, proxy, annotations]
level: advanced
status: docs-checked
description: "Delay and bound proxy shutdown with wait-before-exit-seconds and shutdown-grace-period so in-flight and late requests complete."
sources:
  - https://linkerd.io/2.19/tasks/graceful-shutdown/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When a pod is deleted, Kubernetes sends TERM to each container. The Linkerd proxy then refuses new requests and lets existing ones finish. If the application makes new network calls after the proxy has received TERM, those calls fail. Clients that have not yet seen the endpoint removal can also hit a terminating pod.

Linkerd gives you these options:

- `--wait-before-exit-seconds` on `linkerd inject` (and the equivalent configuration annotation) adds a `preStop` hook to the proxy container that delays its handling of TERM. This gives slow clients time to receive the endpoints update.
- `config.linkerd.io/shutdown-grace-period` on a workload sets how long the proxy may take to shut down. When it elapses the proxy forcibly closes open connections. The default is 120 seconds.

For the best effect give the application container its own `preStop` hook with a sleep shorter than the proxy's delay, and keep both under the pod's `terminationGracePeriodSeconds`:

```yaml
# application container
lifecycle:
  preStop:
    exec:
      command: ["/bin/bash", "-c", "sleep 20"]
```

Kubernetes waits 30 seconds by default before sending KILL. The grace period starts when the preStop hook runs, not when the container begins processing TERM.

Tune the numbers together: proxy delay greater than the app's sleep, both less than `terminationGracePeriodSeconds`.

## Checked

2026-11-08. Read in full against the Linkerd 2.19 docs source (markdown in linkerd/website) of https://linkerd.io/2.19/tasks/graceful-shutdown/. Confirmed the TERM behaviour, wait-before-exit and shutdown-grace-period options, preStop sleep example and 30 second default stated above. Nothing was removed.

Method: documentation only; no commands were run.
