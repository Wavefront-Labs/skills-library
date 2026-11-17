---
id: computing-software.cloud-infrastructure-engineering.docker.registry-management
name: registry-management
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, container-registry, oci-registry, docker-hub, ecr, artifact-registry, acr, ghcr, harbor, distribution-registry, image-tags, digest, immutable-tags, tag-strategy, retention-policy, lifecycle-policy, garbage-collection, pull-through-cache, registry-mirror, rate-limits, credential-helper, imagepullsecrets, replication, crane, skopeo, oras, oci-artifacts, manifest-list, image-index, multi-arch, promotion]
level: practitioner
status: docs-checked
description: "Run container registries well: tag and digest strategy, immutable tags, promotion by copy, retention and GC, pull-through caches for Docker Hub limits, credential helpers, replication."
sources: ["https://github.com/opencontainers/distribution-spec/blob/main/spec.md", "https://docs.docker.com/docker-hub/image-library/mirror/", "https://distribution.github.io/distribution/about/garbage-collection/", "https://goharbor.io/docs/main/working-with-projects/working-with-images/create-tag-retention-rules/", "https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane.md", "https://github.com/containers/skopeo/blob/main/docs/skopeo-copy.1.md", "https://github.com/boto/botocore/blob/develop/botocore/data/ecr/2015-09-21/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container registry management — tags, retention, mirrors and access

**Goal:** every deployed image is traceable to a commit and cannot change under you, storage
does not grow forever, builds do not fail on upstream rate limits, and only the right
identities can push or pull. Vulnerability scanning and signing are in
`computing-software.cloud-infrastructure-engineering.docker.container-image-security-scanning`.

## 1. Tags vs digests
- A **digest** (`@sha256:...`) is the content hash of the manifest — immutable by definition.
- A **tag** is a movable pointer. Deploy by digest (or by an immutable tag) so a re-push can
  never change what production runs.
- Multi-arch images are an **image index** (manifest list); its digest differs from each
  per-platform manifest digest. Pin the index digest so each node pulls its own arch.
- Inspect without pulling: `crane digest <IMAGE>:<TAG>`, `docker buildx imagetools inspect <IMAGE>`,
  `skopeo inspect docker://<IMAGE>`.

## 2. Tag strategy
- Build tags: `<git-sha>` (always), plus `<semver>` on release and optionally `<branch>-<sha>`.
- Avoid deploying `latest` or branch tags; they are fine as human convenience pointers.
- Turn on **tag immutability** where supported: Amazon ECR repositories take an image tag mutability
  setting (`MUTABLE`, `IMMUTABLE`, `IMMUTABLE_WITH_EXCLUSION`, `MUTABLE_WITH_EXCLUSION`, with WILDCARD
  exclusion filters), Harbor has tag immutability rules, and Docker Hub has immutable tags. Use exclusion
  rules for convenience tags like `latest` if needed.

## 3. Promotion by copy, not rebuild
Promote the exact bytes that passed tests:
```bash
crane copy registry-dev.example.com/api@sha256:<DIGEST> registry-prod.example.com/api:1.8.0
skopeo copy --all docker://registry-dev.example.com/api@sha256:<DIGEST> docker://registry-prod.example.com/api:1.8.0
crane tag registry-prod.example.com/api:1.8.0 stable
```
`crane copy` retains the digest value. skopeo `--all` copies the whole list of images and the list itself
(without it only the image matching the current platform is copied). Check each tool's support for
copying referrers such as signatures and SBOMs, and verify them in the destination.

## 4. Retention and garbage collection
- Define lifecycle or retention rules per repository: keep the last N release tags (or per compliance),
  expire untagged manifests and short-lived `pr-*`/branch tags after a set time. Use the registry's own
  syntax (ECR lifecycle policies, Harbor tag retention) and confirm it in that product's documentation.
```json
{"rules": [{"rulePriority": 1, "description": "expire untagged",
  "selection": {"tagStatus": "untagged", "countType": "sinceImagePushed", "countUnit": "days", "countNumber": 7},
  "action": {"type": "expire"}}]}
```
  (ECR syntax; others have equivalents.)
- **Never expire anything running.** Cross-check against images in use
  (`kubectl get pods --all-namespaces` with `-o jsonpath` over `.spec.containers[*].image` and init containers)
  before enabling aggressive rules.
- Self-hosted `distribution` registry: deleting a manifest only unlinks it; disk is freed by
  `registry garbage-collect --delete-untagged /path/to/config.yml` with the
  registry in **read-only mode** (GC racing a push can corrupt images). Harbor schedules GC for you.

## 5. Pull-through caches and rate limits
- Docker Hub limits pulls (limits change; check the current numbers in the Docker Hub usage documentation).
  CI fleets behind one NAT IP hit them first.
- Put a pull-through cache in front: ECR pull-through cache rules, Harbor proxy cache projects, or the
  `distribution` registry with `proxy.remoteurl: https://registry-1.docker.io`. Other clouds have their own
  caching features; see their documentation.
- Point clients at it: containerd `hosts.toml` mirror config, Docker `"registry-mirrors"`
  in `daemon.json` (Docker Hub only), or rewrite image references (`mirror.example.com/library/postgres:16`).
- Mirrors of Docker Hub remain subject to Docker's fair use policy.

## 6. Access
- Humans and CI use credential helpers or the registry vendor's login command — no long-lived passwords in
  `~/.docker/config.json`.
- CI pushes with OIDC-federated short-lived credentials; one push identity per pipeline,
  scoped to its repositories.
- Kubernetes pulls via node IAM (EKS/GKE/AKS native integration) or `imagePullSecrets`
  attached to the ServiceAccount, not each pod spec.
- Separate repositories (or projects) for dev and prod so prod pull identities cannot see
  unreviewed images.

## Gotchas
- Retention by "last N images" counts per repository — a busy branch can evict a release
  image unless releases are protected by a tag-prefix rule.
- `docker rmi` only deletes locally; registry deletion uses the registry API/console.
- OCI artifacts (Helm charts, SBOMs, WASM, signatures) share the registry and its retention
  rules — make sure rules do not delete signatures of kept images.
- Docker Hub `library/` official images: `postgres:16` really means `docker.io/library/postgres:16`;
  mirrors need the full path.

## Verify
- [ ] Every production workload references a digest or an immutable tag.
- [ ] Pushing an existing release tag is rejected.
- [ ] Lifecycle rules dry-run (where available) shows no in-use image would be deleted.
- [ ] CI pulls of Docker Hub images go through the cache (check cache hit metrics/logs).
- [ ] No static registry password exists in CI secrets or on nodes.
- [ ] A promoted image's digest in prod equals the digest tested in staging.

## Checked

2026-10-26. Documentation release: distribution/distribution, OCI distribution-spec, docker/docs, Harbor website docs, go-containerregistry crane docs, skopeo-copy man page and the botocore ECR model, all at main on 2026-10-26. Confirmed: crane digest/copy/tag commands and copy retaining the digest, skopeo copy --all semantics, distribution garbage-collect command and read-only requirement, Docker Hub mirror page (fair use note, Hub-only mirroring), Harbor tag retention, ECR tag mutability values and exclusion filter type, the kubectl jsonpath approach from the Kubernetes docs. Removed unconfirmed claims: cloud-specific immutability and cache features outside ECR, the ECR lifecycle JSON example, cloud credential-helper commands, retention periods (7 and 30 days), egress charges, and the old /etc/docker/registry GC path.

Method: documentation only; no commands were run.
