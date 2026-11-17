---
id: computing-software.software-engineering.go.injection-safe-queries-and-commands
name: injection-safe-queries-and-commands
category: computing-software
field: software-engineering
product: go
tags: [go, go-security, go-injection-safe, sql-injection, command-injection, os-exec, parameterized]
level: practitioner
status: draft
description: "Prevent SQL, command and template injection in Go: parameterised queries, identifier allow-lists, exec.Command without a shell, and html/template."
sources:
  - https://go.dev/doc/security/best-practices
  - https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Injection-safe queries and commands

**Goal:** untrusted text never becomes code.

**SQL:** values go through placeholders; identifiers (table/column/ORDER BY) come from an allow-list.

```go
cols := map[string]string{"name": "name", "created": "created_at"}
col, ok := cols[r.URL.Query().Get("sort")]
if !ok { col = "created_at" }
rows, err := db.QueryContext(ctx, "SELECT id,name FROM t WHERE org=$1 ORDER BY "+col, org)
```

**Commands:** pass arguments as separate strings, never `sh -c` with concatenation.

```go
cmd := exec.CommandContext(ctx, "convert", "--", userFile, "out.png") // "--" ends options
```

`exec.Command` does not invoke a shell, so metacharacters are inert, but a value starting with `-` can still be parsed as an option (argument injection); use `--` or validate. Resolve paths explicitly; since Go 1.19 `exec` refuses to run a binary found relative to the current directory (`ErrDot`).

**HTML:** `html/template` escapes by context; `template.HTML(userInput)` bypasses it, so never convert untrusted text. Use `text/template` only for non-HTML output.

## Gotchas
- `LIKE` patterns need escaping of `%` and `_` even with placeholders.
- ORMs and query builders still allow raw fragments; grep for `Raw(`/`Exec(` with `+`.
- Static analysis: `gosec` (G201/G202 SQL concatenation, G204 subprocess with variable).

## Verify
Run gosec in CI; add a test sending `' OR 1=1 --` and `; rm -rf` payloads and assert they are treated as data.
