---
id: computing-software.cloud-infrastructure-engineering.azure.defender-regulatory-compliance-standards
name: defender-regulatory-compliance-standards
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, defender-for-cloud, regulatory-compliance, compliance-standards, nist, cis-benchmark, iso-27001, pci-dss]
level: practitioner
status: docs-checked
description: "Assign regulatory compliance standards in Defender for Cloud (NIST 800-53, CIS, ISO 27001, PCI DSS), read control status, attest manual controls and export audit reports."
sources: ["https://learn.microsoft.com/azure/defender-for-cloud/concept-regulatory-compliance-standards", "https://learn.microsoft.com/azure/defender-for-cloud/update-regulatory-compliance-packages", "https://learn.microsoft.com/azure/defender-for-cloud/regulatory-compliance-dashboard"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assign regulatory compliance standards

**Goal:** the compliance dashboard shows the frameworks your auditors use, mapped to live
Azure evidence, with manual controls attested.

## Requirements
- Defender CSPM (or any paid Defender plan) on the subscription to add standards beyond the default Microsoft Cloud Security Benchmark (MCSB).
- Owner or Policy Contributor at the scope.

## Add a standard
Defender for Cloud → Environment settings → subscription/MG → **Security policies** → Standards →
enable the standards your auditors use (the available list includes *PCI DSS v4.0.1*; see the Defender for Cloud standards page for the current set). Under the hood this assigns the built-in Azure Policy
initiative in **Audit** mode.
CLI equivalent:
```bash
az policy assignment create --name nist-800-53-r5 --scope /providers/Microsoft.Management/managementGroups/mg-corp \
  --policy-set-definition <initiative-definition-id> --display-name "NIST SP 800-53 Rev. 5"
```
Assign at the MG so all subscriptions inherit; results aggregate in the dashboard.

## Read the dashboard
Regulatory compliance → standard → controls → each control lists assessments
(automated, from policy) with passed/failed resources. Controls with no automated assessment
are **manual** — attest them: *Manage compliance* / attestation with evidence (Defender CSPM feature for custom standards; for built-ins use documentation in the audit package).

## Audit reports
- **Download report** (PDF/CSV) per standard for the current state.
- Continuous export of regulatory compliance assessments to Log Analytics for point-in-time evidence and trend.

## Custom standards
Defender for Cloud supports creating custom standards for internal baselines.

## Gotchas
- A standard's pass % depends on its policy parameters (e.g. allowed locations) — set them, or controls fail spuriously.
- "Compliant" in the dashboard means the automated checks pass — not that you're certified; manual controls dominate many frameworks.

## Verify
- [ ] Standards list shows the required frameworks at the right MG.
- [ ] Monthly export of compliance state stored as audit evidence.

## Checked
2026-10-28. Confirmed on the Defender for Cloud regulatory compliance and standards pages: adding non-default standards needs at least one paid plan, manual assessments can be attested with linked evidence, PCI DSS v4.0.1 is listed, custom standards are supported. Removed: a hard-coded initiative GUID (now a placeholder), unverified standard version names, the audit reports blade, the multi-scope double-counting claim, KQL custom recommendations.
Method: documentation only; no commands were run.
