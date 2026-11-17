---
id: computing-software.software-engineering.go.private-modules-goprivate-goproxy
name: private-modules-goprivate-goproxy
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-modules, goprivate, goproxy, gonosumdb, gonoproxy, private-repositories, athens, netrc, checksum-database]
level: practitioner
status: docs-checked
description: "Fetch private Go modules in dev and CI: GOPRIVATE/GONOSUMDB, git auth via .netrc or insteadOf, and running a module proxy like Athens or Artifactory."
sources:
  - https://go.dev/ref/mod#private-modules
  - https://go.dev/ref/mod#environment-variables
  - https://go.dev/ref/mod#private-module-privacy
  - https://docs.docker.com/build/building/secrets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private modules: GOPRIVATE and GOPROXY

**Goal:** `go mod download` works for internal modules on laptops and CI, without
leaking private module paths to the public proxy or checksum database.

## Why it fails by default
Go fetches modules via `GOPROXY=https://proxy.golang.org,direct` and verifies them
against `sum.golang.org`. Neither can see your private repos, and the checksum database would also
receive the module path (see the Go modules reference section on privacy). Failures typically show up as 404 or 410 responses
from the proxy or the checksum database.

## Configure
```bash
go env -w GOPRIVATE='github.com/acme/*,gitlab.internal.example.com'
```
GOPRIVATE sets defaults for both:
- `GONOPROXY` - fetch these directly from VCS (skip proxy)
- `GONOSUMDB` - don't check these against the public checksum DB
If you run a private proxy that should serve private modules, point `GOPROXY` at it instead of relying on direct fetches
(the reference example uses `GOPROXY=https://proxy.corp.example.com` with `GONOSUMDB=corp.example.com`).

## Authentication for direct fetches
Go runs `git`; configure git (or a `.netrc`, or `GOAUTH` in Go 1.24+), not Go:
```bash
# HTTPS with token (CI)
printf "machine github.com login x-access-token password %s\n" "$GH_TOKEN" > ~/.netrc
# or rewrite to SSH (dev machines)
git config --global url."git@github.com:acme/".insteadOf "https://github.com/acme/"
```
`GIT_TERMINAL_PROMPT=0` disables Git credential prompts so failures are immediate in CI. For hosts that cannot answer the `?go-get=1` query,
put a VCS suffix such as `.git` after the repository root in the module path (`corp.example.com/repo.git/mod`).

## Private proxy (larger orgs)
An internal module proxy can serve private modules: `GOPROXY=https://proxy.corp.example.com,https://proxy.golang.org,direct`
(the go command falls back to the next entry on a 404 or 410 response).
Keep `go.sum` committed either way.

## Docker builds
Pass credentials as BuildKit secrets, not ARG/ENV:
```dockerfile
RUN --mount=type=secret,id=netrc,target=/root/.netrc go mod download
```

## Verify
- [ ] `go env GOPRIVATE GONOSUMDB GOPROXY` correct in CI logs.
- [ ] A clean CI runner (empty module cache) downloads all modules.
- [ ] No tokens in image layers.

## Checked

2026-10-25. Checked against the Go Modules Reference (golang/website `ref/mod`: private modules and the privacy section, environment variables `GOPRIVATE`, `GONOPROXY`, `GONOSUMDB`, `GOPROXY` default `https://proxy.golang.org,direct`, fallback on 404 and 410, `.netrc`, `GIT_TERMINAL_PROMPT=0`, VCS suffix paths, `GOAUTH` in Go 1.24+) and the Docker build secrets documentation (`RUN --mount=type=secret`). Removed unconfirmed details: exact error strings, `GONOPROXY=none`, GitLab subgroup behaviour, named proxy products and their benefits, and the `docker history` check.

Method: documentation only; no commands were run.
