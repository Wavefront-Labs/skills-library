---
id: computing-software.cloud-infrastructure-engineering.docker.in-registry-scanning-harbor-and-ecr
name: in-registry-scanning-harbor-and-ecr
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, vulnerability-scanning, registry-scanning, harbor-scanning, ecr-scanning, trivy, amazon-inspector, image-scanning]
level: practitioner
description: "Turn on registry-side scanning (Harbor with Trivy, ECR basic or enhanced/Inspector, Artifact Registry, ACR Defender) and act on results via policy and API."
sources: ["https://goharbor.io/docs/main/administration/vulnerability-scanning/", "https://github.com/boto/botocore/blob/develop/botocore/data/ecr/2015-09-21/service-2.json", "https://github.com/goharbor/harbor/blob/main/api/v2.0/swagger.yaml"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# In-registry scanning (Harbor, ECR and friends)

CI scanning sees an image once; registry scanning rescans stored images when new CVEs land.

## Harbor + Trivy
- Trivy must be enabled at install time (`--with-trivy` for `install.sh`; Helm `trivy.enabled`). Other
  scanners connect through the pluggable interrogation service; Clair is no longer a default scanner
  (removed in v2.2) but can be added as an external scanner.
- Administration -> Interrogation Services: default scanner, Vulnerability tab with **Scan Now** for all
  artifacts and a schedule (hourly, daily at midnight, weekly at midnight Saturday, custom cron).
- Project -> Configuration: automatic scan on push, and **Prevent vulnerable images from running** with a
  severity threshold: images at or above that severity cannot be pulled (negligible is never blocked).
- CVE allowlist per project (optionally copied from the system allowlist) or system-wide for accepted risks.
- Scans of Cosign signatures are not supported.
- API: `GET /api/v2.0/projects/{p}/repositories/{r}/artifacts/{ref}?with_scan_overview=true`
  for CI gates, `.../additions/vulnerabilities` to export a report; webhook `SCANNING_COMPLETED` for alerts.

## AWS ECR
```sh
# registry-level scanning configuration (PutImageScanningConfiguration is being deprecated in its favour)
# BASIC supports SCAN_ON_PUSH; ENHANCED (Amazon Inspector) supports CONTINUOUS_SCAN and SCAN_ON_PUSH
aws ecr put-registry-scanning-configuration --scan-type ENHANCED \
  --rules '[{"scanFrequency":"CONTINUOUS_SCAN","repositoryFilters":[{"filter":"app","filterType":"PREFIX_MATCH"}]}]'
aws ecr describe-image-scan-findings --repository-name app --image-id imageTag=1.4.0 \
  --query 'imageScanFindings.findingSeverityCounts'
```
- With no registry scanning configuration the BASIC scan type is used; if scan on push is not specified,
  the MANUAL frequency is the default.
- `filterType` is `PREFIX_MATCH` in the current botocore model (the only enum value listed); check the
  Amazon ECR API reference for newer filter types.

## Others
Google Artifact Registry, Azure Container Registry and Docker Hub have their own scanning features; follow
the vendor documentation for current behaviour and pricing rather than this skill.

## Operating it
- Registry findings are inventory; gates belong in CI (fail build) and admission (block deploy).
- Decide owner per repo for triage; untriaged dashboards are noise.
- Old tags accumulate findings forever - lifecycle policies reduce noise and cost.

## Verify
Push an image with a known CVE; once the scan completes the API/CLI query above shows non-zero
CRITICAL/HIGH counts.

## Checked

2026-10-26. Documentation release: Harbor website docs main (last commit 2026-10-15), goharbor/harbor swagger.yaml, goharbor/harbor-helm values.yaml, boto/botocore ECR service model. Confirmed: Trivy install flag and Helm value, Clair removal in v2.2, scan schedule choices, prevent-vulnerable threshold semantics, with_scan_overview parameter, additions/vulnerabilities endpoint, SCANNING_COMPLETED event, ECR scan types, scan frequencies per type, defaults, deprecation of PutImageScanningConfiguration, and filterType enum. Removed unconfirmed claims: 412 status on blocked pulls, Clair-based basic scanning, the Inspector EventBridge detail type, continuous scan window figures, and the GCP, Azure and Docker Scout details (AWS and Google docs were not readable as source).

Method: documentation only; no commands were run.
