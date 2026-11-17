---
id: computing-software.software-engineering.go.project-layout-and-embed
name: project-layout-and-embed
category: computing-software
field: software-engineering
product: go
tags: [go, go-tooling, go-build, go-project-layout, go-embed, internal-packages, cmd-directory, go-embed-fs, go-design-style, go-internal-packages]
level: practitioner
status: verified
description: "Lay out Go modules sensibly (cmd/, internal/, package-by-feature), and ship static assets, templates and migrations inside binaries with go:embed."
sources:
  - https://go.dev/doc/modules/layout
  - https://pkg.go.dev/embed
  - https://go.dev/doc/go1.4#internalpackages
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Go project layout and embed

**Goal:** a structure that matches Go's import rules and scales from one binary to several, and single-file deployments with embedded assets.

## 1. Start small
- A library: package at the module root (`github.com/acme/money` -> `money.go`).
- One command: `main.go` at the root is fine.
Do not pre-create `pkg/`, `util/`, `models/`; empty layers and grab-bag packages are the main layout smell.

## 2. Growing layout (official guidance)
```
go.mod
cmd/
  api/main.go            # thin: parse flags/config, wire dependencies, run
  worker/main.go
internal/
  orders/                # package by feature/domain, not by technical layer
    service.go
    store_postgres.go
    http.go
  platform/postgres/
  platform/httpserver/
migrations/
web/
```
- `internal/` is enforced by the compiler: only code rooted at the parent of `internal` can import it. Put everything there unless you intend others to import it.
- Package names are short, lowercase, no underscores, and describe what they provide (`orders`, not `ordersservice`); avoid `util`, `common`, `helpers`.
- Avoid import cycles by depending on interfaces defined by the consumer, and keep `main` as the composition root.

## 3. go:embed
```go
import "embed"

// in a package that sits next to (or above) the files, e.g. migrations/embed.go (package migrations)
//go:embed *.sql
var migrations embed.FS

// in web/embed.go (package web): the path cannot reach outside the package directory
//go:embed dist
var webDist embed.FS

//go:embed version.txt
var versionTxt string
```
Serve embedded static files:
```go
sub, _ := fs.Sub(web.WebDist, "dist")   // exported var from package web
mux.Handle("GET /", http.FileServerFS(sub))       // Go 1.22+
```
Templates: `template.ParseFS(templatesFS, "templates/*.html")`. Migrations: goose/golang-migrate accept an `fs.FS`.

## 4. embed rules
- The directive must be directly above a package-level `var` of type `string`, `[]byte` or `embed.FS`, and the file must import `embed` (blank import for string/[]byte).
- Patterns are relative to the source file's directory and cannot contain `..` (build error `invalid pattern syntax`), so the embedding package must sit at or above the assets; the directive cannot be on a var with an initializer.
- Directories exclude files beginning with `.` or `_` unless you use the `all:` prefix (`//go:embed all:web/dist`).
- Embedded files are read-only and part of the binary size.

## Gotchas
- Front-end build outputs must exist before `go build`; generate them in CI (or commit a placeholder so `go vet` does not fail on a missing pattern).
- Changing an embedded file triggers a rebuild automatically (go tracks embedded files in the build cache).
- Deep `internal/` nesting can block legitimate sharing between commands; place shared code at `internal/` top level.

## Verify
- `go build ./...` succeeds from a clean clone after the asset build step, the binary serves static files with no files on disk beside it, and `go list -deps ./cmd/api | grep internal` shows no cross-feature cycles.

## Checked
2026-10-21 on Go 1.27.3 (Windows), scratch modules: `//go:embed ../../migrations/*.sql` from `cmd/api` fails with `invalid pattern syntax`, so assets must live at or below the embedding package's directory (the layout tree's root `migrations/` and `web/` need a small package of their own that holds the `go:embed` line); embedding a directory skipped `.hid`, `_u.txt` and `_hidden/` and `all:dist` included them; string and `[]byte` embeds worked; `http.FileServerFS(fs.Sub(...))` on a `GET /` mux served the files (`/index.html` redirects to `/`); a missing pattern fails build and vet with `no matching files found`; `go:embed` on a var with an initializer fails (`cannot apply to var with initializer`); editing an embedded file changed the next `go run` output; importing an `internal/` package from another module failed with `use of internal package ... not allowed`. Layout advice re-read from https://go.dev/doc/modules/layout (see below). Also ran: `goose.SetBaseFS(fs.FS)` and golang-migrate `iofs.New(fs.FS, dir)` both compile and accept an embedded/`fstest.MapFS` filesystem (migrations were not applied to a database).
