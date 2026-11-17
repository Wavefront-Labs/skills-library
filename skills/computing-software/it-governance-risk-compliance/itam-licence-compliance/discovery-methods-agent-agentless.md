---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.discovery-methods-agent-agentless
name: discovery-methods-agent-agentless
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [discovery-methods-agent-agentless, asset-inventory-discovery, discovery, agent, agentless, snmp, wmi, mdm, cloud api, network scan, itam-licence-compliance]
level: practitioner
status: draft
description: "Choose between agent, agentless network scan, MDM and cloud API discovery for each asset class and combine them."
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

# Discovery methods: agent, agentless, API

Goal: complete device and software coverage with the least blind spots.

Method:
- Agent: richest software and usage data on endpoints/servers; needs deployment and upgrades.
- Agentless: SNMP, WMI, SSH, hypervisor APIs; good for network gear and servers where agents are banned.
- MDM/UEM (Intune, Jamf, Workspace ONE) for mobile and remote laptops.
- Cloud APIs (AWS, Azure, GCP, SaaS admin APIs) for ephemeral and SaaS assets.
- Passive: DHCP, switch ARP/CAM tables, NAC logs to find unknown devices.

Gotchas:
- Scan credentials with excessive rights are a security risk; use read-only accounts and vault them.
- Hypervisor hosts need cluster-level scans or you miss VM mobility.

Verify: compare discovered count to authoritative lists (AD, MDM, cloud accounts) and investigate delta over 5%.
