---
id: computing-software.systems-network-administration.linux.firewall-cmd-zones-and-services
name: firewall-cmd-zones-and-services
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, firewalld, firewall-cmd, firewalld-zones, firewalld-services, service-definitions, permanent-vs-runtime, port-forwarding, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Run firewalld with firewall-cmd: zones and how traffic is assigned to them, opening services/ports runtime vs permanent, custom service definitions, and verifying the result."
sources:
  - https://firewalld.org/documentation/man-pages/firewall-cmd.html
  - https://firewalld.org/documentation/man-pages/firewalld.zones.html
  - https://firewalld.org/documentation/man-pages/firewalld.service.html
  - https://github.com/firewalld/firewalld/tree/main/doc/xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# firewall-cmd: zones and services

**Goal:** open exactly the services a host needs, on the right interfaces/sources, and make
it persistent (the RHCSA staple).

## 1. State
```bash
firewall-cmd --state
firewall-cmd --get-active-zones           # zone ← interfaces / sources
firewall-cmd --get-default-zone           # public on most installs
firewall-cmd --list-all                   # default zone: services, ports, rich rules, masquerade
firewall-cmd --list-all --zone=internal
firewall-cmd --get-services | tr ' ' '\n' | grep -i http
```

## 2. How traffic is assigned to a zone
A zone is bound to an interface (`--change-interface=eth1`, or the NetworkManager profile `connection.zone`) or to a source address, network, MAC or ipset (`--add-source=10.0.0.0/8`); connections with no zone use the default zone (`--get-default-zone`). A connection can only be in one zone. The zone file `target` attribute is `ACCEPT`, `%%REJECT%%` or `DROP`; see `firewall-cmd --info-zone=<z>` for what a zone does with unlisted traffic.

## 3. Open services and ports
```bash
firewall-cmd --add-service=https                         # runtime only (lost on reload/reboot)
firewall-cmd --permanent --add-service=https             # permanent only (not active until reload)
firewall-cmd --reload
# or do runtime first, test, then:
firewall-cmd --runtime-to-permanent
firewall-cmd --permanent --zone=internal --add-port=8443/tcp
firewall-cmd --permanent --zone=internal --add-source=10.20.0.0/16
firewall-cmd --permanent --remove-service=cockpit
firewall-cmd --add-service=ssh --timeout=10m             # temporary
```
Interface to zone persistently with NetworkManager: `nmcli con mod eth1 connection.zone internal`.

## 4. Custom service definitions
```bash
firewall-cmd --permanent --new-service=myapp
firewall-cmd --permanent --service=myapp --set-description="MyApp API" --add-port=9443/tcp --add-port=9444/udp
firewall-cmd --reload && firewall-cmd --permanent --add-service=myapp && firewall-cmd --reload   # new permanent services only appear after a reload
firewall-cmd --info-service=myapp
```
The definition is a service XML file (see `firewalld.service(5)`) — ship it with config management or the app package. A named service documents
*why* ports are open; prefer it over bare `--add-port`.

## Gotchas
- `--permanent` without `--reload` → it "doesn't work"; runtime without permanent → it "stops working" after reboot.
- Docker adds its own rules and, with firewalld running, a `docker` zone with target ACCEPT for its bridge interfaces, so container traffic is not governed by your other zones.

## Verify
- [ ] `firewall-cmd --list-all --zone=<z> --permanent` equals runtime `--list-all`.
- [ ] From another host: `nc -zv host 443` succeeds; an unopened port is rejected/filtered.

## Checked

Date: 2026-10-25. Documentation release: firewalld man page sources (firewalld/firewalld master, doc/xml: firewall-cmd, firewalld.richlanguage, firewalld.zone, firewalld.zones, firewalld.ipset; latest release tag v2.5.2, read 2026-10-25); Docker docs (docker/docs packet-filtering-firewalls.md).
Confirmed: `--runtime-to-permanent`; `--timeout` with s/m/h time values (runtime only, not combinable with `--permanent`); `--new-service`, `--info-service`; `--add-source` accepting source/mask, MAC or `ipset:`; `--change-interface` going through NetworkManager; `--reload` discarding runtime-only changes; zone `target` values; NetworkManager `connection.zone` property; Docker's `docker` zone.
Removed as unconfirmed: the strict source, then interface, then default matching order and the per-zone default-target sentence; the SELinux, iptables-conflict and service-file path statements.

Method: documentation only; no commands were run.
