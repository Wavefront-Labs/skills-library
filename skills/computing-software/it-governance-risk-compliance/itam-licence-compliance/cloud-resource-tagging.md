---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.cloud-resource-tagging
name: cloud-resource-tagging
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [cloud-resource-tagging, cloud-and-virtual-asset-management, tagging, aws tags, azure tags, gcp labels, cost allocation tags, owner tag, itam-licence-compliance]
level: practitioner
status: draft
description: "Define and enforce a mandatory tag schema in AWS, Azure and GCP so every resource has an owner and cost centre."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud resource tagging and ownership

Goal: every cloud resource attributable to an owner.

Method:
- Mandatory tags: owner, cost-centre, environment, application, data-classification, expiry (for non-prod).
- Enforce: AWS Tag Policies and SCPs, Azure Policy (deny or append), GCP organisation policy and label constraints.
- Activate cost allocation tags in AWS Billing so they appear in cost reports.
- Remediate untagged resources with automation, then notify owners.
- Review tag compliance weekly as a KPI.

Gotchas:
- Not all resource types support tags; use account/subscription boundaries as fallback.
- Free-text tags drift; use allowed values.

Verify: tag coverage exceeds 95% of spend.
