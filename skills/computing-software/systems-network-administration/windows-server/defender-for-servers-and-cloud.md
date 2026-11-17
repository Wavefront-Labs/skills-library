---
id: computing-software.systems-network-administration.windows-server.defender-for-servers-and-cloud
name: defender-for-servers-and-cloud
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, security-auditing, defender-for-servers, defender-for-cloud, defender-for-endpoint, secure-score, azure-arc, vulnerability-assessment]
level: practitioner
status: docs-checked
description: "Plan Defender for Servers in Defender for Cloud for Windows Servers: Plan 1 vs Plan 2, Azure Arc onboarding, file integrity monitoring and free ingestion."
sources:
  - https://learn.microsoft.com/en-us/azure/defender-for-cloud/plan-defender-for-servers
  - https://learn.microsoft.com/en-us/azure/defender-for-cloud/tutorial-enable-servers-plan
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defender for Servers and Defender for Cloud recommendations

## Plans
Defender for Servers has Plan 1 and Plan 2. After you enable a plan, a 30-day trial period begins. Plan 2 includes file
integrity monitoring (set up after enabling the plan) and 500 MB of free daily ingestion per node for eligible security
data when Plan 2 is enabled on the Log Analytics workspace the machines report to. If you onboard on-premises machines
by installing the Defender for Endpoint agent directly instead of Azure Arc, only Plan 1 functionality is available.

## On-premises servers
Onboard on-premises machines as Azure Arc-enabled VMs to use all Defender for Servers features.

## Verify
- [ ] The server appears in Defender for Cloud as an Azure Arc-enabled machine with the plan enabled.

## Checked

2026-10-28. Confirmed against: plan-defender-for-servers and tutorial-enable-servers-plan pages (Plan 1/Plan 2, Azure Arc onboarding, file integrity monitoring, 500 MB free ingestion, 30-day trial, Plan 1 only without Arc). Removed (not confirmable from the cited pages): plan feature table beyond those items, subscription settings path, MDE.Windows extension name, recommendation names, Sentinel connector, azcmagent and Get-MpComputerStatus checks.

Method: documentation only; no commands were run.
