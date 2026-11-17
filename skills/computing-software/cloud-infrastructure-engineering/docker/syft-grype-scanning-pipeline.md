---
id: computing-software.cloud-infrastructure-engineering.docker.syft-grype-scanning-pipeline
name: syft-grype-scanning-pipeline
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, grype, syft, syft-grype, grype-db, vulnerability-scanning, sbom, cve]
level: practitioner
description: "Generate an SBOM once with syft and scan it with grype (fail-on, only-fixed, ignore rules), managing the grype vulnerability DB updates and staleness."
sources: ["https://github.com/anchore/grype", "https://github.com/anchore/syft", "https://github.com/anchore/grype/blob/main/cmd/grype/cli/options/database.go", "https://github.com/anchore/grype/blob/main/cmd/grype/cli/options/grype.go"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# syft -> grype scanning pipeline

## Why split SBOM and scan
The SBOM is fixed per image digest; vulnerabilities change daily. Generate the SBOM at build
time, store it, and rescan the SBOM (seconds, no image pull) whenever the DB updates.

```sh
syft registry.example.com/app:1.4.0 -o syft-json=sbom.syft.json -o spdx-json=sbom.spdx.json
grype sbom:./sbom.syft.json --fail-on high --only-fixed -o table
grype sbom:./sbom.syft.json -o sarif > grype.sarif           # GitHub code scanning
grype registry.example.com/app:1.4.0                         # or scan the image directly
```
- `--fail-on <severity>` exits 1 at or above that severity.
- `--only-fixed` hides vulns with no fix available (actionable list); `--only-notfixed` the inverse.
- Grype scans an image, a directory (`grype ./my-project`) or an SBOM (`grype sbom:./sbom.json`);
  an SBOM can also be piped in on stdin. On Linux `--from containers-storage` reads local Podman
  or Buildah images.

## Ignore rules
```yaml
# .grype.yaml
ignore:
  - vulnerability: CVE-2023-12345
    reason: "not reachable: feature disabled"
  - vulnerability: GHSA-xxxx-yyyy-zzzz
    package: { name: golang.org/x/net, type: go-module }
  - fix-state: wont-fix
```
Keep a `reason` - auditors ask. Rule fields include `vulnerability`, `namespace`, `fix-state` (fixed, not-fixed, wont-fix, unknown), `match-type`, `reason`, `include-aliases` and `package` (name, version, language, type, location, upstream-name); a match must meet all fields of a rule. Grype also accepts OpenVEX documents via `--vex`.

## The DB
```sh
grype db status          # built date, schema
grype db update
grype db check           # reports whether a database update is available
```
- `max-allowed-built-age` (config `db.max-allowed-built-age`, default 120h, five days) is the maximum age of the vulnerability database; with `db.validate-age` on, an older database is rejected, which can break CI on an offline runner.
- `db.cache-dir` sets where the database is stored; persist it in the CI cache to avoid a download per job (the source notes the DB was about 156 MB in April 2024).
- `db.auto-update: false` stops the update check on each run, for deterministic re-runs against a pinned DB. Environment variables use the `GRYPE_DB_` prefix with the same names, for example `GRYPE_DB_AUTO_UPDATE`.

## Gotchas
- Results differ from Trivy/Scout: different data sources and matching. Pick one gate, use
  others for second opinions.
- SBOM-based scans only know the packages the SBOM lists.

## Verify
Introduce a known-vulnerable package version; the job fails with `--fail-on high`; after
bumping, the same SBOM rescan passes.

## Checked
Documentation release: anchore/grype v0.121.0 (README, cmd/grype/cli/options/*.go descriptions) and anchore/syft README, checked 2026-10-26.
Confirmed: `--fail-on` (negligible, low, medium, high, critical; exit code 1), `--only-fixed`, `--vex`, `grype sbom:./sbom.json`, `syft -o spdx-json=` and `syft-json` format id, `-o sarif`, `db check`, ignore-rule fields and fix states, `max-allowed-built-age` default 120h, `cache-dir`, `auto-update`.
Removed as unsupported: the exit code 100 claim, the source-scheme list, `~/.cache/grype/db` path, the ~100 MB figure (replaced by the documented 156 MB note), and the Go build-info and cataloger claims.
Method: documentation only; no commands were run.
