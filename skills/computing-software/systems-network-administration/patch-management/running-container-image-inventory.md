---
id: computing-software.systems-network-administration.patch-management.running-container-image-inventory
name: running-container-image-inventory
category: computing-software
field: systems-network-administration
product: patch-management
tags: [running-image-inventory, container-inventory, kubernetes, image-digest, patch-management]
level: practitioner
status: docs-checked
description: "Inventory the container images actually running in clusters by digest, map them to owners and registries, and scan what runs, not just what sits in registries."
sources:
  - https://kubernetes.io/docs/tasks/access-application-cluster/list-all-running-container-images/
  - https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/
  - https://trivy.dev/latest/docs/target/kubernetes/
  - https://docs.aws.amazon.com/cli/latest/reference/ecs/describe-tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running container image inventory

**Goal:** a list of every image digest running now, which workload runs it and who owns it, so a new CVE can be answered with "these 14 pods" rather than "these 600 registry tags".

## List running images with digests
```sh
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{range .status.containerStatuses[*]}{.imageID}{" "}{end}{"\n"}{end}'
```
Use `status.containerStatuses[].imageID` (resolved digest), not `spec.containers[].image` (a tag that may have moved). Include `initContainerStatuses` and `ephemeralContainerStatuses`.

Unique digest count and where they run:
```sh
kubectl get pods -A -o json | jq -r '.items[] | .metadata.namespace as $ns | .status.containerStatuses[]? | "\(.imageID)\t\($ns)"' | sort -u
```

## Add ownership
Map namespace or workload labels (`app.kubernetes.io/name`, `team`, `owner`) to a team. Enforce an owner label with an admission policy so the inventory never has orphans.

## Scan what runs
```sh
trivy k8s --report summary --scanners vuln
trivy image --format json ghcr.io/org/app@sha256:... > app.json
```
Or install the Trivy Operator in the cluster, which scans it continuously (see the Trivy Operator project).

## Outside Kubernetes
- Docker hosts: list containers with `docker ps --format '{{.ID}} {{.Image}}'` and resolve each image with `docker image inspect`.
- ECS: `aws ecs describe-tasks` -> `containers[].imageDigest`.

## Gotchas
- Pods with `imagePullPolicy: IfNotPresent` and a mutable tag may run an old digest on some nodes and a new one on others; inventory by digest exposes this.
- Short-lived Jobs/CronJobs disappear between snapshots; collect continuously (operator or event-based) or from the registry pull logs.
- Sidecars injected by meshes (istio-proxy) are images too; they count.

## Verify
For one deployment, the inventory digest equals the digest the container runtime reports on the node, and the scanner report references the same digest.

## Checked
Date: 2026-10-27. Documentation checked: Kubernetes Pod API reference (`status.containerStatuses[].imageID`, `initContainerStatuses`, `ephemeralContainerStatuses`), the Kubernetes "List All Container Images Running in a Cluster" task, Trivy Kubernetes target page (`trivy k8s --report summary`, Trivy Operator), AWS CLI `ecs describe-tasks` reference (`containers[].imageDigest`), Docker `container ls` format placeholders. Removed `trivy k8s ... cluster` (no such argument), the cloud scanner claims, the Docker `RepoDigests` pipeline and the `crictl` command, which were not confirmed.

Method: documentation only; no commands were run.
