---
id: computing-software.cloud-infrastructure-engineering.zot.security-posture-hardening
name: security-posture-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, hardening, security-posture, unprivileged-process, outbound-tls, ca-trust-store]
level: advanced
status: docs-checked
description: "Zot's build-time and runtime hardening: PIE, minimal builds, unprivileged process, auth choices, outbound TLS trust store hygiene and timeouts."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/security-posture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Build time:
- The binary is built PIE so ASLR applies.
- Conditional builds separate core Distribution Spec code from extensions. Minimal = core only; full = minimal plus all extensions. Choose with `make EXTENSIONS=search binary`.
- CI/CD aims at OpenSSF practices: code-owner review on every PR, unit, functional and integration tests, quality and style checks, performance regression checks and vulnerability scans of binaries.

Runtime:
- Zot does not need root; run it under a separate user and group ID.
- Enable an authentication mechanism (htpasswd, LDAP, mTLS or token) and then access control per repository and action.
- Read and write timeouts (`http.readTimeout`, `http.writeTimeout`, default 60s) guard against slow clients; `0` disables them.
- Keep TLS verification on for upstream sync and HTTPS event sinks; maintain trust stores and remove distrusted roots rather than bypass verification.

Trust-store note on the page: an eMudhra incident led Debian to drop the `emSign ECC Root CA - G3` and `AAA Certificate Services` roots; update older trust stores or rebuild custom images with a corrected bundle. Zot's container build copies the CA bundle from the builder image, so updating only the Distroless base may not fix the final image. Do not reintroduce the affected roots via custom certificates.

Zot also supports security scanning of stored container images. Report security issues per SECURITY.md in the repository.

## Checked

Whole page read. Dropped the unsupported claim that scanning is the search CVE feature.

Method: docs-checked 2026-11-09 against zot docs articles/security-posture.md (read in full).
