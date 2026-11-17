---
id: computing-software.systems-network-administration.patch-management.container-base-image-rebuilds
name: container-base-image-rebuilds
category: computing-software
field: systems-network-administration
product: patch-management
tags: [image-patching, immutable-infrastructure, base-image-update, image-rebuild, renovate, dependabot, digest-pinning, containers, patch-management]
level: practitioner
status: docs-checked
description: "Patch containers by rebuilding, not by patching running containers: pin base images by digest, automate base-image bump PRs, scheduled rebuilds, and redeploying to production."
sources:
  - https://csrc.nist.gov/pubs/sp/800/190/final
  - https://docs.renovatebot.com/docker/
  - https://fluxcd.io/flux/components/image/
  - https://kubernetes.io/docs/tasks/access-application-cluster/list-all-running-container-images/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patching container images by rebuilding

**Goal:** vulnerabilities in base images and OS packages inside containers get fixed
through the normal build pipeline within the same SLAs as servers.

## Principle
Treat containers as immutable (NIST SP 800-190 is the reference for container security guidance): never `apt upgrade` inside a running container. Fix the image
(Dockerfile/base image), rebuild, scan, redeploy. Running containers are replaced.

## Pin and bump
- Pin base images by **digest** for reproducibility:
  `FROM docker.io/library/debian:12-slim@sha256:<digest>`
- Renovate recommends pinning Docker images to an exact digest so builds are immutable. It opens
  pull requests when the digest behind a tag changes (for example a security rebuild by the base
  image publisher); digest updates can be auto-merged with the `default:automergeDigest` preset
  once tests pass.
- Include an OS update layer only when the base lags a fix:
  `RUN apt-get update && apt-get -y upgrade && rm -rf /var/lib/apt/lists/*` (prefer a
  fresher base when possible).

## Scheduled rebuilds
Even without code changes, rebuild images weekly (CI cron) so new base digests and package
fixes land; tag with date and git SHA; scan; promote via the same environments as app
changes.

## Redeploy
- Kubernetes: update the image tag/digest in manifests (GitOps PR) → rollout; or Flux image
  automation (image-reflector-controller and image-automation-controller).
- Inventory running images (the Kubernetes task "List All Container Images Running in a
  Cluster" shows the kubectl jsonpath method; use `status.containerStatuses[].imageID` for
  digests) against the registry's scan results: an image fixed in the registry but still running old pods is
  not remediated.

## Choose smaller bases
Distroless, `-slim`, Alpine, or vendor minimal images reduce the package count and so the
patch volume; static binaries on `scratch` remove the OS layer entirely.

## Gotchas
- `:latest` or floating tags make rebuilds non-reproducible and rollbacks impossible.
- Multi-stage builds: patch the final stage's base; builder stages matter only for
  supply-chain risk.
- Third-party images (databases, ingress controllers) need their vendors' releases; track
  them like any other product.

## Verify
Scanner shows no fixable critical/high CVEs in images running in production; base digest
age per image is under your SLA; running pods use the latest built digest.

## Checked
Date: 2026-10-27. Documentation checked: Renovate Docker documentation (digest pinning, `default:automergeDigest`), Flux GitOps Toolkit image automation controllers page, Kubernetes "List All Container Images Running in a Cluster" task and Pod API reference (`containerStatuses[].imageID`). NIST SP 800-190 is cited only as the container security reference, not for a specific figure. Removed the Dependabot and Argo CD Image Updater claims, which were not confirmed.

Method: documentation only; no commands were run.
