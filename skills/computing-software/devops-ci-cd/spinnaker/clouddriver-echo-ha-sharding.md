---
id: computing-software.devops-ci-cd.spinnaker.clouddriver-echo-ha-sharding
name: clouddriver-echo-ha-sharding
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [high-availability, clouddriver, echo, halyard, hal-config-deploy-ha, kubernetes, redis-replica]
level: advanced
status: docs-checked
description: "Split Clouddriver into caching, rw, ro and ro-deck services with hal config deploy ha clouddriver enable, and understand the Kubernetes-only distributed requirement."
sources:
  - https://spinnaker.io/docs/reference/halyard/high-availability/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page is headed "Halyard is deprecated" (kept for historical purposes; the majority of the relevant information has moved to the high-availability documentation). Beyond plain horizontal scaling, Halyard can split a service into separate logical roles so each can be configured and scaled independently. This was inspired by Netflix's large-scale experience. It currently applies only to **Clouddriver and Echo**, and only for a **distributed Spinnaker deployment on the Kubernetes provider**.

**HA Clouddriver.**

```bash
hal config deploy ha clouddriver enable
```

Spinnaker is then deployed with Clouddriver as four services, each doing a subset of the work:
- `clouddriver-caching`
- `clouddriver-rw`
- `clouddriver-ro`
- `clouddriver-ro-deck`

By default all four use the global Redis, but the recommended layout is an external Redis: `clouddriver-ro` against a read replica, `clouddriver-ro-deck` against a different read replica, and the other two against the master. Halyard does this automatically if you give it the endpoints (valid Redis URIs):

```bash
hal config deploy ha clouddriver edit --redis-master-endpoint $REDIS_MASTER_ENDPOINT --redis-slave-endpoint $REDIS_SLAVE_ENDPOINT --redis-slave-deck-endpoint $REDIS_SLAVE_DECK_ENDPOINT
```

Roles: `clouddriver-caching` caches and retrieves cloud infrastructure data and talks to no other Spinnaker service; `clouddriver-rw` handles all other mutating operations; `clouddriver-ro` handles read requests; `clouddriver-ro-deck` handles reads from Deck through Gate. The rw, ro and ro-deck services can be scaled. For sizing use `spin-<name>` (for example `spin-clouddriver-rw`); for custom profiles or service settings use the bare name.

**HA Echo.** `hal config deploy ha echo enable` splits Echo into `echo-scheduler` (cron-style scheduled tasks; must run exactly one pod to avoid duplicate triggering) and `echo-worker` (everything else; can scale beyond one pod). Only echo-worker scales horizontally, but splitting reduces load on both.

**Orphans.** Halyard does not clean up the old non-HA services when HA is toggled on a running Spinnaker; add `--delete-orphaned-services` to `hal deploy apply`.

**Recoverability.** With an external Redis, Igor polls the state store and recreates state; its `pollingSafeguard.itemUpperThreshold` caps the number of pipeline triggers accepted so a recovery does not re-trigger many old pipelines. The page advises against spot or preemptible nodes in production and suggests spreading services across availability zones.

Because the new logical services have new names, they can be configured and scaled independently.

## Checked

2026-11-04. Scope limits, the enable command, the four Clouddriver services and the Redis replica layout were confirmed on the High Availability page. The edit command flags, per-service roles, Echo split, orphan cleanup and recoverability notes were confirmed on the same page. Removed: the monitoring and firewall advice (not on the page).

Method: documentation only; no commands were run.
