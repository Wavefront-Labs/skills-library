---
id: computing-software.software-engineering.go.govulncheck-and-dependency-upgrades
name: govulncheck-and-dependency-upgrades
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-modules, govulncheck, vulnerability-scanning, go-get-u, go-mod-tidy, minimal-version-selection, toolchain-directive, dependency-updates, go-security, go-version-upgrade]
level: practitioner
status: verified
description: "Find reachable Go vulnerabilities with govulncheck, upgrade dependencies and the toolchain safely under minimal version selection, and keep go.mod tidy."
sources: ["https://go.dev/doc/security/vuln/", "https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck", "https://go.dev/ref/mod#minimal-version-selection", "https://go.dev/doc/toolchain"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# govulncheck and dependency upgrades

**Goal:** fix the vulnerabilities your code actually reaches, and upgrade dependencies
predictably.

## govulncheck
```bash
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...                 # source mode: call-graph reachability
govulncheck -mode=binary ./app    # scan a built binary
govulncheck -show verbose ./...   # also list imported-but-unreachable vulns
```
Source mode reports a vuln only if your code calls the vulnerable symbol, which keeps
noise low compared with manifest scanners. It also checks the Go standard library for
your toolchain version - many findings are fixed by a Go patch release.
CI: `golang/govulncheck-action` or plain `govulncheck ./...` (exit code 3 when it finds reachable vulnerabilities, 0 when clean).

## Upgrading
```bash
go list -m -u all                     # what has updates
go get example.com/lib@v1.8.2         # one module, exact version
go get -u ./...                       # all direct+indirect to latest minor/patch (can be big)
go get -u=patch ./...                 # patch-only, safer
go mod tidy                           # prune unused, add missing
```
Under minimal version selection, the build uses the MAX of the minimums required by
everyone, never "latest" automatically, so builds are reproducible without a lockfile.
Upgrading one dependency can raise transitive ones; review the go.mod/go.sum diff.
`go mod why -m example.com/x` and `go mod graph` explain why something is present.

## The toolchain
```
go 1.23.0            // minimum language version for this module
toolchain go1.23.4   // preferred toolchain when running go commands here
```
With `GOTOOLCHAIN=auto` (default), the `go` command uses a newer toolchain, downloading it if needed, when the main module's `go`/`toolchain` line is newer than the installed one. A dependency's `go` line does not do this by itself: building with a dependency that needs a newer `go` fails with `module ... requires go >= X` until `go get`/`go mod tidy` raises the main module's `go` line (which then switches the toolchain). So raising the `go` line in a LIBRARY forces that bump on all its users; be conservative there.

## Automation
Dependabot/Renovate support gomod; group minor/patch updates weekly, security updates
immediately. Always run `go test ./...` and `govulncheck` on the PR.

## Verify
- [ ] `govulncheck ./...` exits 0 in CI.
- [ ] `go mod tidy && git diff --exit-code go.mod go.sum` passes in CI.

## Checked
2026-10-21 on Go 1.27.3 and 1.22.5 (Windows), govulncheck v1.9.0 with the live vuln.go.dev DB: against a scratch module pinned to x/text v0.3.7 and yaml.v2 v2.2.2, `govulncheck ./...` printed 3 reachable vulns with call traces and exited 3; `-show verbose` added Package Results and Module Results sections; `-mode=binary` on the built exe gave the same summary; `go list -m -u all` listed updates; `go get -u=patch ./...` moved x/text to v0.3.8 and yaml.v2 to v2.2.8 only and govulncheck then exited 0; `go mod why -m` and `go mod graph` ran. Toolchain: a dependency whose go.mod says `go 1.25` made `go build` in a `go 1.21` module fail with `requires go >= 1.25` (also with GOTOOLCHAIN=local), while `go mod tidy` switched toolchains, downloaded Go 1.26.10/1.25.0 and raised the main module's go line to 1.25; GOTOOLCHAIN defaults to auto per https://go.dev/doc/toolchain; `golang/govulncheck-action` exists (GitHub API, not archived); Dependabot's ecosystem name is `gomod` (dependabot-core README).
