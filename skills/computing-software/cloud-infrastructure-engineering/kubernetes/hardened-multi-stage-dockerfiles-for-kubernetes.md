---
id: computing-software.cloud-infrastructure-engineering.kubernetes.hardened-multi-stage-dockerfiles-for-kubernetes
name: hardened-multi-stage-dockerfiles-for-kubernetes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, dockerfile-hardening, multi-stage-build, distroless, non-root, supply-chain, cks, container-image, distroless-base]
level: practitioner
status: docs-checked
description: "Write images that pass restricted Pod Security: multi-stage builds, minimal or distroless bases pinned by digest, numeric non-root USER, and correct signal handling."
sources: ["https://docs.docker.com/build/building/multi-stage/", "https://docs.docker.com/build/building/best-practices/", "https://docs.docker.com/reference/dockerfile/", "https://docs.docker.com/build/building/secrets/", "https://github.com/GoogleContainerTools/distroless", "https://kubernetes.io/docs/concepts/security/pod-security-standards/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hardened multi-stage Dockerfiles for Kubernetes

## Template (Go; same shape for Java/Node/Python)
```dockerfile
# syntax=docker/dockerfile:1
FROM golang:<version>@sha256:<digest> AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod go mod download
COPY . .
RUN --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -trimpath -ldflags='-s -w' -o /out/app ./cmd/app

FROM gcr.io/distroless/static-debian13:nonroot@sha256:<digest>
COPY --from=build /out/app /app
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/app"]
```

## Rules and why
- **Multi-stage**: compilers, package managers and source never reach the runtime image.
- **Minimal base** (distroless, Chainguard's static images, `scratch` for static binaries): fewer
  packages and no shell for an attacker. The distroless README currently lists `static-debian13`,
  `base-debian13` and others with `latest`, `nonroot`, `debug` and `debug-nonroot` tags, and says any
  other tags are deprecated and no longer updated. Pin by **digest** and let Renovate/Dependabot bump
  it (Docker's best practices also recommend pinning base image versions).
- **Numeric `USER`**: PSA `restricted` requires `runAsNonRoot: true`, and the kubelet can only
  verify a numeric UID. `USER app` (a name) fails with `container has runAsNonRoot and image has
  non-numeric user (app), cannot verify user is non-root`. Distroless `nonroot` images use UID 65532.
- **Exec-form ENTRYPOINT** so the app is PID 1 and receives SIGTERM: Docker documents that the
  shell form starts the executable as a subcommand of `/bin/sh -c`, which does not pass signals, so
  the executable is not PID 1 and does not receive SIGTERM.
- **Read-only root filesystem**: write only to mounted `emptyDir` (`/tmp`, caches) so
  `readOnlyRootFilesystem: true` works.
- **Secrets at build time** via `RUN --mount=type=secret,id=npmrc`, never `ARG`/`ENV`
  (they persist in image history).
- `.dockerignore` excludes `.git`, `.env`, local credentials, `node_modules`.
- Define health checks as probes in the pod spec rather than relying on a Dockerfile `HEALTHCHECK`.

## Matching pod securityContext
```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities: {drop: [ALL]}
  seccompProfile: {type: RuntimeDefault}
```

## Debugging shell-less images
`kubectl debug -it <pod> --image=busybox --target=app` (ephemeral container sharing the
process namespace); do not add a shell back to the image.

## Verify
```bash
docker image inspect <img> --format '{{.Config.User}}'       # numeric
trivy image --severity HIGH,CRITICAL <img>
docker history --no-trunc <img> | grep -iE 'secret|token|password'   # nothing
kubectl apply --dry-run=server -f deploy.yaml   # no PSA restricted warnings
```

## Checked

2026-10-27. Release: Docker docs, distroless README (Debian 13 images), Kubernetes v1.37 docs (kubernetes/website main), Trivy docs, accessed October 2026
- Corrected the base image: the distroless README now lists `static-debian13` (not `static-debian12`) with `nonroot` tags, and `NONROOT = 65532` in the repository variables confirms the UID.
- Confirmed the kubelet error text `container has runAsNonRoot and image has non-numeric user (<name>), cannot verify user is non-root` in the kubelet source, and that PSS `restricted` requires `runAsNonRoot`, `allowPrivilegeEscalation: false`, dropping ALL capabilities and a seccomp profile (Pod Security Standards page; `readOnlyRootFilesystem` is not part of it).
- Confirmed in Docker's Dockerfile reference that shell-form ENTRYPOINT does not pass signals or become PID 1, that `RUN --mount=type=cache` and `type=secret` exist, and that build args and environment variables persist in the final image (Docker secrets page); confirmed `kubectl debug ... --image=busybox --target=` in the Kubernetes debug page and `trivy image --severity HIGH,CRITICAL` in the Trivy docs.
- Removed the pinned Go tag and the unsupported tini/shareProcessNamespace and Wolfi remarks.

Method: documentation only; no commands were run.
