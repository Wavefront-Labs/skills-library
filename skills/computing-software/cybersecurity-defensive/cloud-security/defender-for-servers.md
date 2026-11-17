---
id: computing-software.cybersecurity-defensive.cloud-security.defender-for-servers
name: defender-for-servers
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [defender-for-servers, microsoft-defender-for-cloud, azure-arc, mde-integration, agentless-scanning, just-in-time-vm-access, cloud-workload-protection]
level: practitioner
status: docs-checked
description: "Deploy Defender for Servers: Plan 1 vs Plan 2, MDE auto-onboarding, agentless scanning, deployment scope, JIT VM access."
sources: ["https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-servers-overview", "https://learn.microsoft.com/en-us/azure/defender-for-cloud/just-in-time-access-usage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defender for Servers

## Plans
- Plan 1 is entry level and focuses on the EDR capabilities of the Defender for Endpoint integration. Plan 2 has everything in Plan 1 plus more.
- Plan 2 only (marked "-" for Plan 1 in the feature table): agentless vulnerability scanning, agentless malware scanning, agentless machine secrets scanning, Defender for DNS alerts, threat detection at the Azure network layer, OS system updates and OS baseline misconfigurations (Azure Arc machines only), Defender Vulnerability Management premium features (Defender portal only), file integrity monitoring, just-in-time VM access (Azure and AWS), network map (Azure), the free 500 MB data ingestion.
- Both plans: Defender for Endpoint automatic onboarding and EDR, integrated alerts and incidents, software inventory discovery, agent-based vulnerability scanning.
- Covers Windows and Linux machines in Azure, AWS, GCP and on-premises (connected to Defender for Cloud). Most features no longer need the Log Analytics agent or Azure Monitor Agent; AMA remains a collection method for the 500 MB ingestion benefit.

## Deployment scope
- Enable at the subscription level. Resource level: Plan 1 can be enabled and disabled per server; Plan 2 cannot be enabled per resource but can be disabled per resource.
- After enabling: a 30-day trial starts that cannot be stopped, paused or extended; the Defender for Endpoint extension is installed automatically on supported machines (automatic provisioning can be disabled); Defender Vulnerability Management is on by default for machines with the extension; agentless scanning is on by default for Plan 2; OS configuration assessment (Plan 2) against Microsoft Cloud Security Benchmark baselines needs the Azure Machine Configuration extension; set up file integrity monitoring yourself after enabling Plan 2.

## Just-in-time VM access
- Needs Defender for Servers Plan 2 on the subscription. Supports Resource Manager VMs, VMs behind Azure Firewall on the same VNet, and AWS EC2 (preview). Classic VMs and VMs behind Azure Firewall controlled by Azure Firewall Manager are unsupported; a VM needs an NSG or Azure Firewall.
- Recommended ports to protect: 22 (SSH), 3389 (RDP), 5985 and 5986 (WinRM). Per port you set protocol, allowed source IPs and maximum request time.
- Enabling from the VM Configuration page uses defaults: RDP 3389 or SSH 22, maximum access 3 hours, allowed source any.
- Policy name plus VM name cannot exceed 56 characters.
- Requesting access needs `Microsoft.Security/locations/jitNetworkAccessPolicies/initiate/action` plus read on the policies, VM, network interfaces and public IPs. Configuring a policy needs `Microsoft.Security/locations/jitNetworkAccessPolicies/write` and `Microsoft.Compute/virtualMachines/write`.
- If the requester is behind a proxy, enter the proxy IP range.
- PowerShell: `Set-AzJitNetworkAccessPolicy` to configure, `Start-AzJitNetworkAccessPolicy` to request. Audit via the VM's Activity Log from the Configured tab.

## Verify
- [ ] Servers show the plan enabled and Defender for Endpoint onboarded.
- [ ] JIT is configured on VMs that expose management ports.

## Checked
2026-11-09: read the Defender for Servers overview and the JIT access usage pages in full. Removed unconfirmed claims: Plan 1 vulnerability assessment detail, adaptive network hardening, regulatory compliance as Plan 2 only, Azure Arc connector mechanics, per-server-hour billing, duplicate onboarding handling, exclusions guidance, the Windows Server version list, and the plan-defender-for-servers source (not read).
Method: documentation only; no commands were run.
