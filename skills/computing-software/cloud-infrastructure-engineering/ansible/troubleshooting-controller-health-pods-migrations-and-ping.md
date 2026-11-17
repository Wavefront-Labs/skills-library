---
id: computing-software.cloud-infrastructure-engineering.ansible.troubleshooting-controller-health-pods-migrations-and-ping
name: troubleshooting-controller-health-pods-migrations-and-ping
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, controller-install, awx-pod-troubleshooting, api-ping, awx-operator]
level: practitioner
status: draft
description: "Diagnose AWX and controller health: /api/v2/ping, operator and pod logs, stuck migrations, task vs web containers, and pending jobs with no capacity."
sources: ["AWX operator troubleshooting (https://ansible.readthedocs.io/projects/awx-operator/en/latest/troubleshooting/debugging.html)", "Automation controller administration - troubleshooting (https://docs.ansible.com/automation-controller/latest/html/administration/troubleshooting.html)", "AWX API ping endpoint (https://ansible.readthedocs.io/projects/awx/en/latest/rest_api/)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Controller health: pods, migrations and ping

## Health endpoints
```bash
curl -sk https://awx.example.com/api/v2/ping/ | jq            # unauthenticated: version, instances, capacity, ha
curl -sk -H "Authorization: Bearer $T" https://awx.example.com/api/v2/instances/ | jq '.results[] | {hostname, node_type, capacity, errors, last_seen}'
```
AAP 2.5 via gateway: `/api/controller/v2/ping/`. Use ping for load balancer health checks (HTTP 200, JSON with `instances`).

## AWX operator on Kubernetes
```bash
kubectl -n awx get awx,pods
kubectl -n awx logs deploy/awx-operator-controller-manager -c awx-manager -f    # reconciliation errors
kubectl -n awx logs deploy/awx-web -c awx-web --tail=100
kubectl -n awx logs deploy/awx-task -c awx-task --tail=100        # dispatcher, job launches
kubectl -n awx logs deploy/awx-task -c awx-ee                     # receptor/EE side
kubectl -n awx get events --sort-by=.lastTimestamp | tail -20
```
| Symptom | Likely cause |
|---|---|
| UI "AWX is currently upgrading" forever | migration job failed: `kubectl logs job/awx-migration-<ver>`; DB connectivity or disk |
| web pod CrashLoopBackOff | bad `extra_settings`, secret key mismatch after restore |
| jobs stay Pending | no instance with capacity / instance group empty / EE image pull failing |
| jobs Error "Receptor detail" | EE pull secret, container group pod spec, node unreachable |
| operator not reconciling | operator version vs CR fields, RBAC |

## Containerized AAP (podman)
```bash
podman ps --format '{{.Names}} {{.Status}}'
podman logs automation-controller-task --tail 100
journalctl --user -u automation-controller-task -n 100
```

## Pending jobs checklist
1. Instance group of the template/inventory/org has instances with capacity > 0.
2. `receptorctl status` on the node shows it advertising work types.
3. EE image pullable from that node (registry credential).

## Verify
- [ ] `/api/v2/ping/` lists every instance with capacity and a recent heartbeat.
