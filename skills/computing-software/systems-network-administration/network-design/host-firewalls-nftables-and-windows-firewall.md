---
id: computing-software.systems-network-administration.network-design.host-firewalls-nftables-and-windows-firewall
name: host-firewalls-nftables-and-windows-firewall
category: computing-software
field: systems-network-administration
product: network-design
tags: [firewall, host-firewall, nftables, windows-firewall, netsh-advfirewall, microsegmentation, linux]
level: practitioner
status: draft
description: "Configure host-based firewalls as a segmentation layer: nftables default-deny inbound rulesets on Linux and Windows Defender Firewall rules via PowerShell and GPO, with logging."
sources:
  - https://wiki.nftables.org/wiki-nftables/index.php/Main_Page
  - https://learn.microsoft.com/en-us/powershell/module/netsecurity/new-netfirewallrule
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Host firewalls: nftables and Windows Firewall

Network firewalls see traffic between zones; host firewalls stop lateral movement inside a VLAN.

## Linux nftables (default deny inbound)
`/etc/nftables.conf`:
```
table inet filter {
  set mgmt { type ipv4_addr; flags interval; elements = { 10.0.0.0/24 } }
  chain input {
    type filter hook input priority 0; policy drop;
    ct state established,related accept
    ct state invalid drop
    iif lo accept
    ip protocol icmp accept
    ip6 nexthdr icmpv6 accept               # ND needs this
    tcp dport 22 ip saddr @mgmt accept
    tcp dport { 80, 443 } accept
    log prefix "nft-drop " limit rate 5/second drop
  }
  chain forward { type filter hook forward priority 0; policy drop; }
  chain output  { type filter hook output priority 0; policy accept; }
}
```
```
nft -c -f /etc/nftables.conf       # syntax check
systemctl enable --now nftables
nft list ruleset
```
Distros with firewalld/ufw generate nftables rules; use one tool only. Docker and Kubernetes insert
their own chains; test container publishing after changes.

## Windows Defender Firewall
```
Set-NetFirewallProfile -Profile Domain,Private,Public -DefaultInboundAction Block -DefaultOutboundAction Allow -LogBlocked True -LogFileName %systemroot%\system32\LogFiles\Firewall\pfirewall.log
New-NetFirewallRule -DisplayName "RDP from jump hosts" -Direction Inbound -Protocol TCP -LocalPort 3389 -RemoteAddress 10.0.0.10,10.0.0.11 -Action Allow -Profile Domain
Disable-NetFirewallRule -DisplayGroup "Remote Desktop"     # remove the broad built-in rule
Get-NetFirewallRule -Enabled True -Direction Inbound | Get-NetFirewallAddressFilter
```
At scale use GPO (Computer Configuration > Windows Settings > Security Settings > Windows Defender
Firewall) or Intune; set "apply local firewall rules: No" so admins cannot punch holes.

## Workstation baseline
Block inbound SMB, RDP and WinRM between workstations (only from admin jump hosts); this alone
breaks most ransomware lateral movement.

## Gotchas
- Lock-out risk on remote Linux hosts: apply with a timed rollback (`nft -f new.conf; sleep 60; nft
  -f old.conf` in a screen session) until confirmed.
- Windows network profile detection: a server that sees its network as Public gets the wrong rules.
- Logging every drop floods disks; rate-limit.

## Verify
- [ ] From a peer in the same VLAN, blocked ports time out; allowed sources connect; drop logs show
  the attempts.
