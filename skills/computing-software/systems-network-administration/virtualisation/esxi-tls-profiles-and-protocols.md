---
id: computing-software.systems-network-administration.virtualisation.esxi-tls-profiles-and-protocols
name: esxi-tls-profiles-and-protocols
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-tls-profile, tls-configurator, tls, vmware, vsphere]
level: advanced
status: docs-checked
description: "Control TLS protocol versions and cipher profiles on ESXi and vCenter, including the vSphere 8 TLS profiles, and verify with openssl."
sources:
  - https://knowledge.broadcom.com/external/article/377775/disable-cbc-ciphers-flagged-as-weak-by-s.html
  - https://knowledge.broadcom.com/external/article/377237/how-to-disable-sha1-tls-ciphers-managin.html
  - https://knowledge.broadcom.com/external/article/402714/disabling-tls-ciphers-on-vcenter.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ESXi and vCenter TLS profiles and protocol versions

**Goal:** only approved TLS versions and ciphers are offered, without breaking older integrations.

## By release
- **8.0 Update 3 and later**: named **TLS profiles**. `COMPATIBLE` (default; permits CBC
ciphers and older algorithms for interoperability) and `NIST_2024` (removes the
CBC/SHA1-family ciphers scanners flag). vCenter offers `NIST_2024`, `COMPATIBLE` and
`COMPATIBLE-NON-FIPS`; there is no `MANUAL` profile for vCenter. Check the TLS profile
KBs for the exact cipher list per profile and build.

## ESXi (8.0 U3+)
```bash
esxcli system tls server get
esxcli system tls server set -p NIST_2024
```
## vCenter (8.0 U3+)
vCenter TLS profiles are managed through the vSphere API (`appliance` > `tls/profiles/global`, GET to read, PUT with `{ "profile": "NIST_2024" }`) or curl against that REST endpoint; KB 377237 shows the full session and curl sequence. There is no standard CLI command. Services restart; plan a maintenance window, snapshot/back up first, and read the VCHA caveats in KB 377237. Auto Deploy environments need review before changing TLS profiles (see the same KB).

## Before tightening
Inventory every client of the host/vCenter APIs: backup proxies, monitoring, old PowerCLI or Java tools, hardware management agents, storage plug-ins. Clients without TLS 1.2+ or the allowed ciphers fail at handshake.

## Verify
```bash
openssl s_client -connect esx01.example.com:443 -tls1_1 </dev/null    # must fail
openssl s_client -connect esx01.example.com:443 -tls1_3 </dev/null    # succeeds with NIST_2024
nmap --script ssl-enum-ciphers -p 443 esx01.example.com
```
Check backup and monitoring jobs succeed after the change.

## Checked
2026-10-31: `esxcli system tls server get` and `esxcli system tls server set -p NIST_2024` confirmed in KB 377775; the COMPATIBLE default on 8.0 U3, NIST_2024 removing CBC/SHA1 ciphers, the vCenter profile set (`NIST_2024`, `COMPATIBLE`, `COMPATIBLE-NON-FIPS`, no MANUAL) confirmed in KB 377775 and KB 402714; the API path `tls/profiles/global` with GET/PUT and the curl sequence, VCHA special requirements and the Auto Deploy review note confirmed in KB 377237. Removed unconfirmed claims: the 6.7/7.0 TLS Configurator history, `UserVars.ESXiVPsDisabledProtocols`, the ESXi `MANUAL` profile, PowerCLI cmdlet names and the mandatory-reboot note.
Method: documentation only; no commands were run.
