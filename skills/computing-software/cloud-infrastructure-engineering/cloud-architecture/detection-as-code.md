---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.detection-as-code
name: detection-as-code
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, detection-and-response, detection-as-code, sigma, detection-engineering, ci-cd]
level: practitioner
status: draft
description: "Manage detection rules as code: Sigma or native query rules in git, review, unit tests with sample logs, CI deployment to SIEM, versioning and tuning metrics."
sources: ["https://github.com/SigmaHQ/sigma", "https://learn.microsoft.com/azure/sentinel/ci-cd", "https://docs.panther.com/detections", "https://cloud.google.com/chronicle/docs/detection/yara-l-2-0-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detection rules as code

## Steps
1. **Format**: write rules in Sigma (vendor-neutral YAML, converted with pySigma backends) or
   the SIEM's native language (KQL for Sentinel, YARA-L for Google SecOps, SPL) stored in git
   with metadata: ATT&CK technique, severity, data source, owner, runbook link.
2. **Review**: pull requests with a second detection engineer; check logic, performance and
   false positive expectations.
3. **Test**: each rule has positive and negative sample events; CI runs them (pySigma
   conversion plus query execution against a test dataset or the SIEM test API).
4. **Deploy via pipeline**: Sentinel repositories/ARM or Terraform, SecOps API, Splunk
   apps; no console edits in production (or detect and reconcile drift).
5. **Version and tune**: track alert volume, true-positive rate per rule; suppressions are
   code changes with justification.
6. **Coverage reporting** generated from rule metadata against ATT&CK.

## Gotchas
- Rules that pass syntax checks but never fire due to wrong field names; tests catch it.
- Console hot-fixes during incidents drift from git; reconcile after.

## Verify
- [ ] Every rule has sample-based tests running in CI.
- [ ] Deployed rules match the repository.
