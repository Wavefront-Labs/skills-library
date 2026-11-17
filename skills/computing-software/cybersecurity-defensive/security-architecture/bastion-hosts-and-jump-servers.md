---
id: computing-software.cybersecurity-defensive.security-architecture.bastion-hosts-and-jump-servers
name: bastion-hosts-and-jump-servers
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [network-segmentation, bastion-host, jump-server, privileged-access-workstation, session-recording, ssm-session-manager, azure-bastion]
level: practitioner
status: docs-checked
description: "Design jump servers and bastions as security-controlled intermediaries, and choose managed alternatives such as AWS Session Manager and Azure Bastion."
sources:
  - https://learn.microsoft.com/en-us/azure/bastion/bastion-overview
  - https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html
  - https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-intermediaries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bastion hosts and jump servers

**Goal:** administrative access to sensitive segments goes through a small number of
hardened, monitored intermediaries instead of direct connections from user networks.

## Why they need care
- A jump server is an intermediary in the session's Zero Trust chain, so it must keep or improve the security assurances of the session.
- Jump servers and VPNs are exposed to the internet to provide remote access and their maintenance is frequently neglected; an attacker needs only one unpatched service.
- A jump server used by administrators hosts many or all sensitive sessions, so attackers can use standard credential theft tools against it to steal and reuse credentials.
- Controls to cover: inbound connection security (Microsoft suggests Entra ID and Conditional Access so inbound devices and accounts are known and trusted), security of the intermediary itself, and the security signals for the next interface. Dedicated intermediary instances for privileged roles are optional and allow stricter restrictions and closer monitoring.

## Managed alternatives
- **AWS Systems Manager Session Manager:** node access without opening inbound ports, maintaining bastion hosts or managing SSH keys. Access is controlled by IAM policies (including temporary access, such as an on-call rotation). Supports port forwarding and Windows, Linux and macOS. Session logging goes to CloudTrail (API calls), S3 and CloudWatch Logs, and EventBridge with SNS can notify on session start or end. Sessions through port forwarding or SSH are not logged, because Session Manager only tunnels the encrypted SSH data.
- **Azure Bastion:** managed PaaS giving RDP/SSH over TLS (port 443) from the Azure portal or a native client; deployed in your virtual network, uses private IPs so VMs need no public IP, agent or special client software. Basic, Standard and Premium need a dedicated subnet named AzureBastionSubnet. Native client, shareable links, IP-based connections and file transfer need Standard or above; session recording and private-only deployment (no public IP) need Premium.
- Microsoft describes Azure Bastion and Entra application proxy as application- or server-specific access without general network access, and suggests moving over time from VPNs to them. Secure the Azure portal interface to the level of the resources and roles that use it.

## Gotchas
- Managed or not, a single path that all privileged sessions cross is a high-value target; protect it as privileged.
- PIM/PAM does not address device compromise: an attacker controlling an admin workstation can use the credentials while the user is logged on, so keep separate device and account protections.
- Session Manager logging gap for SSH and port-forwarded sessions (above): do not assume recordings exist.

## Verify
From a user network, direct SSH/RDP to targets fails; access via the intermediary requires authentication and is logged where the product supports it.

## Checked
Read the Azure Bastion overview, the AWS Session Manager landing page (benefits, logging and the SSH/port-forwarding note) and the Microsoft privileged access intermediaries page (jump server risks, Azure Bastion section, controls list). Removed as unconfirmed: placement and firewall rules, OS hardening list, short-lived SSH certificates, tier separation, patch timing, JIT and Teleport/Boundary/GCP IAP items, `tlog`, the Defender for Cloud JIT pairing, and the `ssh -J` agent forwarding advice.
Method: docs-checked 2026-11-09 against the Azure Bastion overview, AWS Session Manager page and Microsoft privileged access intermediaries page.
