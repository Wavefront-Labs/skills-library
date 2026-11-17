---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.oracle-virtualisation-and-cloud
name: oracle-virtualisation-and-cloud
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [oracle-virtualisation-and-cloud, oracle-licensing, oracle vmware, hard partitioning, soft partitioning, authorized cloud environments, oracle cloud policy, itam-licence-compliance]
level: sme
status: draft
description: "Apply Oracle's partitioning and cloud policies to VMware, public cloud and authorised cloud environments."
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

# Oracle on virtualised and cloud platforms

Goal: avoid cluster-wide licence demands.

Key policy points (confirm the current Oracle Partitioning Policy and Cloud Licensing Policy):
- Hard partitioning methods approved by Oracle (e.g. Oracle VM with pinning, LPAR on IBM, Solaris zones) allow licensing the partition only.
- Soft partitioning, including VMware vSphere, is not accepted; Oracle may require licensing all physical hosts in the vCenter or cluster that could host the VM.
- Authorised cloud environments (AWS, Azure) count two vCPUs as one Processor licence when hyperthreading is enabled, one vCPU per core otherwise; confirm current policy.
- Mitigation: dedicate clusters or hosts to Oracle, restrict migration with DRS rules, or move to Oracle-supported platforms.

Gotchas:
- Policy documents are not part of the contract unless referenced; get legal advice.

Verify: vCenter evidence of host affinity rules.
