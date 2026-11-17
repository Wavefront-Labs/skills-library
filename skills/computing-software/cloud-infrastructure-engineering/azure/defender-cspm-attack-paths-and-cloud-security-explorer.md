---
id: computing-software.cloud-infrastructure-engineering.azure.defender-cspm-attack-paths-and-cloud-security-explorer
name: defender-cspm-attack-paths-and-cloud-security-explorer
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, defender-for-cloud, defender-cspm, attack-paths, cloud-security-explorer, agentless-scanning, sensitive-data-discovery]
level: advanced
status: docs-checked
description: "Use Defender CSPM: enable agentless scanning and data discovery, triage attack paths, query the cloud security graph with Cloud Security Explorer, and act on choke points."
sources: ["https://learn.microsoft.com/azure/defender-for-cloud/concept-cloud-security-posture-management", "https://learn.microsoft.com/azure/defender-for-cloud/how-to-manage-attack-path", "https://learn.microsoft.com/azure/defender-for-cloud/how-to-manage-cloud-security-explorer", "https://learn.microsoft.com/azure/defender-for-cloud/concept-agentless-data-collection"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defender CSPM: attack paths and cloud security explorer

**Goal:** fix the few misconfigurations that create real exploitable paths to sensitive data,
instead of chasing thousands of individual recommendations.

## Enable
```bash
az security pricing create -n CloudPosture --tier standard \
  --extensions name=AgentlessVmScanning isEnabled=True
```
Agentless VM scanning snapshots disks (no agent) for vulnerabilities, secrets and malware context;
enable the other CSPM extensions (for example sensitive data discovery) in Environment settings.

## Attack paths
Defender for Cloud → **Attack path analysis**. Each path: entry point (e.g. internet-exposed VM
with high-severity vuln) → lateral steps (managed identity with permissions, key in VM) → target
(storage account with sensitive data). Fields: risk level, risk factors, **choke points**.
Triage loop:
1. Sort by risk level; open path; read the "Insights" (e.g. *VM has a managed identity that can read storage X*).
2. Fix the **cheapest link** that breaks the path: remove public IP, reduce role, patch CVE, remove plaintext secret.
3. After you resolve a path it can take up to 24 hours to leave the list.

## Cloud security explorer
Graph queries over resources, identities, vulnerabilities, data and exposure:
- Templates: *Internet-exposed VMs with high-severity vulnerabilities*, *Storage accounts with sensitive data accessible by a VM with internet exposure*, *Kubernetes pods running privileged containers*.
- Build: Virtual machine → *is exposed to internet* AND *has vulnerability with severity High* AND *has managed identity with permission to* Storage account → *contains sensitive data*.
- Save queries and export results (CSV) for owners.

## Use with governance
Assign governance rules/owners to the recommendations on attack paths; integrate with
ServiceNow via workflow automation; track count of critical/high attack paths as the KPI.

## Gotchas
- Without data discovery, "sensitive data" conditions never match → fewer paths shown.
- Scanning disks encrypted with customer-managed keys needs extra permissions on the agentless extension; check the agentless coverage docs.

## Verify
- [ ] Plan extensions all show On in Environment settings.
- [ ] Attack path count tracked weekly; each critical path has an owner ticket.

## Checked

2026-10-28. Confirmed on the az security pricing reference and attack path page: --tier and --extensions exist, AgentlessVmScanning extension name appears in the reference example, resolved attack paths can take up to 24 hours to leave the list, CMK-encrypted disks need more permissions. Removed: unconfirmed extension names, first-scan time, the ADE unsupported claim and the connector claim.

Method: documentation only; no commands were run.
