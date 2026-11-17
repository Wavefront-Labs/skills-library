---
id: computing-software.systems-network-administration.linux.hostname-and-name-resolution
name: hostname-and-name-resolution
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, hostname, hostnamectl, hosts-file, etc-hosts, resolv-conf, systemd-resolved, resolvectl, name-resolution, nsswitch, dns-client, search-domain, split-dns, mdns, networkmanager-dns, dhcp-dns, getent, lpic-1, networking, sysadmin, dns-over-tls]
level: practitioner
status: docs-checked
description: "Set the hostname and control Linux name resolution: /etc/hosts, nsswitch order, who owns resolv.conf (resolved, NetworkManager, DHCP), split DNS and search domains, debugging with resolvectl/getent."
sources:
  - https://man7.org/linux/man-pages/man1/hostnamectl.1.html
  - https://man7.org/linux/man-pages/man5/resolv.conf.5.html
  - https://man7.org/linux/man-pages/man8/systemd-resolved.service.8.html
  - https://man7.org/linux/man-pages/man5/nsswitch.conf.5.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hostname and name resolution — fix "it resolves in dig but not in curl"

**Goal:** a host with a stable name that resolves itself, and a DNS client config you
can explain: which file is authoritative, who rewrites it, and in what order lookups happen.

## 1. Hostname
```bash
hostnamectl set-hostname web01.example.com      # writes /etc/hostname, applies live
hostnamectl set-hostname --pretty "Web 01"
hostnamectl                                     # static / transient / pretty
```
- Static hostname = `/etc/hostname`; transient = what the kernel reports (DHCP can set
  it); pretty = free text. `hostname -f` needs the FQDN resolvable — put it in `/etc/hosts`:
  `127.0.1.1 web01.example.com web01` (Debian style) or `<primary ip> web01.example.com web01`.
  `sudo` lags seconds and logs "unable to resolve host" when this line is missing.
- Cloud images: cloud-init sets the hostname each boot unless `preserve_hostname: true`
  in `/etc/cloud/cloud.cfg.d/`.
- NetworkManager may overwrite it from DHCP: `hostname-mode=none` in `[main]` of
  `/etc/NetworkManager/NetworkManager.conf`.

## 2. Lookup order: nsswitch
```
# /etc/nsswitch.conf
hosts: mymachines resolve [!UNAVAIL=return] files myhostname dns
```
(Example from the systemd nss-resolve manual; the order differs between distributions, so read your own file.)
- `files` = `/etc/hosts` (use it for emergency overrides and for the
  host's own name). `myhostname` resolves the local hostname and `localhost`. `resolve` =
  systemd-resolved via NSS (it also reads `/etc/hosts` itself); `dns` = classic libc
  through `/etc/resolv.conf`.
- `getent hosts name` uses the full NSS chain (what applications see); `dig`/`host`
  talk to DNS directly and ignore `/etc/hosts` and resolved's per-link routing — hence
  "dig works, app doesn't".

## 3. Who owns `/etc/resolv.conf`
```bash
ls -l /etc/resolv.conf            # symlink target tells you the owner
```
| Target | Owner | Configure with |
|---|---|---|
| `../run/systemd/resolve/stub-resolv.conf` (nameserver 127.0.0.53) | systemd-resolved | `resolvectl`, `/etc/systemd/resolved.conf(.d)`, per-link via NM/networkd |
| `../run/systemd/resolve/resolv.conf` | resolved; lists the upstream servers directly, bypassing the stub | same |
| plain file | NetworkManager (`dns=default`), dhclient, or you | `nmcli con mod eth0 ipv4.dns "10.0.0.2 10.0.0.3" ipv4.dns-search example.com`; `ipv4.ignore-auto-dns yes` to stop DHCP overriding |
| `../run/NetworkManager/resolv.conf` | NM directly | as above |
Writing to it by hand works until the owner next runs. To hand-manage: set
`dns=none` in NetworkManager.conf, or `systemctl disable --now systemd-resolved` and
replace the symlink with a real file.

## 4. systemd-resolved essentials
```bash
resolvectl status                 # per-link DNS servers, search domains, DNSSEC/DoT state
resolvectl query web01.example.com
resolvectl dns eth0 10.0.0.2 10.0.0.3; resolvectl domain eth0 example.com
resolvectl domain wg0 '~corp.internal'      # route only this domain to the VPN link's DNS
resolvectl flush-caches; resolvectl statistics
```
- `~domain` = routing-only domain (split DNS); `~.` makes a link the default for everything.
- Global fallback: `/etc/systemd/resolved.conf.d/dns.conf` → `[Resolve] DNS=10.0.0.2 FallbackDNS= Domains=example.com`.
- `DNSSEC=` accepts a boolean or `allow-downgrade`, which resolved.conf(5) recommends unless the DNS server is known to support DNSSEC correctly; `DNSOverTLS=` accepts a boolean or `opportunistic`.
- `LLMNR=` and `MulticastDNS=` can be set to `no` to disable those protocols.

## 5. Debugging checklist
```bash
getent hosts api.internal || echo "NSS fails"
dig @"$(awk '/^nameserver/{print $2; exit}' /etc/resolv.conf)" api.internal
resolvectl query api.internal        # shows which link/server answered
journalctl -u systemd-resolved -b | grep -i 'using degraded\|timed out'
```
- Search list: `options ndots:1` is the libc default; Kubernetes pods use `ndots:5`, which
  is why bare names resolve slowly there. `search a.example b.example` applies to names with
  fewer dots than ndots.
- `options timeout:2 attempts:2 rotate` in resolv.conf (or `resolved.conf` equivalents)
  shortens stalls when the first server is dead (default timeout is 5 s).
- A resolver that mishandles parallel A/AAAA queries can cause multi-second hangs: fix the resolver,
  or use `options single-request` as a workaround.

## Verify
- [ ] `hostname -f` returns the FQDN instantly and `sudo true` prints no resolution warning.
- [ ] `ls -l /etc/resolv.conf` matches the intended owner, and it survives a reboot/DHCP renew.
- [ ] `getent hosts <internal name>` and `dig <internal name>` agree.

## Checked
2026-10-27. Checked against systemd hostnamectl(1), resolvectl(1), resolved.conf(5), systemd-resolved.service(8), nss-resolve(8) and nss-myhostname(8) (current main), man-pages resolv.conf(5) (6.19), NetworkManager.conf (hostname-mode none, dns=none) and the cloud-init set_hostname module (preserve_hostname). Confirmed: pretty, static and transient hostnames; resolvectl status, query, dns, domain, flush-caches and statistics; routing-only domains with a ~ prefix and ~. ; stub-resolv.conf and resolv.conf paths and the 127.0.0.53 stub; resolved.conf DNS, FallbackDNS, Domains, DNSSEC allow-downgrade, DNSOverTLS opportunistic, LLMNR and MulticastDNS; nsswitch example with resolve [!UNAVAIL=return]; NetworkManager hostname-mode and dns none. Removed: the Go and musl resolver remark, the mdns4_minimal remark, the CIS remark and the 'safe production values' wording.

Method: documentation only; no commands were run.
