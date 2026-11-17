---
id: computing-software.software-engineering.go.workspaces-and-replace-directives
name: workspaces-and-replace-directives
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-modules, go-work, replace-directive, multi-module, local-development, monorepo, go-work-sum]
level: practitioner
status: verified
description: "Develop several Go modules together with go work workspaces, use replace directives correctly, and avoid leaking local replaces into releases."
sources: ["https://go.dev/doc/tutorial/workspaces", "https://go.dev/ref/mod#workspaces", "https://go.dev/ref/mod#go-mod-file-replace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workspaces and replace directives

**Goal:** edit a library and the service that uses it at the same time, without
committing broken `replace ../lib` lines.

## go work (Go 1.18+)
```bash
go work init ./service ./lib       # creates go.work
go work use ./another-module       # add more
go work sync                       # push workspace build list back into each go.mod
```
```
// go.work
go 1.23
use (
    ./service
    ./lib
)
```
Inside the workspace, imports of `example.com/lib` resolve to `./lib` source. Each
module's `go.mod` stays unchanged.

### Commit go.work or not?
- Usually NOT for repos where modules are released independently (add `go.work` and
  `go.work.sum` to `.gitignore`); CI should build each module against its real
  requirements.
- In a monorepo where modules always move together, committing it can be fine; then CI
  must also test with `GOWORK=off` to prove each module builds on its own.
`GOWORK=off go build ./...` disables the workspace for one command.

## replace directives
```
replace example.com/lib => ../lib                    // local path (no version)
replace example.com/lib v1.2.3 => example.com/fork/lib v1.2.4-fix   // fork
```
- `replace` only applies in the MAIN module; replaces in dependencies are ignored. So a
  library's replace does nothing for its users, and a local path replace in a library
  breaks nobody but confuses everyone.
- Local path replaces in a committed go.mod break CI and other machines. Use go.work for
  local dev instead.
- Forks: replace to a published fork with a real version, and track removing it.
- `exclude` blocks specific bad versions; prefer upstream `retract`.

## Gotchas
- `go mod tidy` operates per module and ignores go.work; run it in each module.
- Tools that don't understand workspaces (older linters) may resolve differently;
  check `go env GOWORK`.
- Vendoring with workspaces requires `go work vendor` (Go 1.22+).

## Verify
- [ ] `git grep -n "=> \.\./" -- '*go.mod'` returns nothing in release branches.
- [ ] CI runs with `GOWORK=off` per module.
