---
id: computing-software.cloud-infrastructure-engineering.kubernetes.multi-cluster-dr-failover-runbook
name: multi-cluster-dr-failover-runbook
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cluster-failover, dr-failover, disaster-recovery, multi-cluster, runbook, rto-rpo]
level: advanced
status: docs-checked
description: "Fail a production workload over from one Kubernetes cluster or region to a standby: readiness criteria, data promotion, GitOps retargeting, DNS/GSLB shift, verification, failback."
sources: ["https://velero.io/docs/main/disaster-case/", "https://velero.io/docs/main/resource-filtering/", "https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html", "https://sre.google/sre-book/managing-incidents/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-cluster DR failover runbook

## Prerequisites (before the bad day)
- Standby cluster provisioned from the same IaC and GitOps repo; same add-on versions,
  CRDs, secrets backend access, image registry access (replicated registry in the DR region).
- Standby state: **warm** (apps deployed, scaled low) or **pilot light** (platform only).
  Decide per service from RTO.
- Data replication per store with known RPO: DB cross-region replicas, object storage
  replication, Velero backups (schedules to a bucket in the DR region) for PV data and
  cluster objects not in Git.
- Traffic layer able to shift: DNS failover with health checks and a low TTL, or a global
  load balancer with both backends registered.
- Runbook rehearsed at least quarterly with timings recorded.

## Decision
Declare failover on defined triggers (region outage confirmed by provider, primary
control plane unrecoverable within RTO). Name one incident commander. Record the time:
everything written after the last replicated point is the accepted data loss.

## Steps
1. **Freeze**: stop deploy pipelines and GitOps sync to the primary (turn off Argo CD automated
   sync with `spec.syncPolicy.automated.enabled: false`, or `flux suspend kustomization <name>`)
   so a recovering primary does not fight the DR side.
2. **Fence the primary** if it is partially alive: stop writers (scale to 0, revoke DB
   credentials) to avoid split brain.
3. **Promote data**: promote the DB replica in the DR region; confirm replication lag at
   promotion time; update connection endpoints (Secrets via ESO, or DNS CNAMEs for DBs).
4. **Restore cluster state not in Git**: first set the Velero BackupStorageLocation to
   read-only so no backups are created or deleted during the restore:
   `kubectl patch backupstoragelocation <name> -n velero --type merge -p '{"spec":{"accessMode":"ReadOnly"}}'`.
   Then `velero restore create --from-backup <latest> --include-namespaces <ns1>,<ns2>` for
   PV-backed workloads, and set `accessMode` back to `ReadWrite` afterwards.
5. **Scale up** the DR workloads to production capacity: change the overlay/values in Git
   (replicas, HPA min) or ApplicationSet generator to target the DR cluster. Pre-warm
   node pools; capacity in the DR region may be contended during regional events.
6. **Shift traffic**: flip DNS/GSLB weights; watch TTL expiry and client caching.
7. **Verify**: synthetic checks on critical journeys, error rates, queue consumers running
   exactly once (no duplicate consumers in both regions), scheduled jobs running in DR only.
8. **Communicate** status and expected data loss window.

## Failback
Treat as a planned migration: re-establish replication primary <- DR, wait for sync,
schedule a window, repeat the steps in reverse. Never fail back automatically.

## Common failures
- Secrets/IAM bound to primary-region resources (KMS keys, IRSA roles) not replicated.
- Hard-coded regional endpoints in config.
- CronJobs and consumers active in both clusters after the primary recovers.
- DNS TTL far higher than assumed in intermediate resolvers.

## Verify (each drill)
- [ ] Measured RTO and RPO recorded against targets; action items for every manual step that surprised anyone.

## Checked
2026-10-27 against the Velero docs (velero.io main docs, latest release v1.18.4: disaster
recovery, restore reference, resource filtering), the Argo CD automated sync policy page and
the Flux getting-started docs. Confirmed: `velero restore create --from-backup` with
`--include-namespaces`, the read-only BackupStorageLocation step, `spec.syncPolicy.automated.enabled`
and `flux suspend kustomization`. Removed a fixed 60-second TTL that no source gives; source URLs
respond.
Method: documentation only; no commands were run.
