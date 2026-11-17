---
id: computing-software.cloud-infrastructure-engineering.knative.traffic-management
name: traffic-management
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [traffic-management, traffic-split, revision-tag, latest-revision, percent]
level: practitioner
status: docs-checked
description: "Split traffic across revisions and tag revisions for direct URLs."
sources:
  - https://knative.dev/docs/serving/traffic-management/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: route portions of traffic to specific Revisions and give revisions their own addresses.

A new Knative Service has no default `traffic` spec. Setting `traffic` lets you split traffic over any number of fixed Revisions, or send it to the newest Revision with `latestRevision: true`.

```yaml
spec:
  traffic:
  - percent: 0
    revisionName: example-service-1
    tag: staging
  - percent: 40
    revisionName: example-service-2
  - percent: 60
    revisionName: example-service-3
```

Tags: a `tag` on a traffic target creates an address for it. The target above is reachable at `staging-<route name>.<namespace>.<domain>`, while untagged targets are reachable only through the main route `<route name>.<namespace>.<domain>`. A tagged target also gets its own Kubernetes Service named `staging-<route name>` in the same namespace, so other in-cluster Services can call it.

Examples from the page:
- `latestRevision: true` with `percent: 100` sends everything to the newest Revision; `status.traffic` shows the Revision name it resolved to.
- Pinning `revisionName: example-service-1` with tag `current` at 100%, plus a `latest` tagged target with `latestRevision: true` and 0%, keeps the latest ready Revision available even though no traffic is routed to it.
- Splitting 50/50 between `current` (example-service-1) and `candidate` (example-service-2), with a 0% `latest` target, is the same pattern extended to two live Revisions.

With the `kn` CLI: `kn service update <service-name> --traffic <revision-name>=<percent>` (repeat `--traffic` per target), `--tag <revision>=<tag>` to tag a Revision, and `@latest` to mean the latest Revision, for example `--traffic @latest=80 --traffic v1=20`.

Blue/green with a Route: send 100% to the first Revision, add the second Revision at `percent: 0` with a `tag` (for example `v2`) so it gets its own test URL (read it with `kubectl get route <route-name> --output jsonpath="{.status.traffic[*].url}"`), then move to 50/50 and finally 100% on the new Revision. If you will not roll back, you can delete the old Revision instead of leaving it at 0%; non-routeable Revisions are garbage-collected.

## Checked

Method: docs-checked 2026-11-09 against https://knative.dev/docs/serving/traffic-management/ (read in full). Dropped the earlier unsourced claim that percentages must add up to 100.
