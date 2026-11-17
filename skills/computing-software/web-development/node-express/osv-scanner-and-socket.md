---
id: computing-software.web-development.node-express.osv-scanner-and-socket
name: osv-scanner-and-socket
category: computing-software
field: web-development
product: node-express
tags: [osv-scanner, socket-dev, dependency-scanning, vulnerability-scanning, supply-chain, sca]
level: practitioner
status: docs-checked
description: "Scanning dependencies beyond npm audit: OSV-Scanner for multi-ecosystem CVEs with ignore files and fixes, and Socket-style behavioural analysis of new packages in PRs."
sources:
  - https://google.github.io/osv-scanner/
  - https://google.github.io/osv-scanner/configuration/
  - https://google.github.io/osv-scanner/github-action/
  - https://github.com/SocketDev/socket-cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSV-Scanner and Socket

Two different questions: "does anything I use have a **known vulnerability**?" (CVE scanners) and "is this new package **malicious or risky**?" (behaviour scanners).

## 1. OSV-Scanner (known vulnerabilities, all ecosystems)
```bash
osv-scanner scan source -r .                       # finds lockfiles: npm, pnpm, yarn, pip, poetry, Gemfile.lock, go.sum...
osv-scanner scan image ghcr.io/acme/web:1.4.2      # container image layers
osv-scanner fix --strategy=in-place -L package-lock.json   # guided remediation (experimental)
```
Ignore with justification and expiry:
```toml
# osv-scanner.toml
[[IgnoredVulns]]
id = "GHSA-xxxx-xxxx-xxxx"
ignoreUntil = 2026-12-31
reason = "Only affects server-side rendering path we do not use"
```
CI: `google/osv-scanner-action` workflows (PR diff mode reports only newly introduced vulns). Data comes from the OSV.dev database. SBOM files are recognised by file name following the SBOM spec (for example `*.spdx.json`); see the v2 migration guide.

## 2. Socket (behavioural / malware signals)
- CLI wrapper: `socket npm install`, `socket pnpm install` and `socket yarn add <package>` run the install through Socket Firewall, which blocks known-malicious packages before they are installed.
- `socket scan create` scans the project dependencies.
- Decide in advance which findings block a PR and which only warn.

## 3. Operating it
- Triage by reachability and exposure: dev-only tooling CVEs (e.g. ReDoS in a build tool) rarely matter for production; runtime web-facing deps do.
- Fix by updating the direct dependency; `overrides` (npm and pnpm) or `resolutions` (yarn) for transitive pins, with a comment and a ticket to remove.
- Track mean time to remediate per severity.

## Verify
- [ ] PRs introducing a vulnerable or flagged package show a failing check with the reason; ignores carry expiry dates.

## Checked

2026-10-25 against the OSV-Scanner docs (google/osv-scanner main) and the Socket CLI README (SocketDev/socket-cli, 2026-10-15). Confirmed: osv-scanner scan source -r, scan image, and fix --strategy=in-place -L syntax; guided remediation is experimental; osv-scanner.toml uses [[IgnoredVulns]] with id, ignoreUntil and reason, and aliases are ignored too; the PR workflow reports only vulnerabilities introduced by the pull request; OSV-Scanner is a frontend to the OSV.dev database; socket npm, socket pnpm and socket yarn run installs through Socket Firewall which blocks known-malicious packages.

Method: documentation only; no commands were run.
