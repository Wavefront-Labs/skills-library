---
id: computing-software.systems-network-administration.linux.nftables-and-iptables
name: nftables-and-iptables
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nftables, iptables, netfilter, firewall, nat, masquerade, conntrack, ip6tables, iptables-legacy, iptables-nft, chains, tables, packet-filtering, dnat, snat, sysadmin, networking, nftables-conf, iptables-save, nft-ruleset]
level: advanced
status: docs-checked
description: "Write and debug Linux firewalls in nftables and legacy iptables: tables/chains, NAT, conntrack, and the iptables-to-nft migration."
sources:
  - https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes
  - https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT)
  - https://wiki.nftables.org/wiki-nftables/index.php/Moving_from_iptables_to_nftables
  - https://wiki.nftables.org/wiki-nftables/index.php/Nftables_families
  - https://docs.kernel.org/networking/nf_conntrack-sysctl.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# nftables and iptables — Linux's packet filter, old and current syntax

**Goal:** read and write firewall rules that actually match the intended
packets, understand why a rule that looks right doesn't fire, and know which
tool a given box is really running under the hood.

## 1. Which one is this box actually using?
```bash
iptables --version              # the version string names the variant, e.g. iptables-nft (old syntax on the nf_tables backend) or iptables-legacy
nft list ruleset                # the nf_tables ruleset, including rules added through iptables-nft
```
The nftables wiki warns against using the nft and the legacy tools at the same time: they use the x_tables and nf_tables kernel subsystems and "could lead to unexpected results". Check `nft list ruleset` as the source of
truth whenever `iptables -L` and observed behaviour disagree.

## 2. nftables model: tables → chains → rules
```bash
nft add table inet filter
nft add chain inet filter input   { type filter hook input priority 0 \; policy drop \; }
nft add chain inet filter forward { type filter hook forward priority 0 \; policy drop \; }
nft add rule inet filter input ct state established,related accept
nft add rule inet filter input iif lo accept
nft add rule inet filter input tcp dport 22 accept
nft add rule inet filter input tcp dport { 80, 443 } accept
nft add rule inet filter input counter drop
```
`inet` tables see both IPv4 and IPv6 packets through the same rules (the main reason to prefer nftables
over maintaining parallel `iptables`/`ip6tables` rule sets). Persist with a
ruleset file and load it at boot:
```bash
nft -f /etc/nftables.conf           # load a ruleset file; the file path and the boot-time unit that loads it are distro-specific
```
A `.conf` file is just the same rule syntax, one statement per line, wrapped
in `table`/`chain` blocks — write it once, don't rebuild the ruleset
imperatively on every boot.

## 3. NAT (works the same way conceptually in both tools)
```bash
# nftables: masquerade outbound traffic from a LAN behind one public IP
nft add table ip nat
nft add chain ip nat postrouting { type nat hook postrouting priority 100 \; }
nft add rule ip nat postrouting oif "eth0" masquerade

# DNAT: forward port 8080 on the host to 192.168.1.10:80
nft add chain ip nat prerouting { type nat hook prerouting priority -100 \; }
nft add rule ip nat prerouting tcp dport 8080 dnat to 192.168.1.10:80
```
Equivalent legacy iptables:
```bash
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 192.168.1.10:80
```
Forwarding needs the kernel's permission too (`net.ipv4.ip_forward`, default 0 per the kernel docs; the nftables NAT page does not mention it) (see
`computing-software.systems-network-administration.linux.kernel-tuning-with-sysctl`).

## 4. conntrack — why "stateful" rules behave the way they do
```bash
conntrack -L | head                     # live connection tracking table
sysctl net.netfilter.nf_conntrack_max net.netfilter.nf_conntrack_buckets
```
`ct state established,related accept` (nftables) / `-m state --state
ESTABLISHED,RELATED -j ACCEPT` (iptables) is what lets reply traffic back in
without a matching inbound rule for every ephemeral port. The table has a
finite size (`nf_conntrack_max`, which defaults to `nf_conntrack_buckets`; entries are counted twice, once per direction). The bucket count defaults to total memory / 16384, between 1024 and 262144. Size both before traffic spikes.

## 5. Legacy iptables essentials (still the production reality on many boxes)
```bash
iptables -L -v -n --line-numbers        # see counters + rule numbers for -D/-I by position
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -I INPUT 1 -s 10.0.0.5 -j DROP # insert at the TOP — order matters, first match wins
iptables-save > rules.v4              # dump the ruleset; the persistent path and boot loader are distro-specific
iptables-restore < rules.v4
```
**Rule order decides outcome** — a `DROP` above an `ACCEPT` for the same
traffic wins; appending (`-A`) always adds to the bottom, so a broad early
`ACCEPT`/`DROP` can shadow everything added after it. `--line-numbers` plus
`-D INPUT <n>` is safer than reconstructing a rule to delete it by content.

## Gotchas
- `policy drop` on a chain plus **forgetting the loopback/established rules**
  is the single most common "I locked myself out of the box" mistake —
  always add `iif lo accept` and `ct state established,related accept`
  before adding a restrictive default policy, and test from a second session
  before closing the first.
- nftables sets (`{ 80, 443 }`) and iptables `-m multiport --dports 80,443`
  look similar but nftables sets can also be named and typed (`flags interval`, `timeout`; see the ipset skill) — use a named set for anything that changes at runtime
  (dynamic allow-lists, bans).
- `iptables -F` is documented as deleting all rules one by one; it says nothing about the chain policy, so check `iptables -S` for the policy before flushing on a remote box (a `DROP` policy with no rules drops everything).
- IPv6 needs its own rules (`ip6tables` legacy, or just use nftables' `inet`
  family) — a host "firewalled" only via IPv4 iptables is wide open over
  IPv6 if it has a routable v6 address.

## Verify
- [ ] `nft list ruleset` (not just `iptables -L`) matches intended policy — confirms which backend is actually enforcing.
- [ ] Loopback and established/related traffic are explicitly accepted before any default-drop policy.
- [ ] A reboot (or loading the ruleset file with `nft -f`) reproduces the same ruleset — rules aren't only "in RAM" from manual testing.
- [ ] The conntrack entry count stays well under `nf_conntrack_max` under expected peak load.
- [ ] NAT/forwarding rules are backed by `net.ipv4.ip_forward=1` where forwarding is intended.

## Checked

Date: 2026-10-25. Documentation release: nftables wiki pages (Quick reference, NAT, Moving from iptables to nftables, Nftables families, Sets), iptables(8) 1.8.13 and iptables-extensions(8) man pages, kernel nf_conntrack-sysctl.rst and ip-sysctl.rst (torvalds/linux master), all read 2026-10-25.
Confirmed: chain syntax `type filter hook input priority 0; policy drop;` (policy defaults to accept); `inet` sees IPv4 and IPv6; NAT chains at priority -100 (prerouting, dnat) and 100 (postrouting, masquerade) with the `nft add chain ... { type nat hook ... }` form; dnat/masquerade syntax; iptables-nft/legacy coexistence warning; iptables `-I` with rule number 1, `-D` by number, `--line-numbers`, MASQUERADE only in nat POSTROUTING, DNAT `--to-destination`, state match with ESTABLISHED,RELATED, multiport `--dports`; `nf_conntrack_max` and `nf_conntrack_buckets` defaults; `ip_forward` default 0; sets with `flags interval`/`timeout`.
Removed as unconfirmed: "most distros since 2020", update-alternatives, the systemd unit and config path, the `nf_conntrack: table full` log text, the iptables-save target paths, the `-F` policy claim as stated, and the live-update `add element` example.

Method: documentation only; no commands were run.
