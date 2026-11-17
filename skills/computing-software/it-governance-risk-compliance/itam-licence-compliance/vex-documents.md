---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.vex-documents
name: vex-documents
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [vex-documents, vex-and-vulnerability-linkage, vex, vulnerability exploitability exchange, not_affected, under_investigation, openvex, csaf vex, justification, cyclonedx vex, itam-licence-compliance]
level: advanced
status: docs-checked
description: "Author VEX statements marking vulnerabilities not_affected, affected, fixed or under_investigation with justifications."
sources:
  - https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md
  - https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html
  - https://cyclonedx.org/capabilities/vex/
  - https://github.com/anchore/grype
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VEX statements and status values

Goal: tell consumers which vulnerabilities in the SBOM actually matter.

OpenVEX status values: not_affected, affected, fixed, under_investigation. CSAF 2.0 product_status instead uses lists such as known_affected, known_not_affected, fixed and under_investigation. CycloneDX analysis.state has its own values (resolved, resolved_with_pedigree, exploitable, in_triage, false_positive, not_affected).
For not_affected give a justification, e.g. component_not_present, vulnerable_code_not_present, vulnerable_code_not_in_execute_path, vulnerable_code_cannot_be_controlled_by_adversary, inline_mitigations_already_exist.
Formats: OpenVEX (JSON-LD), CycloneDX vulnerabilities[].analysis (state, justification, response), CSAF 2.0 VEX profile.
An OpenVEX statement combines product(s), a vulnerability and a status, within a document that has a timestamp.

Method: triage scanner findings in reachability review, publish VEX with each release, update as status changes.

Gotchas:
- A VEX is a claim by the supplier; consumers decide trust.
- Don't mark not_affected without evidence; keep the analysis.

Verify: consumer tooling (grype lists OpenVEX support in its README) ingests the document.

## Checked

2026-11-02. Checked against the OpenVEX spec (statement structure, statuses, justification required for not_affected, JSON-LD, timestamp), the CSAF 2.0 standard (csaf_vex profile, product_status fields), the CycloneDX 1.6 schema (vulnerabilities analysis state, justification, response) and the grype README (OpenVEX support). Fixed: the status list was presented as universal but is OpenVEX's; CSAF and CycloneDX use different values. Removed: the grype --vex flag and GHSA identifier.

Method: documentation only; no commands were run.
