---
id: computing-software.cloud-infrastructure-engineering.docker.container-image-security-scanning
name: container-image-security-scanning
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, container-security, image-scanning, vulnerability-scanning, cve, trivy, grype, syft, docker-scout, snyk-container, sbom, spdx, cyclonedx, vex, openvex, cosign, sigstore, image-signing, slsa, provenance, attestation, secret-scanning, misconfiguration, ci-gate, severity-threshold, ignorefile, kyverno-verify-images, supply-chain-security, epss, kev]
level: advanced
status: docs-checked
description: "Scan container images and act on results: Trivy/Grype/Scout in CI, severity gates that don't cry wolf, SBOMs and VEX, ignore files with expiry, cosign signing and admission-time verification."
sources: ["https://trivy.dev/latest/docs/configuration/filtering/", "https://trivy.dev/latest/docs/scanner/secret/", "https://github.com/anchore/grype", "https://github.com/docker/scout-cli", "https://docs.docker.com/build/metadata/attestations/", "https://docs.sigstore.dev/cosign/signing/signing_with_containers/", "https://openvex.dev/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container image security scanning — findings people actually fix

**Goal:** every image is scanned before it ships and again while it runs, the gate blocks
what matters and nothing else, and production only admits images you built and signed.
Reducing attack surface in the Dockerfile itself (distroless, non-root) is in
`computing-software.cloud-infrastructure-engineering.docker.multi-stage-dockerfiles`.

## 1. What scanners actually check
- **OS packages** and **language dependencies** found in the image, matched against the
  scanner's vulnerability database.
- Optionally **secrets** (Trivy `--scanners secret`) and **misconfiguration** (Dockerfile and
  Kubernetes YAML via `trivy config`).
- Blind spots: software that is not recorded as a package (for example a binary downloaded
  into `/usr/local/bin`) can be missed; a scanner reports nothing for what it cannot see.

## 2. CI scanning
```bash
trivy image --scanners vuln,secret --severity HIGH,CRITICAL --ignore-unfixed \
  --exit-code 1 --format table registry.example.com/api:${GIT_SHA}
grype registry.example.com/api:${GIT_SHA} --fail-on high --only-fixed
docker scout cves --only-severity critical,high --exit-code registry.example.com/api:${GIT_SHA}
trivy config --exit-code 1 .            # Dockerfile / k8s misconfig
```
- Scan the **pushed digest** you will deploy, not a local rebuild.
- `--ignore-unfixed` / `--only-fixed` for the blocking gate: failing a build on a CVE with no
  fix available teaches people to bypass the gate. Still *report* unfixed findings.
- Cache the vulnerability DB in CI (`TRIVY_CACHE_DIR`) or use a mirror; anonymous DB pulls
  can be rate-limited.

## 3. Triage that scales
Severity alone is a poor priority. Order by:
1. In CISA **KEV** (exploited in the wild) → fix now (`docker scout cves --only-cisa-kev`).
2. High **EPSS** score (`docker scout cves --epss`) and reachable (package actually loaded by the app).
3. CVSS critical/high with a fix → next base-image bump.
4. Everything else → batch with routine updates.

Most findings in a typical image come from the base layer; rebuilding on a fresh base
digest (Renovate/Dependabot) clears more than any per-CVE work.

## 4. Suppressions with accountability
```yaml
# .trivyignore.yaml
vulnerabilities:
  - id: CVE-2024-XXXXX
    paths: ["usr/lib/x86_64-linux-gnu/libfoo.so.1"]
    statement: "libfoo not loaded by the service; vendor fix pending"
    expired_at: 2026-12-31
```
- Every ignore has a reason and an expiry; an expired ignore re-fails the build.
- Prefer **VEX** (OpenVEX/CycloneDX VEX) statements (`not_affected`, with justification)
  attached to the image as an attestation — consumers and other scanners can read them.
  Trivy and Grype both accept VEX input (check flags for your version).

## 5. SBOM, provenance, signing
```bash
docker buildx build --sbom=true --provenance=mode=max --push -t registry.example.com/api:${GIT_SHA} .
syft registry.example.com/api@sha256:<DIGEST> -o cyclonedx-json > sbom.cdx.json
cosign sign --yes registry.example.com/api@sha256:<DIGEST>          # keyless via OIDC in CI
cosign verify registry.example.com/api@sha256:<DIGEST> \
  --certificate-identity-regexp 'https://github.com/<ORG>/<REPO>/.+' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```
- Sign the **digest**, never a tag.
- Keep SBOMs; when the next big library CVE lands, `grype sbom:sbom.cdx.json` answers
  "are we affected?" across every image in minutes without re-pulling.
- Enforce at deploy time with an admission or pull-time policy that rejects unsigned images
  or ones signed by the wrong identity.

## 6. Continuous scanning
New CVEs appear for images that have not changed. Rescan running/registry images daily
(registry-native scanning, Docker Scout, or a scheduled job rescanning stored SBOMs) and route
new criticals to the owning team, not a shared channel.

## Gotchas
- Two scanners give different counts for the same image (feeds, matching rules); pick one as
  the gate and use the other for spot checks only.
- `latest`/mutable tags make scan results meaningless — the scanned bytes may not be what runs.
- Removing a package in a later layer hides it from some scanners but it still ships in
  earlier layers; rebuild without it.
- Keyless cosign identity regexes that are too loose (`.*`) accept any repo's workflow.
- Secret findings in layers mean the secret is leaked: rotate it, do not just rebuild.

## Verify
- [ ] CI fails on a deliberately vulnerable test image (e.g. an old base) and passes on current.
- [ ] Every ignore entry has a statement and an expiry date.
- [ ] Each released digest has an SBOM, provenance and a signature (`cosign tree <IMAGE>`).
- [ ] Admission policy rejects an unsigned image in a test namespace.
- [ ] Daily rescan exists and its last run is less than 24 h old.

## Checked
Documentation release: Trivy docs (main: `trivy image` CLI reference, filtering page, secret scanning), Grype v0.121.0 source, Docker Scout `docker scout cves` reference (docker/docs data/cli), Docker build attestations docs and cosign v3.1.4 reference, checked 2026-10-26.
Confirmed: Trivy flags `--scanners`, `--severity`, `--ignore-unfixed`, `--exit-code`, `--format`, `TRIVY_CACHE_DIR`; Grype `--fail-on` and `--only-fixed`; Scout `--only-severity`, `--exit-code` (exit code 2), `--epss`, `--only-cisa-kev`; `.trivyignore.yaml` fields `id`, `paths`, `statement`, `expired_at` (documented as experimental); Trivy and Grype `--vex`; `--sbom=true` and `--provenance=mode=max` buildx flags; `cosign verify` identity flags and `cosign tree`.
Removed as unsupported by the documentation read: the NVD over-reporting claim, "go binary build info" cataloguing, named admission controllers (Kyverno, Policy Controller, Gatekeeper with Ratify) and Trivy Operator.
Method: documentation only; no commands were run.
