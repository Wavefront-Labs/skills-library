---
id: computing-software.cloud-infrastructure-engineering.kubernetes.container-image-scanning-and-admission-gates
name: container-image-scanning-and-admission-gates
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, trivy, grype, clair, vulnerability-scanning, cve, severity-gating, admission-control, ci-cd, image-scanning, vex, exceptions, false-positive, sbom, distroless]
level: advanced
status: docs-checked
description: "CVE scanning with Trivy/Grype in CI and at admission: severity gates, exception/VEX handling, distroless images, and why runtime scanning catches what CI misses."
sources: ["https://github.com/aquasecurity/trivy/blob/main/docs/guide/references/configuration/cli/trivy_image.md", "https://github.com/aquasecurity/trivy/blob/main/docs/guide/configuration/filtering.md", "https://github.com/aquasecurity/trivy/blob/main/docs/guide/supply-chain/vex/index.md", "https://github.com/anchore/grype"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image vulnerability scanning and admission gating

**Goal:** catch known-vulnerable packages before they run, without the scan
either rubber-stamping everything (CRITICAL-only gates miss the long tail) or
blocking every deploy on CVEs nobody can fix yet. Signing/identity verification
is a different control, covered in
`computing-software.cloud-infrastructure-engineering.kubernetes.container-image-signing-and-verification`;
SBOM generation that scanners often consume is in
`computing-software.cloud-infrastructure-engineering.kubernetes.supply-chain-security-sbom-provenance`.

## 1. Where scanning happens, and why one place isn't enough
- **CI (build time)** — fail the pipeline before push. Catches it earliest, but
  only knows the CVE database as of build time; a package with no known CVE at
  build can have one disclosed the next day while the image sits in a registry
  untouched.
- **Registry (continuous)** — many registries can re-scan stored images against
  updated feeds (check what yours offers); this is what
  catches "safe when built, vulnerable now."
- **Admission (deploy time)** — re-check at the moment something is actually
  scheduled, via Kyverno/Gatekeeper calling into scan results or a dedicated
  scanner webhook. Closes the gap between "pushed 3 months ago" and "deploying
  today," which CI-time scanning alone cannot.
Treat these as layers, not alternatives — CI scanning alone lets an image rot in
the registry and get deployed stale; admission-only scanning with no CI gate
means every failed deploy is discovered late and expensively.

## 2. Trivy / Grype basics
```bash
trivy image --severity CRITICAL,HIGH --exit-code 1 --ignore-unfixed registry.example.com/app:1.2.3
grype registry.example.com/app:1.2.3 --fail-on high
```
- `--ignore-unfixed` (Trivy: show only vulnerabilities that have a fix) and `--only-fixed` (Grype: only
  fail on vulnerabilities that have a fix): a CRITICAL CVE with no
  upstream fix yet cannot be remediated by rebuilding — gating on it blocks every
  future build until the vendor patches, with no action you can take. Decide
  explicitly whether "no fix available" blocks or merely warns; most mature setups
  warn-and-track rather than hard-block on unfixed CVEs, but *do* hard-block once a
  fix exists and isn't picked up.
- Scanners read OS package databases (apk/dpkg/rpm) **and** language manifests
  (`package-lock.json`, `go.sum`, `requirements.txt` if baked in, Java `.jar`
  manifests) — a vulnerable transitive dependency compiled into a Go static
  binary with no OS packages at all can still be found by Trivy, which reads module
  information embedded in Go binaries (check each scanner's language coverage); distroless does not make an image CVE-free, it only removes the OS
  package-level attack surface (shell, package manager) and OS-level CVEs.

## 3. Severity gating is a policy decision, not a scanner setting
- CRITICAL/HIGH-only gates are common but miss the aggregate risk of many MEDIUMs
  in a widely-used library; conversely gating on every MEDIUM/LOW produces so much
  noise teams stop reading scan output (alert fatigue defeats the control).
  A workable default: hard-fail CI on fixable CRITICAL/HIGH, track MEDIUM/LOW in a
  dashboard with an SLA (e.g. 30/90 days) rather than blocking the pipeline on them.
- CVSS score alone ignores exploitability in *your* context — a CRITICAL in a
  library function you never call is lower real risk than a MEDIUM in
  internet-facing request parsing. **VEX (Vulnerability Exploitability eXchange)**
  documents let you formally assert "not affected, vulnerable code not reachable"
  per CVE per component, and feed that assertion back into the scanner/gate so the
  same CVE doesn't keep re-blocking builds after a documented, reviewed decision. Trivy reads VEX
  documents with `--vex` (experimental; CSAF VEX files are shown in its docs) and Grype supports OpenVEX
  with `--vex`.

## 4. Exceptions need an expiry, not just a suppression
- `.trivyignore` (entries can carry an expiry, `CVE-ID exp:YYYY-MM-DD`; `.trivyignore.yaml` uses
  `expired_at`) / Grype's ignore rules let you suppress a specific CVE ID for a
  specific image — always pair a suppression with a tracked ticket and an expiry
  date; an un-expiring ignore list is where "known" vulnerabilities go to become
  permanently unpatched and forgotten.
- Store exceptions in version control next to the Dockerfile (not as a one-off
  CLI flag someone ran once), so the decision is reviewable and the exception
  updates/removes itself when the next base-image bump resolves the CVE.

## 5. Admission-time enforcement
Same mechanism as other admission policy: Kyverno's `verifyImages` can check an
**attestation** containing scan results (image was scanned, attach the Trivy JSON
as a cosign attestation (predicate type `vuln`), verify a signed "no CRITICAL" assertion exists) rather
than re-scanning live in the admission path — re-scanning synchronously inside a
webhook request inherits every latency/timeout caveat in
`admission-webhooks-validating-and-mutating` and is slow (full image pull +
scan) for a per-request budget measured in seconds. Scan once in CI/registry,
attest the result, verify the attestation at admission. (Kyverno `verifyImages` rules in `ClusterPolicy` are deprecated as of Kyverno v1.19 and removed in v1.20; use `ImageValidatingPolicy`.)

## Gotchas
- Base-image CVE counts dominate most scan output — rebasing to a smaller/newer
  base image (distroless, `-slim`, chainguard images) often reduces findings more
  than fixing app-level dependencies; check base image age before chasing
  individual CVEs.
- A scanner's database staleness matters as much as the scan itself — Trivy/Grype
  pull a vulnerability DB that needs refreshing (`trivy image --download-db-only`
  pre-pulled in CI, or it refetches per run); a runner that uses `--skip-db-update` or an old
  cached DB misses recently disclosed CVEs.
- "0 findings" from a scan of an image with no package manager at all (scratch,
  some static binaries) usually means the scanner found nothing to scan, not that
  the image is clean — confirm the scanner actually detected a package ecosystem.

## Verify
- [ ] CI fails the build on fixable CRITICAL/HIGH CVEs; unfixed CVEs are tracked,
      not silently ignored.
- [ ] Vulnerability DB freshness is confirmed in CI logs (not a stale cached DB).
- [ ] Exceptions live in version control with a ticket reference and expiry, not
      as ad hoc CLI ignores.
- [ ] Admission gate checks a signed scan attestation rather than re-scanning
      synchronously in the webhook path.
- [ ] Registry continuous re-scan is enabled and alerts on newly-disclosed CVEs
      in already-deployed images.

## Checked

Checked 2026-10-27 against the Trivy docs source (aquasecurity/trivy, main), the Grype README and CLI option source, the cosign CLI reference and Kyverno docs source (kyverno/website, main; describes Kyverno v1.19).

- Trivy flags `--severity`, `--exit-code`, `--ignore-unfixed`, `--download-db-only`, `--skip-db-update`, `--vex`, and `.trivyignore` expiry (`exp:`, `expired_at`) confirmed; Go binaries with embedded module information are scanned by Trivy; VEX statuses such as `not_affected` shown in its docs.
- Grype `--fail-on` (severity threshold), `--only-fixed`, `--vex`, and OpenVEX support confirmed in its README and option definitions.
- cosign `--type vuln` predicate type confirmed in the cosign CLI reference; Kyverno ClusterPolicy deprecation (v1.19) confirmed.
- Removed unconfirmed claims: named registry products doing continuous re-scan, Grype binary-level Go detection, silent stale-database behaviour. The prose entries in `sources` were replaced with URLs.

Method: documentation only; no commands were run.
