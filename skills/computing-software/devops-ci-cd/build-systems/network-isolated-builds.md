---
id: computing-software.devops-ci-cd.build-systems.network-isolated-builds
name: network-isolated-builds
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, hermetic-builds, network-isolation-builds, no-network-sandbox, docker-network-none, buildkit-network-none, offline-builds, fetch-then-build, slsa-build-l3, egress-policy, nix-sandbox, harden-runner]
level: advanced
status: docs-checked
description: "Make builds hermetic by cutting network access: fetch-then-build split, docker/BuildKit --network=none, Kubernetes egress policies for build pods, Nix sandbox, and auditing egress."
sources: ["https://docs.docker.com/reference/dockerfile/#run---network", "https://pnpm.io/cli/fetch", "https://doc.rust-lang.org/cargo/commands/cargo-build.html", "https://pip.pypa.io/en/stable/cli/pip_install/", "https://github.com/step-security/harden-runner", "https://nix.dev/manual/nix/stable/store/building", "https://slsa.dev/spec/v1.0/requirements", "https://kubernetes.io/docs/concepts/services-networking/network-policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Network-isolated builds

A build that can reach the internet can pull a different dependency tomorrow, or
exfiltrate secrets today. Hermetic = all inputs are declared and fetched (with hashes)
before the build step, and the build step itself has **no network**.

## Pattern: fetch, then build offline
```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.23 AS deps
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download && go mod verify                 # network allowed, hashes checked

FROM deps AS build
COPY . .
RUN --network=none CGO_ENABLED=0 GOFLAGS=-mod=readonly GOPROXY=off go build -trimpath -o /out/app ./cmd/app
```
`RUN --network=none` (BuildKit Dockerfile syntax) runs that step with no network access; any hidden download
fails loudly. Equivalents:
- npm: `npm ci` in the fetch stage, then build without network access.
  pnpm: `pnpm fetch` populates the store from the lockfile, then `pnpm install --offline`.
- Cargo: `cargo fetch --locked` then `cargo build --frozen` (`--frozen` is `--locked` plus `--offline`).
- pip: `pip download -r req.txt -d wheels --require-hashes` then
  `pip install --no-index --find-links wheels -r req.txt`.
- Maven: `mvn dependency:go-offline` then `mvn -o package` (plugins resolved late can
  still escape; verify with the network off).
- Gradle: `--offline` after a warm-up resolve.

Whole-build: `docker run --network=none -v "$PWD:/src" builder make build`.

## In Kubernetes CI (Tekton, Jenkins agents, GitLab runners)
Default-deny egress for build namespaces and allow only the artifact proxy (NetworkPolicy enforcement requires a network plugin that supports it):
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: build-egress, namespace: ci-builds }
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress:
  - to: [{ namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: artifact-proxy } } }]
    ports: [{ port: 443, protocol: TCP }]
  - to: [{ namespaceSelector: {} , podSelector: { matchLabels: { k8s-app: kube-dns } } }]
    ports: [{ port: 53, protocol: UDP }, { port: 53, protocol: TCP }]
```
A single `to` entry with both `namespaceSelector` and `podSelector` selects those pods in those namespaces; the control plane sets the `kubernetes.io/metadata.name` namespace label automatically, and `k8s-app=kube-dns` is the label on cluster DNS pods in Kubernetes' DNS debugging guide. A proxy (Artifactory/Nexus) gives an auditable, cacheable single egress point.

## Hosted runners
You can't remove the network on GitHub-hosted runners, but `step-security/harden-runner`
with `egress-policy: audit` records the endpoints a job contacts; its documentation describes then restricting egress to an allowed-domain list.

## Nix / Bazel
Nix builds run in a sandbox: the process sees a loopback-only network configuration, except fixed-output derivations, which get network access to fetch declared content. Bazel: see
`computing-software.devops-ci-cd.build-systems.bazel-sandboxing`
(`--sandbox_default_allow_network=false`).

## Why it matters (SLSA)
SLSA's build track requires, from Build L3, that builds run in an isolated environment free of unintended external influence (no secrets of the build platform, no influence between builds, ephemeral environments). That requirement is about isolation between builds, not a ban on network access, so network isolation plus pinned, hash-verified inputs is a complementary control rather than the definition of L3.

## Verify
Run the build step with networking removed and a cold cache except for the fetched
deps: it succeeds. Add `curl https://example.com` to the build step: it fails.

## Checked
Date: 2026-10-25. Documentation: Kubernetes website sources (network-policies, labels, DNS debugging; kubernetes/website), Dockerfile reference (moby/buildkit `frontend/dockerfile/docs/reference.md`), pnpm `fetch` and `install` pages, Cargo `--frozen` option text, pip install docs, step-security/harden-runner README, Nix manual "Building" page (NixOS/nix), SLSA build requirements (slsa-framework/slsa `spec/build-requirements.md`).
Confirmed: `RUN --network=none`; `pnpm fetch` and `pnpm install --offline`; `--frozen` = `--locked` plus `--offline`; pip `--no-index`/`--find-links` and `--require-hashes`; harden-runner `egress-policy: audit` and allow-list egress control; Nix sandbox network behaviour and fixed-output derivations; SLSA "Isolated" requirement wording; NetworkPolicy `policyTypes`, selector combination semantics, the `kubernetes.io/metadata.name` label and the `k8s-app=kube-dns` label.
Removed: `npm ci --ignore-scripts` and `npm run build --offline`, the Nix "sandbox = true default" setting claim, the SLSA statement that L3 expects network isolation (the requirement is build isolation), and the DNS rule restricted to UDP (TCP added).
Method: documentation only; no commands were run.
