---
id: computing-software.cloud-infrastructure-engineering.google-cloud.mig-autohealing-with-application-health-checks
name: mig-autohealing-with-application-health-checks
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, managed-instance-groups, mig-autohealing, autohealing-health-check, initial-delay, health-check-firewall]
level: practitioner
status: docs-checked
description: "Set up MIG autohealing: a dedicated application health check, initial delay sized to boot, firewall for probe ranges, and diagnosing recreate loops from health state."
sources: ["https://cloud.google.com/compute/docs/instance-groups/autohealing-instances-in-migs", "https://cloud.google.com/load-balancing/docs/health-check-concepts", "https://cloud.google.com/sdk/gcloud/reference/compute/instance-groups/managed/update"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MIG autohealing with application health checks

## Configure
```bash
gcloud compute health-checks create http app-autoheal --port=8080 --request-path=/healthz \
  --check-interval=10s --timeout=5s --healthy-threshold=2 --unhealthy-threshold=3
gcloud compute firewall-rules create allow-hc --network=<NET> --direction=INGRESS \
  --source-ranges=35.191.0.0/16,130.211.0.0/22 --allow=tcp:8080 --target-tags=app
gcloud compute instance-groups managed update app-mig --region=<R> \
  --health-check=app-autoheal --initial-delay=300
```
- Use a **separate, more lenient** health check for autohealing than for the LB: the LB should drain
  quickly, autohealing should only recreate truly broken VMs (unhealthy-threshold 3+ at 10s+).
- `/healthz` should check the process itself, not downstream dependencies; a DB outage must not
  recreate the whole fleet.
- `--initial-delay` (0 to 3600 s) makes the MIG ignore unsuccessful health checks while the VM boots and the app warms up. `gcloud compute health-checks create http` defaults are 5s interval, 5s timeout, healthy threshold 2 and unhealthy threshold 2.

## Observe
```bash
gcloud compute instance-groups managed list-instances app-mig --region=<R> \
  --format="table(instance.basename(),status,currentAction,instanceHealth[0].detailedHealthState)"
```
`detailedHealthState` values: `HEALTHY`, `UNHEALTHY`, `TIMEOUT`, `DRAINING`, `UNKNOWN`. Health state change logs are described on the autohealing page.

## Recreate-loop diagnosis
| Pattern | Cause |
|---|---|
| All instances `TIMEOUT` | firewall missing probe ranges, wrong port |
| Healthy then unhealthy at ~initial-delay | app needs longer warmup |
| One zone only | zonal dependency (disk, metadata) |

## Gotchas
- Health checks from `35.191.0.0/16` and `130.211.0.0/22` (and IPv6 `2600:2d00:1:b029::/64`).

## Verify
- [ ] Killing the app process on one VM leads to its recreation after threshold; others untouched.

## Checked

Checked 2026-10-27 against Set up an application health check and autohealing, the health check concepts page and the gcloud reference for instance-groups managed update and health-checks create http, plus the v1 API discovery document (detailedHealthState). Confirmed the probe ranges (35.191.0.0/16, 130.211.0.0/22, 2600:2d00:1:b029::/64), --initial-delay 0 to 3600, --health-check, the advice to use separate health checks, and the five health states. Removed the unconfirmed recreation event name, maxUnavailable and stateful-disk claims.

Method: documentation only; no commands were run.
