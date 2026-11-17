---
id: computing-software.systems-network-administration.linux.ipset-address-sets
name: ipset-address-sets
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ipset, hash-net, hash-ip, blocklist, allowlist, iptables-set, nftables-sets, firewalld-ipset, timeout, geo-blocking, security, sysadmin]
level: practitioner
status: docs-checked
description: "Match thousands of addresses in one firewall rule with ipset (iptables/firewalld) or native nftables sets: set types, timeouts, atomic swap reloads, persistence and memory sizing."
sources:
  - https://ipset.netfilter.org/ipset.man.html
  - https://wiki.nftables.org/wiki-nftables/index.php/Sets
  - https://firewalld.org/documentation/man-pages/firewalld.ipset.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ipset and nftables sets

**Goal:** block or allow large, changing lists of IPs/networks (threat feeds, country
ranges, partner ranges) with O(1) lookups and reloads that never leave a gap.

## 1. ipset with iptables
```bash
ipset create blocklist hash:net family inet hashsize 4096 maxelem 262144 timeout 0
ipset add blocklist 203.0.113.0/24
ipset add blocklist 198.51.100.7 timeout 3600        # per-entry expiry (set created with timeout)
ipset test blocklist 203.0.113.9
iptables -I INPUT -m set --match-set blocklist src -j DROP
ipset list blocklist | head; ipset list -t            # -t: set names and headers only
```
Types: `hash:ip` (hosts), `hash:net` (networks), `hash:ip,port`, `hash:net,iface`,
`bitmap:port`, `list:set` (a list of set names). The default family is `inet` (IPv4); IPv6 needs a separate `family inet6` set. Defaults: `hashsize` 1024, `maxelem` 65536. `timeout` on `create` is the default entry timeout in seconds; a per-entry `timeout` is allowed when the set was created with timeout support.

## 2. Atomic reload from a feed
```bash
ipset create blocklist-new hash:net maxelem 262144 -exist
ipset flush blocklist-new
# feed.txt: one "add blocklist-new <net>" line per entry (restore input format, as written by `ipset save`)
ipset restore -exist < feed.txt
ipset swap blocklist-new blocklist      # exchanges the set names; the referring rule keeps using "blocklist" (sets must exist and be of compatible type)
ipset destroy blocklist-new
```
Persistence: `ipset save` writes the sets in the format `ipset restore` reads; restore them before the firewall rules at boot (the unit or package that does this is distro-specific).

## 3. firewalld
```bash
firewall-cmd --permanent --new-ipset=blocklist --type=hash:net --option=maxelem=262144
firewall-cmd --permanent --ipset=blocklist --add-entries-from-file=feed.txt
firewall-cmd --permanent --zone=drop --add-source=ipset:blocklist      # everything from the set → drop zone
firewall-cmd --reload
firewall-cmd --info-ipset=blocklist | head
```
`--add-entries-from-file` reads one entry per line (lines starting with `#` or `;` and empty lines are ignored). Permanent ipsets are stored as XML (see `firewalld.ipset(5)`), so very large feeds make the permanent configuration large.

## 4. Native nftables sets (no ipset needed)
```
table inet filter {
  set blocklist { type ipv4_addr; flags interval, timeout; auto-merge; }
  chain input { type filter hook input priority 0; ip saddr @blocklist drop; }
}
```
```bash
nft add element inet filter blocklist '{ 203.0.113.0/24, 198.51.100.7 }'
nft list set inet filter blocklist
```

## Gotchas
- A rule referencing a set that does not exist fails to load — create sets before the firewall rules at boot.
- `maxelem` is fixed at creation; size it for the largest feed (the ipset man page only documents `forceadd` evicting entries when a set is full).
- nft `interval` sets fail to load with "conflicting intervals" when entries overlap unless `auto-merge` is set.

## Verify
- [ ] `ipset test blocklist <ip>` (or `nft get element ...`) confirms membership; packet counters on the matching rule rise (`iptables -vnL` / `nft list ruleset`).
- [ ] After reboot the set is populated before the firewall rules that reference it load (`ipset list` shows the expected entries).

## Checked

Date: 2026-10-25. Documentation release: ipset man page at ipset.netfilter.org, nftables wiki "Sets" page, iptables-extensions(8) (set match), firewalld 2.5.2 man pages (firewall-cmd, firewalld.ipset), all read 2026-10-25.
Confirmed: `create` options hashsize/maxelem/timeout/family and their defaults; set types; `swap`, `restore -exist`, `save`, `list -t`; `-m set --match-set NAME src`; firewalld `--new-ipset --type --option`, `--add-entries-from-file` (one entry per line, `#`/`;` comments), `--add-source=ipset:`; nft set `flags interval, timeout`, `auto-merge`, "conflicting intervals" on overlap, `nft list set`, `nft get element`.
Removed as unconfirmed: the per-entry-timeout `nft add element` example, service and package names for restoring sets at boot, the reload-time figures and the claim that hash:net overlaps are always fine.

Method: documentation only; no commands were run.
