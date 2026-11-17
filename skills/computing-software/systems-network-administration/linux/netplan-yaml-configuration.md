---
id: computing-software.systems-network-administration.linux.netplan-yaml-configuration
name: netplan-yaml-configuration
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, netplan, netplan-yaml, netplan-apply, netplan-try, ubuntu, static-ip, dhcp, renderer, systemd-networkd, networkmanager, networking, sysadmin]
level: practitioner
status: docs-checked
description: "Configure Ubuntu networking with netplan YAML: static/DHCP addresses, routes, DNS, renderer choice, safe netplan try/apply, and reading the generated backend config."
sources:
  - https://netplan.readthedocs.io/en/stable/netplan-yaml/
  - https://netplan.readthedocs.io/en/stable/netplan-try/
  - https://github.com/canonical/netplan/tree/main/doc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# netplan YAML — Ubuntu's network description layer

**Goal:** describe interfaces once in YAML, let netplan render them for systemd-networkd
(servers) or NetworkManager (desktops), and apply changes without locking yourself out.

## 1. Where things live
- `netplan generate` reads `/lib/netplan/*.yaml`, `/etc/netplan/*.yaml` and `/run/netplan/*.yaml`. A file with the same name in `/run/netplan` shadows one in `/etc/netplan`, which shadows one in `/lib/netplan`; files with different names are read in lexicographic order and later files override earlier ones.
- Netplan's security guidance: keep all YAML files readable and writable by root only (`chmod 600`), since they can hold secrets such as Wi-Fi or WireGuard keys.
- Cloud images may ship a cloud-init generated file in this directory; check how your image manages it before editing.
- The backend files netplan generates are output; edit the YAML, not them.

## 2. Static server config
```yaml
# /etc/netplan/01-lan.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eno1:
      match: {macaddress: "52:54:00:12:34:56"}
      set-name: lan0
      dhcp4: false
      dhcp6: false
      addresses: [10.0.10.20/24, "2001:db8:10::20/64"]
      routes:
        - to: default
          via: 10.0.10.1
        - to: 192.168.50.0/24
          via: 10.0.10.254
          metric: 50
      nameservers:
        addresses: [10.0.0.53, 10.0.0.54]
        search: [corp.example]
      mtu: 9000
```
- `gateway4:` is deprecated (see "Default routes" in the netplan reference); use `routes: - to: default`.
- `set-name` is used together with a `match:` on unique properties; a second device matching the rule fails to be renamed and keeps its kernel name.
- DHCP with your own DNS: `dhcp4: true` + `dhcp4-overrides: {use-dns: false}` (`use-dns` defaults to true and only affects the networkd backend).

## 3. Apply safely
```bash
netplan generate                 # syntax/semantic check, writes backend files only
netplan try --timeout 120        # applies, rolls back unless you confirm in time (default timeout 120 s)
netplan apply                    # apply the configuration
netplan get ethernets.eno1       # read the merged YAML from /{etc,lib,run}/netplan
netplan status --all             # live state, including inactive interfaces
networkctl status lan0           # networkd renderer view
```
Over SSH prefer `netplan try`; it rolls back if you do not confirm. Per the man page, if it times out or is cancelled, verify that the configuration was really reverted and check the files on disk before rebooting. Some configurations (such as STP) can take over a minute to settle.

## Gotchas
- YAML indentation errors give "Invalid YAML" with a line number; tabs are illegal.
- Two files defining the same interface merge silently — `netplan get` shows the result.
- With `renderer: NetworkManager`, changes made with `nmcli` do not go back into the YAML; pick one tool for edits.
- A device that does not match any definition is not configured by netplan; if an interface is missing after reboot check that its key or `match:` fits the device name.

## Verify
- [ ] `netplan generate` silent; `ip -br addr` and `ip route` show the intended addresses and default route.
- [ ] `resolvectl status lan0` lists the configured DNS servers and search domain.
- [ ] Reboot: the same state returns without manual action.

## Checked

Date: 2026-10-25. Documentation release: netplan docs (canonical/netplan main: doc/netplan-yaml.md, netplan-generate.md, netplan-try.md, netplan-get.md, netplan-status.md, security.md), read 2026-10-25.
Confirmed: search directories and shadowing/lexicographic order; `chmod 600` guidance; `renderer` values networkd/NetworkManager; `match: macaddress`, `set-name` behaviour; `routes: to: default` and `gateway4` deprecation; `dhcp4-overrides use-dns`; `netplan try --timeout` default 120 s and its known-issues note; `netplan get`; `netplan status --all`; `openvswitch` and `vlans` mappings.
Removed as unconfirmed: the cloud-init disable file contents, version numbers for warnings and `netplan status`, exact generated file names, the claim that try refuses bonds/bridges and its `at` workaround, and the manpages.ubuntu.com apply link (replaced by the netplan repository documentation).

Method: documentation only; no commands were run.
