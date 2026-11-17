---
id: computing-software.cloud-infrastructure-engineering.google-cloud.assured-workloads-and-compliance-controls
name: assured-workloads-and-compliance-controls
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, assured-workloads, compliance, data-residency, access-transparency, access-approval, resource-locations, gcp-resourcelocations, sovereign-controls, fedramp, il4, cjis, hipaa, eu-regions-and-support, key-access-justifications, compliance-reports-manager, shared-responsibility, data-sovereignty]
level: advanced
status: docs-checked
description: "Meet residency and regulatory needs: Assured Workloads folders, resourceLocations policy, Access Approval and Transparency, Key Access Justifications."
sources: ["https://docs.cloud.google.com/assured-workloads/docs/overview", "https://docs.cloud.google.com/organization-policy/restrict-locations", "https://docs.cloud.google.com/assured-workloads/key-access-justifications/docs/overview", "https://docs.cloud.google.com/sdk/gcloud/reference/assured/workloads/create", "https://docs.cloud.google.com/sdk/gcloud/reference/access-approval/settings/update", "https://assuredworkloads.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assured Workloads and compliance controls

**Goal:** workloads under a regime (EU data boundary, FedRAMP Moderate/High, IL4, CJIS,
healthcare, ITAR, Canada Protected B...) run in a folder where the platform enforces the controls, and Google access to your data is visible and, where required, approvable.

## 1. Residency without Assured Workloads (first step for everyone)
```bash
gcloud resource-manager org-policies allow gcp.resourceLocations in:eu-locations --folder=<EU_FOLDER_ID>
# value groups: in:eu-locations, in:us-locations, in:asia-locations, or explicit regions like europe-west1
```
- The `gcp.resourceLocations` constraint controls creation of resources whose location can be chosen. It does not affect global resources (for example Compute Engine global addresses) or resources with no selectable location, and it does not cover every service: check the supported-services list.
- Multi-region values such as `eu` and `us` exist; `global` is treated as a multi-region and is not controllable.
- Related constraints: `gcp.restrictCmekCryptoKeyProjects` and `gcp.restrictNonCmekServices` for keys.

## 2. Assured Workloads
```bash
gcloud assured workloads create --organization=<ORG_ID> --location=europe-west4 \
  --display-name=eu-boundary --compliance-regime=EU_DATA_BOUNDARY_AND_SUPPORT \
  --billing-account=billingAccounts/<BILLING_ID> \
  --provisioned-resources-parent=folders/<PARENT_FOLDER>
```
- A control package creates a folder; its controls define guardrails for every project and resource inside, enforced with organisation policy constraints and other features. Support for products varies by control package, so check "Supported products by control package".
- **Control package names changed in June 2025.** Use the new `ComplianceRegime` values, for example `EU_DATA_BOUNDARY_AND_SUPPORT`, `US_DATA_BOUNDARY_AND_SUPPORT`, `CANADA_DATA_BOUNDARY_AND_SUPPORT`, `AUSTRALIA_DATA_BOUNDARY_AND_SUPPORT`, `DATA_BOUNDARY_FOR_FEDRAMP_MODERATE`, `DATA_BOUNDARY_FOR_FEDRAMP_HIGH`, `DATA_BOUNDARY_FOR_IL2`, `DATA_BOUNDARY_FOR_IL4`, `DATA_BOUNDARY_FOR_IL5`, `DATA_BOUNDARY_FOR_CJIS`, `DATA_BOUNDARY_FOR_ITAR`, `DATA_BOUNDARY_FOR_IRS_PUBLICATION_1075`, `DATA_BOUNDARY_FOR_CANADA_PROTECTED_B`, `US_DATA_BOUNDARY_FOR_HEALTHCARE_AND_LIFE_SCIENCES` (and `..._WITH_SUPPORT`), `ISRAEL_DATA_BOUNDARY_AND_SUPPORT`, `JAPAN_DATA_BOUNDARY`, `KSA_DATA_BOUNDARY_WITH_ACCESS_JUSTIFICATIONS`, `SWITZERLAND_DATA_BOUNDARY_WITH_ACCESS_JUSTIFICATIONS`, `ASSURED_WORKLOADS_FOR_PARTNERS`. Old names (`EU_REGIONS_AND_SUPPORT`, `FEDRAMP_HIGH`, `IL4`, `CJIS`, `ITAR`, `CA_REGIONS_AND_SUPPORT`, `AU_REGIONS_AND_US_SUPPORT`, `ISR_REGIONS`, `JP_REGIONS_AND_SUPPORT`, `KSA_REGIONS_AND_SUPPORT_WITH_SOVEREIGNTY_CONTROLS`) are marked as superseded in the API, and `HIPAA` and `HITRUST` are deprecated in favour of the US healthcare package. `complianceRegime` is immutable once set.
- Package types: regional data boundaries (residency, some with personnel and access controls), regulatory data boundaries (FedRAMP, CJIS, IL levels, ITAR, IRS 1075, Canada Controlled Goods, healthcare) and Sovereign Controls by Partners (partner-operated keys, access justification and audits).
- Personnel controls come from Assured Support, an Assured Workloads feature of Customer Care that needs Enhanced or Premium Support. For FedRAMP High, first- and second-level support staff and subprocessors must be US-located with enhanced background checks.
- Key management: ITAR requires CMEK, with a separate key management project and a unique key ring in a compliance location. Other packages support Google-managed keys, CMEK, Cloud EKM and key import. The `--next-rotation-time` and `--rotation-period` flags set KMS settings, and `--resource-settings` customises resources such as the consumer project ID.
- **Monitoring**: Assured Workloads watches organisation policy and resource violations; enable email notifications for violations and exceptions; list them with `gcloud assured workloads violations list`. Workload updates let you move a folder to a newer version of its control package.

## 3. See and gate Google's access
- **Access Transparency** shows logs of Google personnel activity for support and availability work.
- **Access Approval** requires an authorised administrator in your organisation to approve a request before Google administrators get access. Approved accesses are logged in Access Transparency logs. With Assured Workloads, the Assured Workloads personnel assurances take priority over Access Approval request conditions.
```bash
gcloud access-approval settings update --organization=<ORG_ID> --enrolled_services=all --notification_emails=sec@example.com
```
Flags use underscores: `--enrolled_services`, `--notification_emails`, `--active_key_version` (key version used to sign approvals), `--preferred_request_expiration_days`. For project and folder enrollment only `all` is supported.
- **Key Access Justifications** produces a justification code for each cryptographic operation on enrolled Cloud KMS keys, works with Cloud EKM, Cloud HSM or software keys depending on the control package, and lets you approve or deny key access by code. For select packages it logs the codes (Key Access Transparency); for others you can set policy to deny. Access Approval requests can only be processed if the associated key access is permitted by the key's justification policy.

## 4. Evidence and shared responsibility
Document your side per regime: identity, IAM, data classification, key choices, network boundaries, patching, log retention. The Security Command Center compliance monitoring covers configuration mapping (see the security-command-center skill). Compliance reports and agreements (BAA, DPA) come from the Google Cloud compliance resource centre and the terms; this skill does not restate their contents.

## Gotchas
- Support for Google Cloud products varies by control package; check before promising a feature.
- Access Approval delays Google support because nobody looks until you approve; staff a rota or a watched notification channel.
- Assured Support requires Enhanced or Premium Support.

## Verify
- [ ] Creating a bucket in a disallowed location in the folder fails with a `gcp.resourceLocations` constraint error.
- [ ] `gcloud assured workloads describe` shows the expected `complianceRegime` and no active violations.
- [ ] Access Transparency log entries and Access Approval requests appear for a support case where Google touched the project.

## Checked
2026-10-28. Confirmed against the Assured Workloads overview (control package types, personnel controls, key management, violation monitoring, renaming notice, Access Approval and Key Access Justifications behaviour), the resource locations page (constraint scope, value groups, global as multi-region), the Key Access Justifications overview, the gcloud references for `assured workloads create` and `access-approval settings update` (flag names), and the Assured Workloads v1 and Access Approval v1 discovery documents (`ComplianceRegime` enum with superseded and deprecated values; settings fields). Corrected: Access Approval flags use underscores; regime names were renamed in June 2025. Removed: pricing uplift claims, the Access Transparency log name and reason codes, Compliance Reports Manager contents, HIPAA BAA steps, partner names, and project-move behaviour, none of which were readable in the fetched pages.
Method: documentation only; no commands were run.
