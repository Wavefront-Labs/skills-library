---
id: computing-software.cloud-infrastructure-engineering.methods.retire-a-product-from-a-shared-cluster
name: retire-a-product-from-a-shared-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: methods
tags: [method, recipe, decommission, retire, archive, teardown, shutdown, remove-product, remove-tenant, shared-cluster, multi-tenant, kubernetes, gitops, argocd, app-of-apps, ingress, load-balancer, dns, managed-database, alerting, alertmanager, sealed-secrets, orphaned-resources, finalizers, blast-radius, ordering, gates, rollback, cleanup, cost-saving, sunset, wind-down, end-of-life, close-down, mothball, discontinue, deprecate, off-board, shut-down, tear-down, switch-off, take-offline, delete-everything, old-project, side-project, unused-service, cost-cleanup, running-costs, keep-the-code, stop-paying, other-teams-depend]
level: advanced
status: verified
description: "Retire, shut down or decommission a product, app or tenant on a shared Kubernetes/GitOps cluster: inventory, re-home shared alerting, removal order, data last. Use when winding down a service."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Method: retire a product from a shared cluster

A **method** is a recipe, not a technique. Skills are the ingredients; this says which
ones to combine, in what order, and how you know each step is done. It owns no
technique of its own: every "how" below is a link to the skill that carries it, and
where no skill exists yet that is listed under **Gaps**.

**Outcome:** one product (its workloads, ingress, load balancer, DNS, managed databases,
monitoring and repo) is gone or mothballed, and everything else on the platform runs
exactly as before, with nothing still silently depending on the product.

**Executed end to end** on 8-9 Nov 2026: a SaaS tenant on a managed Kubernetes cluster
run by ArgoCD (app-of-apps), with a public ingress and cloud load balancer, two managed
databases, Cloudflare DNS, and a monitoring bundle that also carried the platform's only
alert delivery. The ordering below is what that run settled on; the failure modes are
what actually went wrong or nearly did.

**Use it when** the product owns infrastructure other things quietly lean on, which is
nearly always true of the first product on a platform: it tends to host the alerting,
the ingress, the dashboards and the scheduler everyone else uses.

---

## Ingredients (the skills this bundles)

| Phase | Skill |
|---|---|
| 0 Scope | `computing-software.cloud-infrastructure-engineering.site-reliability-engineering.reviewing-configuration-changes` |
| 0 Scope | `computing-software.cloud-infrastructure-engineering.terraform.blast-radius-review-and-pr-sizing` |
| 1 Inventory | `computing-software.cloud-infrastructure-engineering.kubernetes.namespace-full-object-inventory` |
| 1 Inventory | `computing-software.cloud-infrastructure-engineering.kubernetes.orphaned-resources-cleanup` |
| 1 Inventory | `computing-software.devops-ci-cd.argo-cd.resource-tracking-orphans-and-exclusions` |
| 1 Inventory | `computing-software.cloud-infrastructure-engineering.kubernetes.namespace-soft-multi-tenancy` |
| 2 Dependencies | `computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanagerconfig-crd` |
| 2 Dependencies | `computing-software.cloud-infrastructure-engineering.kubernetes.prometheus-operator-prometheusrule-and-alertmanagerconfig` |
| 3 Re-home | `computing-software.cloud-infrastructure-engineering.prometheus-grafana.alertmanager-receivers-and-webhooks` |
| 3 Re-home | `computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-meta-monitoring-and-deadmans-switch` |
| 3 Re-home | `computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-scopes` |
| 3 Re-home | `computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-seal-and-apply-workflow` |
| 4 Tolerant dependents | `computing-software.cloud-infrastructure-engineering.kubernetes.cloud-loadbalancer-service-annotations` |
| 4 Tolerant dependents | `computing-software.cloud-infrastructure-engineering.kubernetes.loadbalancer-service-pending` |
| 5 Remove | `computing-software.devops-ci-cd.argo-cd.app-of-apps-pattern` |
| 5 Remove | `computing-software.cloud-infrastructure-engineering.kubernetes.workload-garbage-collection-and-finalizers` |
| 5 Remove | `computing-software.cloud-infrastructure-engineering.kubernetes.remove-finalizers-safely` |
| 6 Leftovers | `computing-software.cloud-infrastructure-engineering.kubernetes.admission-webhooks-validating-and-mutating` |
| 6 Leftovers | `computing-software.cloud-infrastructure-engineering.kubernetes.operator-rbac-and-multi-tenancy-scoping` |
| 6 Leftovers | `computing-software.cloud-infrastructure-engineering.velero.cluster-scoped-resource-filters` |
| 7 Data | `computing-software.database-administration.database-backup-recovery.managed-cloud-database-backups` |
| 7 Data | `computing-software.database-administration.database-backup-recovery.legal-hold-and-deletion-in-backups` |
| 9 Verify | `computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-meta-monitoring-and-deadmans-switch` |

## Ordering law

**Reversible before irreversible; shared before owned; dependents before dependencies;
data last.** Each phase makes the next safe: you cannot remove the owner until its shared
services have a new home (2-3), you cannot remove a service until everything that calls
it tolerates its absence (4), and you cannot delete data until a second, independent scan
shows nothing else reads it (7). Importance is not the order; blast radius is.

## Phases

### 0. Scope and approvals
Decide per item: **mothball** (stop it, keep data and code) or **teardown** (delete,
unrecoverable). Write the list down and get the owner's explicit yes to every
irreversible item, individually, because scope tends to widen as the work goes on and
approval for one item is not approval for the next.
**Gate:** a written list with each item marked keep / stop / delete, and the delete items
approved.

