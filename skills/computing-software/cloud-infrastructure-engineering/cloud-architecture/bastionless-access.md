---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.bastionless-access
name: bastionless-access
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, infrastructure-protection, bastionless-access, session-manager, iap, azure-bastion, just-in-time-access]
level: practitioner
status: docs-checked
description: "Give admins shell and RDP access without bastion hosts or open ports: Session Manager, IAP TCP forwarding, Azure Bastion/Entra login and session logging."
sources: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html", "https://cloud.google.com/iap/docs/using-tcp-forwarding", "https://learn.microsoft.com/azure/bastion/bastion-overview", "https://learn.microsoft.com/entra/identity/devices/howto-vm-sign-in-azure-ad-linux"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admin access without bastion hosts

## Steps
1. **Close inbound admin ports**: no 22/3389 from the internet or broad ranges; enforce by
   policy and CSPM.
2. **Use identity-aware brokered access**:
   - AWS Systems Manager Session Manager: IAM policies control who can start sessions and to
     which nodes, with no open inbound ports, bastion hosts or SSH keys; temporary access (for
     example an on-call rotation) is possible; supports port forwarding. VPC endpoints through
     AWS PrivateLink can further secure sessions.
   - Google IAP TCP forwarding: `gcloud compute ssh --tunnel-through-iap`; the firewall rule
     allows ingress only from 35.235.240.0/20 on the ports to expose (for example 22 and 3389);
     grant the IAP-Secured Tunnel User role (`roles/iap.tunnelResourceAccessor`); OS Login is
     the recommended way to manage SSH access.
   - Azure Bastion: managed RDP/SSH over TLS; VMs need no public IP, agent or special client.
     Basic, Standard and Premium need a dedicated subnet and a public IP on Bastion itself;
     Premium supports private-only deployment. Entra ID login for Linux VMs uses OpenSSH
     certificates with Azure RBAC (Virtual Machine Administrator Login or Virtual Machine User
     Login roles) and Conditional Access.
3. **Short-lived credentials**: Entra ID issues ephemeral SSH certificates; prefer these and
   OS Login over static keys.
4. **Session logging**: Session Manager logs to S3 and CloudWatch Logs and API calls go to
   CloudTrail; IAP access requests appear in Cloud Audit Logs once enabled; Azure Bastion session
   recording needs the Premium SKU. Send logs to the SIEM.
5. **Break-glass** path documented and tested.

## Gotchas
- Session Manager does not log sessions that connect through port forwarding or SSH, because the
  traffic is encrypted inside the tunnel.
- Azure Bastion bills hourly from deployment regardless of use.

## Verify
- [ ] No security group/NSG/firewall rule allows admin ports from broad ranges.
- [ ] Session logs arriving in SIEM with user identity.

## Checked
2026-11-08. Confirmed against all four cited pages: Session Manager (IAM control, no inbound ports, port forwarding, PrivateLink endpoints, S3/CloudWatch/CloudTrail logging, no logging for port forwarding or SSH), IAP TCP forwarding (35.235.240.0/20, ports, tunnel user role, --tunnel-through-iap, OS Login, Cloud Audit Logs), Azure Bastion overview (no public IP on VMs, SKU requirements, Premium session recording and private-only, hourly billing) and Entra Linux login (OpenSSH certificates, RBAC roles, Conditional Access). Removed: required endpoint names ssm/ssmmessages/ec2messages, tag conditions, EC2 Instance Connect, JIT elevation, "unreachable without endpoints" claim.
Method: documentation only; no commands were run.
