---
id: computing-software.software-engineering.go.cross-compilation-and-build-tags
name: cross-compilation-and-build-tags
category: computing-software
field: software-engineering
product: go
tags: [go, go-tooling, go-build, cross-compilation, build-tags, cgo, goos-goarch, go-build-toolchain, go-reproducible-builds]
level: practitioner
status: gated
description: "Cross-compile Go binaries for any OS/arch with GOOS/GOARCH, handle cgo, use build constraints and file suffixes for platform code, and build multi-arch containers."
sources:
  - https://go.dev/doc/install/source#environment
  - https://pkg.go.dev/cmd/go#hdr-Build_constraints
  - https://pkg.go.dev/cmd/cgo
  - https://docs.docker.com/build/building/multi-platform/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cross-compilation and build tags

**Goal:** produce binaries for Linux, macOS, Windows on amd64 and arm64 from one machine, and keep platform-specific code clean.

## 1. Cross-compile
```bash
GOOS=linux   GOARCH=arm64 go build -o dist/app-linux-arm64 ./cmd/app
GOOS=windows GOARCH=amd64 go build -o dist/app-windows-amd64.exe ./cmd/app
GOOS=darwin  GOARCH=arm64 go build -o dist/app-darwin-arm64 ./cmd/app
go tool dist list                    # all supported GOOS/GOARCH pairs
GOARM64=v8.2 / GOAMD64=v3            # microarchitecture levels for faster code on newer CPUs
```
Pure Go code cross-compiles with no extra toolchain.

## 2. cgo changes everything
- `CGO_ENABLED` defaults to 1 for native builds only when a C compiler is found on PATH (or `CC` is set); it defaults to 0 when cross-compiling or when no compiler is found (`go doc cmd/cgo`; confirmed on a Windows host with no gcc: `go env CGO_ENABLED` printed 0). Set it explicitly in CI.
- `CGO_ENABLED=0` produces static binaries (ideal for `scratch`/distroless), using the pure-Go DNS resolver and `os/user`.
- Packages needing cgo (`mattn/go-sqlite3`, some GUI/crypto libs) need a cross C toolchain: `CC=aarch64-linux-gnu-gcc`, `zig cc -target aarch64-linux-musl`, or build per platform in CI. Prefer pure-Go alternatives (`modernc.org/sqlite`). (gated: unconfirmed, source is paywalled or blocked; no C cross-toolchain was available to run these)

## 3. Build constraints
File suffixes apply automatically: `x_linux.go`, `x_windows_amd64.go`, `x_test.go`.
Expression constraints at the top of the file (before `package`, followed by a blank line):
```go
//go:build linux && (amd64 || arm64) && !nocgo

package sysinfo
```
Custom tags:
```go
//go:build integration
```
```bash
go test -tags=integration ./...
go build -tags=netgo,osusergo .     # force pure-Go net and user lookups
go list -f '{{.GoFiles}}' -tags=integration ./pkg/...   # which files a tag set includes
```
`// +build` lines are obsolete; `gofmt` adds/maintains `//go:build`.

## 4. Platform abstraction
Define an interface or a function in a shared file and implement it per platform:
```
fs_unix.go      //go:build unix
fs_windows.go
```
Ensure every supported platform has an implementation, or provide a `fs_other.go` with `//go:build !unix && !windows` returning `errors.ErrUnsupported`.

## 5. Multi-arch containers
```dockerfile
FROM --platform=$BUILDPLATFORM golang:1.24 AS build
ARG TARGETOS TARGETARCH
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH go build -trimpath -ldflags="-s -w" -o /app ./cmd/app
FROM gcr.io/distroless/static
COPY --from=build /app /app
ENTRYPOINT ["/app"]
```
`docker buildx build --platform linux/amd64,linux/arm64 -t org/app:1.0 --push .` builds natively-fast cross binaries instead of emulating the compiler under QEMU. (gated: unconfirmed, source is paywalled or blocked; the Dockerfile and buildx command were not run, the Docker daemon was unavailable)

## Gotchas
- `GOOS=windows` binaries need the `.exe` suffix to be runnable by double click / some tools.
- Build tags that exclude every file in a package give "build constraints exclude all Go files".
- Test cross-compiled binaries on the real target (or QEMU) at least in CI; syscall differences surface only at runtime.

## Verify
- CI matrix builds all targets with `go build`, `file dist/*` shows correct formats, and `go vet` runs with each tag set used in production.
