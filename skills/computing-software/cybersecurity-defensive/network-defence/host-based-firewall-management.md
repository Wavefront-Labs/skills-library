---
id: computing-software.cybersecurity-defensive.network-defence.host-based-firewall-management
name: host-based-firewall-management
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [firewall, host-based-firewall, windows-defender-firewall, nftables, firewalld, ufw, lateral-movement-prevention]
level: practitioner
status: draft
description: "Manage host-based firewalls at scale: default-deny inbound on Windows Defender Firewall via Intune or GPO and nftables or firewalld on Linux, logging and blocking lateral movement ports."
sources: ["Microsoft Learn - Windows Firewall best practices and Intune firewall policy", "nftables wiki and Red Hat firewalld documentation", "CIS Controls v8 Safeguard 4.5 Implement and manage a firewall on end-user devices"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Host-based firewalls

**Goal:** every host blocks unsolicited inbound traffic except what its role needs, limiting lateral movement even inside trusted networks.

## Windows Defender Firewall
- Profiles Domain/Private/Public all **On**, inbound default **Block**, outbound default Allow (outbound restriction is possible but costly to maintain).
- Deploy via Intune (Endpoint security > Firewall policy and Firewall rules) or GPO (Computer Configuration > Windows Settings > Security Settings > Windows Defender Firewall with Advanced Security).
- **Disable local rule merge** ("Apply local firewall rules: No") so users/apps cannot add their own allow rules; push needed app rules centrally.
- Workstations: block inbound SMB (445), RPC (135), WinRM (5985/5986), RDP (3389) from other workstations; allow only from management/jump subnets. This breaks most worm and ransomware lateral spread.
- Logging: `%systemroot%\system32\LogFiles\Firewall\pfirewall.log`, log dropped packets, size 16 MB+; or audit Filtering Platform events 5157/5152 (noisy - scope carefully).
- Check: `Get-NetFirewallProfile | Select Name,Enabled,DefaultInboundAction`; `Get-NetFirewallRule -PolicyStore ActiveStore`.

## Linux
- firewalld (RHEL): `firewall-cmd --set-default-zone=drop` (careful remotely), `firewall-cmd --permanent --zone=public --add-service=ssh --add-source=10.250.0.0/16` style rich rules, `--reload`.
- ufw (Ubuntu): `ufw default deny incoming; ufw allow from 10.250.0.0/16 to any port 22 proto tcp; ufw enable`.
- nftables directly:
  ```
  table inet filter { chain input { type filter hook input priority 0; policy drop;
    ct state established,related accept; iif lo accept;
    ip saddr 10.250.0.0/16 tcp dport 22 accept; icmp type echo-request limit rate 5/second accept;
    log prefix "nft-drop " counter drop; } }
  ```
- Docker/Kubernetes nodes manage their own chains; test interactions (Docker bypasses ufw INPUT for published ports).

## macOS
Application firewall + stealth mode via MDM configuration profile (`com.apple.security.firewall`).

## Verify
- [ ] Compliance report shows firewall on with block-inbound on all managed endpoints.
- [ ] From one workstation, `Test-NetConnection <peer> -Port 445` fails.
- [ ] Drops logged and sampled into the SIEM.
