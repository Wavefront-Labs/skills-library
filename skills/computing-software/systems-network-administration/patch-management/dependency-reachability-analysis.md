---
id: computing-software.systems-network-administration.patch-management.dependency-reachability-analysis
name: dependency-reachability-analysis
category: computing-software
field: systems-network-administration
product: patch-management
tags: [reachability-analysis, sca, dependency-vulnerabilities, govulncheck, patch-prioritisation, vulnerability-management]
level: practitioner
status: draft
description: "Prioritise vulnerable dependencies by reachability: run govulncheck and call-graph SCA tools, interpret reachable vs unreachable, and record VEX statements without hiding risk."
sources:
  - https://go.dev/doc/security/vuln/
  - https://openvex.dev/
  - https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reachability analysis for dependency vulnerabilities

**Problem:** SCA tools flag every CVE in every transitive package. Most are in functions your code never calls. Reachability narrows the list so patching effort lands where it matters.

## Levels of reachability
1. **Package present** (manifest/lockfile) - noisiest.
2. **Module imported** - package is actually loaded.
3. **Vulnerable symbol reachable** - call graph from your entry points reaches the affected function.
4. **Exploitable in config** - reachable and attacker-controlled input gets there.

## Go: govulncheck (symbol level, free)
```sh
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...            # reports only vulns whose symbols are called
govulncheck -show verbose ./...   # also lists imported-but-not-called
govulncheck -mode binary ./app    # scan a built binary
```
Output "Your code is affected by N vulnerabilities" lists call stacks as evidence.

## Other ecosystems
- Commercial SCA (Snyk, Endor Labs, Semgrep Supply Chain, Contrast) provide function-level reachability for Java, JS, Python with varying accuracy.
- Python/JS dynamic dispatch, reflection and plugins defeat static call graphs; treat "unreachable" as lower confidence there.

## Recording the decision (VEX)
```json
{"@context":"https://openvex.dev/ns/v0.2.0","statements":[{
 "vulnerability":{"name":"CVE-2023-XXXX"},"products":[{"@id":"pkg:oci/app@sha256:..."}],
 "status":"not_affected","justification":"vulnerable_code_not_in_execute_path",
 "impact_statement":"govulncheck shows no call path to affected function"}]}
```
Ship VEX alongside SBOM so scanners and customers can suppress with justification.

## Policy
- Reachable + KEV/high EPSS -> patch within the critical SLA.
- Unreachable -> still upgrade in the next routine dependency bump; reachability can change with any code change.
- Re-run reachability in CI on every build; VEX statements need an expiry or revalidation date.

## Verify
Sample unreachable findings manually (grep for the symbol, check reflection use); CI fails when a reachable critical appears.
