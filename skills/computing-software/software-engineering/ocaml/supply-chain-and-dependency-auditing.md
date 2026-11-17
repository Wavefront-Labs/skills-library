---
id: computing-software.software-engineering.ocaml.supply-chain-and-dependency-auditing
name: supply-chain-and-dependency-auditing
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, supply-chain-opam, opam-lock, supply-chain, dependency-audit, ocaml-advisories]
level: advanced
status: draft
description: "Reproduce builds with opam lock files and pinned git commits, review dependency growth, and check opam-repository advisories."
sources: ["https://ocaml.org/manual/api/", "https://ocaml.org/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dependency hygiene

```bash
opam lock .                       # writes <pkg>.opam.locked
opam install . --locked --deps-only
opam list --required-by=mypkg --recursive --installed
```

## Notes
- Commit `.opam.locked` files for applications (not libraries) for reproducible builds.
- Pin git dependencies to a commit hash, not a branch.
- opam-repository holds security advisories in `security-advisories/` (OCSF-style YAML) (unconfirmed layout); tools like `opam-audit` consume them (unconfirmed name).
- Review new dependencies' maintainers and transitive closure before adding.
- `opam install --dry-run` shows what would change.
- Dune package management (`dune pkg lock`) is an alternative resolver in recent dune versions (unconfirmed maturity).

## Self-check
- [ ] A fresh clone installs with `--locked` and builds identically.