### 1. Inventory what the product owns
Everything, in four places: its namespaces, cluster-scoped objects (webhooks, cluster
roles, ingress classes), objects it put into *other* namespaces (monitoring is the
classic), and things outside the cluster (DNS, load balancer, managed databases, image
registry, repo, third-party accounts). Find owned objects by their GitOps tracking
annotation, not by name.
**Gate:** zero objects you cannot assign to keep, stop, or delete; the external list is
as long as you expect, with no surprise entries.

### 2. Find what others depend on
For each owned thing ask who else uses it. Alert routes, dashboards, tunnel routes,
schedulers, shared secrets and quotas are the usual hidden ones. A routing object that
looks like "the product's alerts" often matches every alert in the cluster.
**Gate:** each shared function is named with its new owner. If any is unowned, stop here.

### 3. Re-home the shared pieces and prove them
Create the platform-owned copies **alongside** the originals (different names), so both
work during the changeover. Sealed secrets are bound to their name and namespace, so a
moved secret has to be resealed under the new name from the live values, never copied.
**Gate:** the new route is loaded by the running service, a test alert reaches the real
channel, the dead-man's-switch heartbeat is still arriving, and the old and new objects
coexist without errors.

### 4. Make dependents tolerate the removal, and deploy that first
Anything that calls the thing being removed (a scheduler that flips the load balancer, a
check that probes the ingress) must treat "not there" as normal, and be deployed and
exercised before the removal. Otherwise it fails every day from the moment you remove.
**Gate:** the changed dependent runs once against today's unchanged state with identical
behaviour, and once with the removed thing mocked absent.

### 5. Remove through Git, then verify what actually went
Delete the product's definitions from the GitOps repo. Do not assume that deleting an
application deletes what it created: an application without a deletion finalizer is
removed and **its resources keep running**. Read what is left and delete it explicitly,
selected by tracking annotation, in dependency order (child applications, monitoring
objects, workloads, then namespaces).
**Gate:** the applications are gone, no pod from the product is running anywhere, and
namespaces are deleted rather than stuck terminating.

### 6. Cluster-scoped and external leftovers
Namespace deletion does not remove cluster-scoped objects. Delete the webhook
configurations, cluster roles and bindings, and ingress classes the product's controller
installed. Then the cloud load balancer (it disappears when its Service does; confirm in
the provider listing) and the product's DNS records, leaving shared-zone records alone.
**Gate:** no webhook configuration points at a deleted service; the provider shows no
load balancer; only the product's own DNS records are gone.

### 7. Data last, after a second independent scan
Re-scan every Secret and ConfigMap in every namespace, and every repo that could hold a
connection string, for the database hostnames. Use bounded searches (specific repos or
namespaces); a repo-wide filesystem grep can be killed for memory and then tells you
nothing, which is not the same as "no hits". Decide on a final backup versus knowingly
skipping it, and record which.
**Gate:** the scan completed (not interrupted) with zero hits outside the product, the
backup decision is written down, and the owner has approved the deletion by name.

### 8. Archive and hand off
Write the handoff: why it was retired, what was shut down, what was kept, how to revive
it (and what cannot be recovered), and the owner-only actions that remain (store
submissions, API keys, accounts). Archive the repo last, after its final handoff commit
is merged. Update the trackers and memory so no one rebuilds it from habit.
**Gate:** someone with only the repo could explain what exists and what to do next.

### 9. Verify the platform, not the product
Confirm everything else: every application Synced and Healthy, no failing pods, a
scheduled job completes one cycle, alert routing delivers, hosted tools still answer.
**Gate:** the platform matches its pre-removal state minus the product.

## Acceptance criteria

- every item from phase 1 is accounted for as kept, stopped or deleted
- shared alerting delivers a test alert through the platform-owned route
- no scheduled job, probe or dashboard errors because of the removal
- no cluster-scoped leftovers, no load balancer or managed database still billing
- the second consumer scan is on record and clean
- the handoff document exists and the repo state matches it

## Failure modes this method exists to prevent

1. **Silencing the platform.** The product's monitoring bundle contained the only route
   from alerts to the team's channel. Deleting it would have stopped all cluster alerts,
   and nothing would have shown it until the next outage.
2. **A daily error from a dependent.** The scheduler assumed the ingress existed. Removing
   it first would have failed scale-up every morning.
3. **Orphans that keep running.** Deleting an application without a deletion finalizer
   left workloads, exporters and alert rules live, still connecting to the databases
   scheduled for deletion.
4. **Cluster-scoped debris.** An admission webhook left behind with no backing service can
   block creating objects cluster-wide.
5. **Deleting data a second consumer reads.** The first scan found only the product's own
   secrets; the second, repo-wide scan was killed for memory and proved nothing.
6. **Moving a sealed secret by copying it.** The ciphertext is bound to its original name
   and namespace; it must be resealed.
7. **Scope creep by sentences.** "Keep the data" became "delete the databases" mid-run.
   Re-confirm irreversible items when scope changes.


## Gaps (no skill exists yet; these are skills to write)

- cross-namespace consumer scan: find every Secret, ConfigMap and repo that references a
  given hostname or connection string
- managed-provider specifics: DigitalOcean Kubernetes (node pools, capacity refusals,
  load balancer ids on Services) and DigitalOcean managed databases
- tunnel and DNS cleanup: Cloudflare Tunnel hostname routes, Access policies, record
  deletion with the API
- writing a decommission handoff and revival note

## Verify

Walk the acceptance list with evidence in hand (command output, a delivered test alert, a
provider listing), not memory. If the consumer scan or the alert test has no record, that
phase was not done.
