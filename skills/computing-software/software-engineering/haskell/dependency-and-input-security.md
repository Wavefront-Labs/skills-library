---
id: computing-software.software-engineering.haskell.dependency-and-input-security
name: dependency-and-input-security
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, supply-chain, cabal-audit, hackage-security, input-validation, injection, tls, crypton, secrets, cabal-plan, sbom, dependency-and-input-security]
level: practitioner
status: draft
description: "Secure Haskell services: pin and review dependencies (freeze files, index-state), validate input with parsers, parametrised queries, TLS and crypto library choices."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dependency and input security

**Goal:** reduce supply-chain and injection risk in Haskell programs.

## Supply chain
- Pin versions: `cabal.project.freeze`, `index-state`, Stack lock files. Review upgrades via `cabal outdated` and changelogs.
- Hackage uses signed index metadata (TUF-style, `hackage-security`); cabal verifies the index. Packages themselves are not reviewed, so check maintainers and reverse dependencies.
- Template Haskell, custom `Setup.hs` (`build-type: Custom`) and `c-sources` execute code at build time: inspect them for new dependencies.
- Generate a dependency list: `cabal build --dry-run --verbose=2`, `cabal-plan`, or `cabal freeze`; use as SBOM input. Vulnerability advisories: Haskell Security Advisory DB (haskell/security-advisories on GitHub) with `cabal-audit` (check current tool name and status).
- Prefer small, maintained libraries; avoid unmaintained crypto.

## Input handling
- Parse into types at the boundary (`aeson` into records, `megaparsec`), reject, do not sanitise.
- SQL: parameterised queries only (`postgresql-simple` `query conn "... ?" (Only x)`, `persistent`/`esqueleto`, `hasql`). Never build SQL with `++` or `printf`.
- HTML: use an escaping templating library (`blaze-html`, `lucid`, `shakespeare`); JSON via aeson.
- Shell: `System.Process.proc "cmd" [args]` (no shell) rather than `shell "string"`.
- Paths: normalise with `System.FilePath` and reject `..`; use `makeRelative`, check the canonicalised path stays under the root (`canonicalizePath`).
- Resource limits: bound request size (warp `setMaxTotalHeaderLength`, body limits), use `timeout`, and bounded queues.

## Crypto and TLS
`crypton` (maintained fork of `cryptonite`), `tls`/`crypton-connection`/`http-client-tls` for TLS; `bcrypt`/`scrypt`/`argon2` style password hashing (verify current maintained packages); get randomness from `crypton`/`entropy`, not `System.Random`.

## Gotchas
- `Read` on untrusted input can be slow and exponential; use proper parsers.
- Lazy IO and unbounded `ByteString` reads allow memory DoS.
- `show` of secrets in logs; use opaque newtypes with a redacting Show instance.

## Self-check
- [ ] No string-built SQL or shell commands (`grep -rn "shell \"" src`).
- [ ] Secrets never appear in logs or exception messages.
