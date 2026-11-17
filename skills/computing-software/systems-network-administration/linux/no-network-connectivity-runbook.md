---
id: computing-software.systems-network-administration.linux.no-network-connectivity-runbook
name: no-network-connectivity-runbook
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, no-connectivity, network-unreachable, network-troubleshooting, runbook, link-down, default-route, dns-failure, arp, firewall, console-access, sysadmin]
level: practitioner
status: draft
description: "Runbook for a Linux host with no network: from the console, check link, address, route, gateway ARP, DNS, firewall and upstream in order, with the command and the fix at each step."
sources:
  - https://man7.org/linux/man-pages/man8/ip.8.html
  - https://www.freedesktop.org/software/systemd/man/latest/resolvectl.html
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_and_managing_networking/index
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Runbook: host has no network connectivity

**Goal:** restore connectivity on a host you can only reach by console (IPMI, hypervisor,
cloud serial console) by walking the stack bottom-up and stopping at the first broken layer.

## 0. Scope it (30 seconds)
- One host or many? Many on the same segment → switch/VLAN/gateway/DHCP, not this host.
- What changed? `last -x | head`, `journalctl --since -2h -p warning`, `dnf history | head` / `/var/log/apt/history.log`, recent `nmcli`/netplan edits.

## 1. Link
```bash
ip -br link                           # state UP / DOWN / NO-CARRIER
ethtool eno1 | grep -E 'Link detected|Speed|Duplex'
journalctl -k -b | grep -iE 'eno1|link is|renamed'
```
NO-CARRIER → cable/switch port/vNIC disconnected (hypervisor) or wrong NIC (interface renamed after hardware change).
DOWN → `nmcli con up <profile>` / `ip link set eno1 up`; check why the profile didn't autoconnect.

## 2. Address
```bash
ip -br addr
nmcli -f NAME,DEVICE,STATE con show; nmcli dev status
```
No IPv4: DHCP failed (`journalctl -u NetworkManager -g dhcp`) or static profile not applied. `169.254.x.x` = DHCP failed, link-local fallback.
Wrong subnet/prefix (e.g. /32) → fix the profile, `nmcli con up`.

## 3. Gateway and route
```bash
ip route; ip route get 1.1.1.1
ping -c3 <gateway>
ip neigh show <gateway>                # FAILED/INCOMPLETE = no ARP reply
```
No default route → profile missing gateway, or a second interface stole it (metrics). ARP INCOMPLETE → wrong VLAN, gateway down, or duplicate IP (`arping -D -I eno1 <own-ip>`).

## 4. Beyond the gateway
```bash
ping -c3 1.1.1.1                      # IP reachability
tracepath -n 1.1.1.1                  # where it stops; MTU issues
```
Gateway pings but internet doesn't → upstream routing/NAT, or local firewall blocking outbound.

## 5. DNS
```bash
resolvectl status; cat /etc/resolv.conf
dig +short example.com; dig @1.1.1.1 +short example.com
```
IP works, names don't → wrong/unreachable resolvers, broken `/etc/resolv.conf` symlink, or `nsswitch.conf`.

## 6. Local firewall and policy
```bash
nft list ruleset | head -50; firewall-cmd --list-all
ip rule; sysctl net.ipv4.conf.all.rp_filter
```
Default-drop OUTPUT, wrong zone, or strict `rp_filter` with asymmetric routing. Temporarily `systemctl stop firewalld` **only** to confirm, then fix the rule.

## 7. Inbound only broken (outbound fine)
Service bound to 127.0.0.1 (`ss -ltnp`), firewall input rule, cloud security group/NACL, or upstream ACL.

## After restoring
Record cause and fix; make the fix persistent (profile, not `ip` commands); reboot test if the cause was configuration.

## Verify
- [ ] Gateway, an external IP and a DNS name are reachable; the original failing service works from a client.
- [ ] The fix is in persistent config (`nmcli con show`, netplan/networkd files) and survives a reboot.
