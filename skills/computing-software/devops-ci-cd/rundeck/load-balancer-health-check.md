---
id: computing-software.devops-ci-cd.rundeck.load-balancer-health-check
name: load-balancer-health-check
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, health-endpoint, load-balancer, cluster-health, least-privilege]
level: practitioner
status: docs-checked
description: "Point a load balancer health check at Rundeck's unauthenticated /health endpoint, or use a least-privilege API token against system executions status."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/cluster/loadbalancer/health-check.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The load balancer in front of Rundeck should have a health check (documented from 3.3.4).

Preferred, unauthenticated:

```
http://<host>:4440/health
```

This endpoint is enabled by default. The page points to the config file reference (load balancer health endpoint section) for disabling it.

Authenticated alternative, which the docs recommend against because it adds security exposure:

```
<host>:4440/api/32/system/executions/status?authtoken=<TOKEN_VALUE>
```

If you use it, apply least privilege: give the token only the access needed for that call, following the "API Token Authorization Roles" section of the authorization docs.

Verify per node:

```bash
curl -i http://node1.example.com:4440/health
```

Gotcha: the page's examples show `//api` with a double slash in some lines; use a single slash.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Load Balancer - Cluster Health Checks: health checks from 3.3.4, unauthenticated /health enabled by default and disableable via the config file reference, the authenticated api/32/system/executions/status alternative with least privilege advice, and the double slash in page examples. Nothing removed.

Method: documentation only; no commands were run.
