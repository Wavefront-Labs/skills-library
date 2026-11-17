---
id: computing-software.software-engineering.go.major-versions-and-semantic-import-versioning
name: major-versions-and-semantic-import-versioning
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-modules, go-mod, semantic-import-versioning, major-version, v2-module, incompatible, retract, gorelease, go-retract-deprecate]
level: advanced
status: verified
description: "Release breaking changes in a Go module correctly: /v2 module paths, major-branch vs subdirectory layout, +incompatible, retract directives and checking API compatibility."
sources: ["https://go.dev/doc/modules/major-version", "https://go.dev/ref/mod#major-version-suffixes", "https://go.dev/blog/v2-go-modules", "https://go.dev/ref/mod#go-mod-file-retract"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Major versions and semantic import versioning

**Goal:** ship v2 of a Go library without breaking v1 users, and so that `go get` picks
it up at all.

## The rule
"If an old package and a new package have the same import path, the new package must
be backwards compatible with the old package." So from v2 on, the major version is
PART OF THE MODULE PATH:
```
module github.com/acme/client/v2
```
Importers write `import "github.com/acme/client/v2"`. v0 and v1 have no suffix.
Tagging `v2.0.0` without changing the module path makes Go refuse it (or, for repos
without go.mod, mark it `+incompatible`).

## Two layouts
1. **Major branch**: the "most straightforward" approach in the go.dev major-version guide. Branch (or
   switch main), update the `go.mod` path to `/v2`, update all internal imports to `/v2`, tag
   `v2.0.0`. v1 fixes continue on a `v1` branch. Tools that are not version-aware (the `go`
   command in GOPATH mode) may not tell the majors apart if v2 lives on the default branch.
2. **Major subdirectory**: put the code in `v2/` with its own `go.mod`. The 2019 Go blog
   recommends this as long as you have users in GOPATH mode: file paths match what pre-modules
   tools expect, and all majors can be developed side by side.

Steps for (1):
```bash
go mod edit -module github.com/acme/client/v2
# rewrite imports of own packages
find . -name '*.go' -exec sed -i -E 's#"github.com/acme/client(/|")#"github.com/acme/client/v2\1#g' {} +   # also catches the root import (no trailing slash)
go build ./... && go test ./...
git tag v2.0.0 && git push origin v2.0.0
```

## Avoiding v2 when possible
Each major version is effectively a new module and fragments the ecosystem. Prefer
additive changes: new functions, options structs, functional options, deprecate with a
`// Deprecated:` paragraph (some tools warn, and pkg.go.dev hides the docs by default, per go.dev/doc/comment). Staying on v0 signals
"no compatibility promise" but doesn't remove the problem for users.

## Retracting bad releases
```
// go.mod (released in a newer version)
retract v1.4.1 // panics on nil config; use v1.4.2
retract [v1.5.0, v1.5.3]
```
`go get -u` and `go list -m -versions` skip retracted versions (an explicit `go get mod@retracted` still works but prints a notice), and `go list -m -retracted` shows them. Retraction
needs a NEW release containing the directive.

## Checking compatibility
`gorelease` (golang.org/x/exp/cmd/gorelease) compares your API with the last tag and
suggests the next version; `apidiff` does the raw comparison. Run in CI before tagging.

## Verify
- [ ] `go list -m github.com/acme/client/v2@v2.0.0` resolves via the proxy.
- [ ] A scratch module can import v1 and v2 side by side and build.
- [ ] gorelease reports no unexpected incompatible changes for minor releases.

## Checked
2026-10-21 on Go 1.27.3 (Windows), using a local file:// module proxy for example.com modules plus the real proxy for one +incompatible example: a module that imports both `example.com/acme/client` (v1.4.3) and `.../v2` (v2.0.0) built and ran; a v2.0.0 zip whose go.mod keeps the unsuffixed path fails with `invalid version: should be v0 or v1, not v2`; `go list -m -versions` hides the retracted v1.4.1 and `-retracted` shows it; `go get ...@v1.4.1` prints a retraction notice and `go get -u` moved to v1.4.3 (the version carrying the directive); `go list -m ...@v3.2.0+incompatible` resolves for github.com/dgrijalva/jwt-go; `gorelease -base=v1.4.2` reported 'V: removed' as incompatible and refused to suggest a version against a non-latest base; `go mod edit -module` works but the skill's sed line missed the root-package import `"github.com/acme/client"` (no trailing slash), which then failed to build. `apidiff` installs from golang.org/x/exp/cmd/apidiff. The import compatibility rule quote and the layout advice were re-read from https://go.dev/blog/v2-go-modules and https://go.dev/doc/modules/major-version (the blog recommends the subdirectory layout while GOPATH-mode users exist; the doc calls branching the most straightforward). Deprecation and retract rules (a retracting version must be higher than the others) are from https://go.dev/doc/comment and https://go.dev/ref/mod. The sed line was re-run on a scratch module after the fix and the module built.
