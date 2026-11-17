---
id: computing-software.cloud-infrastructure-engineering.docker.image-reference-grammar-and-defaults
name: image-reference-grammar-and-defaults
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, image-reference, docker-io-library, image-tags, digest, registry, normalization]
level: practitioner
status: docs-checked
description: "Parse image references correctly: registry host detection, docker.io and library/ defaults, tag and digest rules, allowed characters, and why localhost:5000/app differs from app."
sources: ["https://docs.docker.com/reference/cli/docker/image/tag/", "https://github.com/distribution/reference/blob/main/reference.go", "https://github.com/opencontainers/distribution-spec/blob/main/spec.md#pulling-manifests"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image reference grammar and defaults

```
[HOST[:PORT]/]NAMESPACE/.../REPOSITORY[:TAG][@DIGEST]
```

The formal grammar is in the `distribution/reference` package: `reference := name [ ":" tag ] [ "@" digest ]`.

## Normalisation rules

| You write | Docker resolves to |
|---|---|
| `nginx` | `docker.io/library/nginx:latest` |
| `bitnami/redis` | `docker.io/bitnami/redis:latest` |
| `ghcr.io/org/app:1.2` | as written |
| `localhost:5000/app` | registry `localhost:5000`, repo `app` |
| `myhost/app` | **Docker Hub** user `myhost`, not a host named myhost |
| `app:1.2@sha256:abc...` | digested reference; the tag is dropped (docker convention) |

In `distribution/reference`, the first path component is treated as a registry domain only if it is exactly
`localhost`, contains a `.` or a `:`, or is not all lowercase. `index.docker.io` is canonicalised to
`docker.io`. That is why `registry/app` refers to Docker Hub.

## Component rules

- Repository path: lowercase alphanumerics joined by separators (`.`, `_`, `__`, one or more `-`), with
  components joined by `/`. Uppercase is rejected with `invalid reference format: repository name (<name>)
  must be lowercase`.
- Tag: `[\w][\w.-]{0,127}`, so up to 128 characters of letters, digits, `_`, `.` and `-`, not starting with
  `.` or `-`. A `+` is not allowed, so semver build metadata `1.2.3+build5` must become `1.2.3-build5` or
  `1.2.3_build5`.
- Digest: `algorithm:hex`. For `sha256` the hex part is 64 characters.
- The repository name is limited to 255 characters in total.

## Practical consequences

```bash
docker tag app reg.example.com:5000/team/app:1.2.3      # explicit host avoids Hub surprises
docker pull nginx:1.27@sha256:<digest>                   # digest wins over the tag
docker image inspect -f '{{index .RepoDigests 0}}' nginx:1.27
```

- `docker.io`, `index.docker.io` and `registry-1.docker.io` all denote Docker Hub; the `docker login` reference
  describes Docker Hub credentials stored under `https://index.docker.io/v1/`.
- Kubernetes pod specs follow the same convention: `busybox` is equivalent to
  `docker.io/library/busybox:latest` unless a default registry is configured.

## Gotchas

- CI that derives image names from branch names must lowercase and sanitise them (`feature/ABC-1` is not a
  valid tag because `/` is not allowed in a tag).
- `docker push app` without a host targets `docker.io/library/app`, which you cannot push to; use an explicit
  host or your Hub namespace.

## Checked

2026-10-26. Documentation release: distribution/reference main (reference.go grammar and normalize.go), OCI distribution-spec main (name and tag rules), Kubernetes website images page and docker/cli login reference, checked 2026-10-26. Confirmed: grammar productions, tag pattern (128 characters, first character a word character), 255 character repository limit, default domain docker.io with library/ prefix and :latest, localhost, dot, colon and uppercase rules for treating the first component as a domain, index.docker.io canonicalisation, the lowercase error text, tag-dropping behaviour of docker's ParseDockerRef, Kubernetes default equivalence. Fixed: the lowercase error message now includes the repository name, the domain heuristic gained the uppercase rule, and the digest rule is stated per algorithm. Removed unconfirmed claims: the exact `denied` error text for pushing to library/, a containerd-specific statement, and a Compose quoting remark.

Method: documentation only; no commands were run.
