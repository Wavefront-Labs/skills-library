---
id: computing-software.devops-ci-cd.secrets-management.language-dependency-audits
name: language-dependency-audits
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, pip-audit, govulncheck, cargo-audit, vulnerability-scanning]
level: practitioner
status: gated
description: "Audit language dependencies in CI with native tools (npm audit, pip-audit, govulncheck, cargo audit/deny, bundler-audit) and handle exceptions, reachability and noise."
sources: ["https://pypi.org/project/pip-audit/", "https://go.dev/doc/security/vuln/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pip-audit, govulncheck, cargo audit and friends

Native auditors read lockfiles and query advisory databases (OSV, GitHub Advisory, RustSec, Go vulndb).

| Ecosystem | Command | Notes |
|---|---|---|
| npm | `npm audit --omit=dev --audit-level=high` | `npm audit signatures` verifies registry signatures/provenance (needs an installed tree: run after `npm ci`; `2 packages have verified registry signatures`). `npm audit` exits 1 on findings at or above the level (run on npm 10.8.2) |
| Python | `pip-audit -r requirements.txt --strict` / `pip-audit` in the venv | `--ignore-vuln ID` with a reason (run on pip-audit: `ignored 2` in the summary). `--strict` fails only when dependency collection fails; vulnerabilities give exit 1 regardless. |
| Go | `govulncheck ./...` | **call-graph reachability**: exit 3 only for vulns whose functions you call (run: `ParseAcceptLanguage` on x/text 0.3.6 flagged with a trace; the same module imported without calling it produced no finding for x/text), but the summary still counts the unreached ones; stdlib vulns depend on the installed Go toolchain |
| Rust | `cargo audit` / `cargo deny check advisories` | cargo-audit 0.22.2 exited 1 on `time 0.1.43` (RUSTSEC-2020-0071); cargo-deny 0.20.2 `ignore = [{ id = "...", reason = "..." }]` passed, and `expiry = "P30D"` (an ISO duration counted from advisory publication) is documented; also licenses/bans |
| Ruby | `bundle audit check --update` | (gated: unconfirmed, no Ruby here) |
| Java | OWASP Dependency-Check, `mvn org.owasp:dependency-check-maven:check` | NVD API key needed for speed (gated: unconfirmed, no Java here) |
| .NET | `dotnet list package --vulnerable --include-transitive` | (gated: unconfirmed, no .NET SDK here) |

## CI pattern
```yaml
- run: govulncheck ./...
- run: pip-audit --strict --progress-spinner off -r requirements.lock
- run: cargo deny check advisories
```
Run on PRs (block new high/critical) and on a nightly schedule against main (new advisories appear
without code changes).

## Exceptions
Each ignore has: advisory id, reason (not reachable / no fix / mitigated), owner, expiry date.
cargo-deny supports this natively; for others keep an `audit-exceptions.yaml` and a wrapper.

## Verify
- [ ] Adding a known-vulnerable version fails CI; nightly job opens issues for new advisories on main.
