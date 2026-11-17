---
id: computing-software.cloud-infrastructure-engineering.kubernetes.harbor-registry-and-proxy-cache
name: harbor-registry-and-proxy-cache
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, harbor, harbor-registry, proxy-cache, air-gapped, container-registry, replication, robot-accounts]
level: practitioner
status: docs-checked
description: "Run Harbor as a cluster's internal registry: Helm install with external DB/storage, proxy-cache projects for Docker Hub and registry.k8s.io, replication, robot accounts and GC."
sources: ["https://goharbor.io/docs/main/administration/configure-proxy-cache/", "https://goharbor.io/docs/main/administration/garbage-collection/", "https://goharbor.io/docs/main/administration/robot-accounts/", "https://github.com/goharbor/harbor-helm", "https://github.com/containerd/containerd/blob/main/docs/hosts.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Harbor as the internal registry, with proxy cache

## Install (Helm)
```bash
helm repo add harbor https://helm.goharbor.io
helm install harbor harbor/harbor -n harbor --create-namespace -f values.yaml
```
Key values (chart defaults in brackets): `expose.type` [ingress] with TLS, `externalURL` [https://core.harbor.domain],
`persistence.imageChartStorage.type` [filesystem; choose an object store such as `s3` for anything real],
`database.type` [internal] and `redis.type` [internal] set to `external` for HA, `trivy.enabled` [true].
Harbor's own images must come from somewhere reachable — mirror them first in an air gap.

## Proxy-cache projects
1. Administration → Registries → New endpoint. Proxy cache supports Harbor, Docker Hub, Docker registry,
   AWS ECR, Azure Container Registry, Google Container Registry, Quay, GitHub Container Registry and JFrog
   Artifactory; use an access account with least privilege, since the cache project can pull everything that
   account can.
2. Projects → New → **Proxy Cache** on, select the endpoint, name e.g. `dockerhub`.
3. Pull through it: `harbor.internal/dockerhub/library/nginx:1.27` (prefix `<harbor_servername>/<proxy_project_name>/`). Point containerd at it via
   `certs.d/docker.io/hosts.toml` with `override_path = true` (containerd's field for a host whose API root is
   not `/v2`) and `https://harbor.internal/v2/dockerhub` so manifests keep `docker.io/...` names.
On a later pull Harbor checks the latest manifest upstream (a HEAD request since v2.1.1, which does not
trigger the Docker Hub rate limiter): unchanged images are served from the cache, updated ones are pulled and
cached, the cached image is served if the upstream is unreachable, and nothing is served if the image is gone upstream.

## Fully air-gapped: replication instead
In the connected zone: a Harbor with **pull replication** rules from upstream, then move the images to the
disconnected Harbor by your own export and import process, or push-replicate across a one-way link.
Replicate digest-pinned image lists generated from your manifests.

## Access
- Robot accounts per consumer: system robot accounts carry permissions across projects, project robot
  accounts are limited to one project; they cannot log into the UI. Grant pull-only to clusters and push to one
  project for CI.
- Project-level vulnerability policy: "Prevent vulnerable images from running" with a chosen severity
  blocks pulls of images at or above it — it can break deploys during CVE storms, so pair it with the allowlist.
- Tag immutability rules for release tags.

## Operations
- **Garbage collection** (Administration → Clean Up) is required to free storage after deletion: space is
  not freed automatically and GC removes blobs no manifest references. It can be scheduled (None, Daily at
  midnight, Weekly at midnight on Saturday), supports a dry run, optionally deletes untagged artifacts, and
  skips layers uploaded within a 2 hour window.
- Tag retention rules: for example keep the N most recently pulled artifacts per repository, or those pulled in the last X days.
- Back up the database and object storage together.

## Verify
- [ ] `crictl pull docker.io/library/busybox:1.36` on a node with no internet succeeds via Harbor.
- [ ] Harbor GC job history shows successful runs; storage graph flat.

## Checked

Checked on 2026-10-26 against `goharbor/website` docs (administration/configure-proxy-cache, garbage-collection, robot-accounts, working-with-projects/project-configuration, tag retention and immutability pages), the `goharbor/harbor-helm` `values.yaml` and README (latest release v1.19.4), and containerd `docs/hosts.md` for `override_path`.
Confirmed: Helm repo `https://helm.goharbor.io`; chart defaults for `expose.type`, `externalURL`, `imageChartStorage.type`, `database.type`, `redis.type`, `trivy.enabled`; the list of proxy-cache endpoint types; proxy cache behaviour; GC schedule options, dry run, untagged option and 2 hour window; robot account kinds; the "Prevent vulnerable images from running" project setting; retention rules.
Removed as unconfirmed: the 7 day cache cleanup default, the `skopeo sync`/`oras` and `yq` pipeline, and short robot expiry as a Harbor-specific claim.

Method: documentation only; no commands were run.
