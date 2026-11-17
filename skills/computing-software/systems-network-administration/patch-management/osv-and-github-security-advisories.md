---
id: computing-software.systems-network-administration.patch-management.osv-and-github-security-advisories
name: osv-and-github-security-advisories
category: computing-software
field: systems-network-administration
product: patch-management
tags: [osv, ghsa, vulnerability-intelligence, osv-scanner, open-source, security-advisories]
level: practitioner
status: docs-checked
description: "Use OSV.dev and GitHub Security Advisories to find vulnerable open-source packages: OSV API queries, osv-scanner on lockfiles and SBOMs, GHSA vs CVE IDs and ecosystem versions."
sources:
  - https://osv.dev/
  - https://google.github.io/osv-scanner/
  - https://docs.github.com/en/code-security/security-advisories/working-with-global-security-advisories-from-the-github-advisory-database/about-the-github-advisory-database
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSV and GitHub Security Advisories

NVD keys on CPE (vendor/product), which maps poorly to package ecosystems. **OSV** keys on
`ecosystem + package + version range` (PyPI, npm, Maven, Go, crates.io, Debian, Alpine,
Ubuntu, ...), aggregating GHSA, PyPA, RustSec, Go vulndb, distro advisories.

## IDs
- `GHSA-xxxx-xxxx-xxxx`: GitHub advisory; reviewed ones carry affected ranges and aliases.
- `CVE-...`: may be an alias of a GHSA/OSV record.
- `DSA-`/`DLA-` (Debian advisories converted by OSV.dev) and the other database prefixes defined in the OSV schema.
Deduplicate on `aliases`.

## Query the API
```sh
curl -s -d '{"package":{"name":"jinja2","ecosystem":"PyPI"},"version":"2.11.2"}' https://api.osv.dev/v1/query | jq '.vulns[] | {id, aliases, summary}'
curl -s https://api.osv.dev/v1/vulns/<id> | jq '.affected[].ranges'
```
Batch: `POST /v1/querybatch` with many packages.

## Scan projects and images
```sh
osv-scanner scan source -r .                  # scans a directory recursively (source is the default subcommand)
osv-scanner scan image registry.example/app:1.4.2
osv-scanner scan source -r . --format json > osv.json
```
GitHub-hosted code: Dependabot alerts use GHSA directly; `gh api /repos/{owner}/{repo}/dependabot/alerts`.

## Using it in patch management
- Server packages from distro repos: prefer the **distro** advisory (Debian/Ubuntu/RHEL
  backport fixes without version bumps). OSV includes Debian/Ubuntu/Alpine data with
  distro versions.
- Application dependencies: OSV/GHSA are authoritative; the fix is a dependency bump and
  rebuild, owned by the app team; track via the same SLA.
- Combine with EPSS/KEV for priority.

## Gotchas
- Unreviewed GHSA entries may lack ranges; treat as needing manual check.
- Version range semantics are ecosystem-specific (SEMVER vs ECOSYSTEM ordering); don't
  compare strings.

## Verify
Scanner results match known test cases (e.g. an intentionally old lockfile shows expected
GHSAs); findings flow into tickets with aliases deduplicated.

## Checked
Date: 2026-10-27. Documentation checked: OSV API pages (`POST /v1/query` with package name and ecosystem plus version, `POST /v1/querybatch`, `GET /v1/vulns/{id}`), OSV data sources page (aggregated databases, Debian and Alpine conversions, Ubuntu and other ecosystems covered), OSV schema (database prefixes, DSA/DLA), OSV-Scanner usage page (`scan`, `scan source`, `scan image`, `--format json`), GitHub Advisory Database page (GitHub-reviewed advisories), GitHub REST `GET /repos/{owner}/{repo}/dependabot/alerts`. Removed `--sbom`, the ID prefixes the schema pages did not confirm and the hard-coded advisory ID.

Method: documentation only; no commands were run.
