---
id: computing-software.software-engineering.go.version-info-with-ldflags-and-buildinfo
name: version-info-with-ldflags-and-buildinfo
category: computing-software
field: software-engineering
product: go
tags: [go, go-tooling, go-build, ldflags, buildinfo, versioning, reproducible-builds, trimpath]
level: practitioner
status: verified
description: "Embed version, commit and build metadata into Go binaries with -ldflags -X or runtime/debug.ReadBuildInfo, and make builds reproducible with -trimpath and stamped VCS info."
sources:
  - https://pkg.go.dev/cmd/link
  - https://pkg.go.dev/runtime/debug#ReadBuildInfo
  - https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies
  - https://go.dev/blog/rebuild
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedding version info with -ldflags and debug.BuildInfo

**Goal:** every binary can tell you exactly what source and settings produced it (`app --version`, metrics labels, crash reports).

## 1. Free metadata: debug.ReadBuildInfo
Since Go 1.18 `go build` stamps module and VCS info automatically (when building from a Git checkout with `-buildvcs=auto`).
```go
import "runtime/debug"
func version() string {
    bi, ok := debug.ReadBuildInfo()
    if !ok { return "unknown" }
    var rev, dirty, when string
    for _, s := range bi.Settings {
        switch s.Key {
        case "vcs.revision": rev = s.Value
        case "vcs.modified": if s.Value == "true" { dirty = "-dirty" }
        case "vcs.time": when = s.Value
        }
    }
    return fmt.Sprintf("%s (%s%s, %s, %s)", bi.Main.Version, rev, dirty, when, bi.GoVersion)
}
```
`bi.Main.Version` is the module version for `go install module@v1.2.3` builds; Go 1.24+ also sets it from VCS for local builds: `v1.2.3` exactly on a tag, otherwise a pseudo-version such as `v1.2.4-0.<time>-<rev>`, with `+dirty` for a modified tree (Go 1.22 reports `(devel)`; both tested). Inspect any binary with `go version -m ./app`.

## 2. -ldflags -X for custom values
```go
package main
var (
    version = "dev"
    commit  = "none"
)
```
```bash
go build -ldflags "-X main.version=$(git describe --tags --always --dirty) -X main.commit=$(git rev-parse --short HEAD)" ./cmd/app
go build -ldflags "-X 'github.com/acme/app/internal/build.Version=v1.4.0'" ./cmd/app   # full import path for non-main packages
```
- Only package-level `string` variables (not constants, not initialised by function calls) can be set.
- A typo in the symbol path is silently ignored; check with `go version -m` or by printing.

## 3. Release flags
```bash
go build -trimpath -ldflags="-s -w -X main.version=$VERSION" ./cmd/app
```
- `-trimpath` removes local filesystem paths (reproducibility, no leaking `$HOME`).
- `-s -w` strip symbol table and DWARF (smaller; but no debugger symbols; panics still show stack traces).
- Avoid embedding build timestamps if you want bit-for-bit reproducible builds; use `vcs.time` (commit time) instead.

## 4. Tooling
GoReleaser's default ldflags are `-s -w -X main.version={{.Version}} -X main.commit={{.Commit}} -X main.date={{.Date}} -X main.builtBy=goreleaser` (docs: goreleaser.com/customization/builds/go/) and builds the matrix, checksums and SBOMs.

## Gotchas
- Docker builds copying source without `.git` produce no VCS stamps (the build still succeeds, even with `-buildvcs=true`, on Go 1.24); pass values via `-ldflags` build args or copy `.git`.
- With `-trimpath`, `go version -m` omits the `-ldflags` line (tested on Go 1.24), so do not use it to check `-X` values on such builds; print the value instead.
- `go run` and `go test` binaries do not include VCS stamps.
- Vendored or dirty working trees show `vcs.modified=true`; CI builds should be clean.

## Verify
- `./app --version` prints the tag and commit; `go version -m ./app` lists `vcs.revision` and `-trimpath` in build settings; two CI builds of the same commit have identical checksums.
