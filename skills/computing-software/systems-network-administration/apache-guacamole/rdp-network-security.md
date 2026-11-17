---
id: computing-software.systems-network-administration.apache-guacamole.rdp-network-security
name: rdp-network-security
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, rdp, rdp-parameters, security-mode, nla, ignore-cert, domain, disable-auth, hostname, port, timeout]
level: practitioner
status: draft
description: "Guacamole RDP connection parameters for host, port, timeout and credentials, plus the security modes any, nla, nla-ext, tls, vmconnect and rdp, ignore-cert and disable-auth."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RDP: network, authentication and security

| Parameter | Default | Notes |
|---|---|---|
| `hostname` | required | RDP server |
| `port` | 3389 (2179 for vmconnect) | |
| `timeout` | 10 | seconds before aborting |
| `username`, `password`, `domain` | none | optional; if missing and NLA is used, the user may be prompted |
| `security` | `any` | `any`, `nla`, `nla-ext`, `tls`, `vmconnect`, `rdp` |
| `ignore-cert` | validate | `true` accepts any certificate, incl. self-signed |
| `disable-auth` | off | `true` skips authentication on connect |

Security modes:
- `any`: negotiate what both ends support.
- `nla`: Network Level Authentication (TLS, credentials before session).
- `nla-ext`: as nla plus the Early User Authorization Result.
- `tls`: RDSTLS, mainly for load-balanced servers that redirect.
- `vmconnect`: Hyper-V only (see apache-guacamole.rdp-hyperv-vmconnect).
- `rdp`: legacy RDP encryption for older Windows; disabled by default on newer.

NLA requires authentication, so do not set `disable-auth=true` with NLA.

Prompting: Guacamole asks for credentials only when none are configured; a wrong preconfigured password fails instead of prompting (apache-guacamole.parameter-tokens for injecting `${GUAC_USERNAME}`).

Common failures: certificate errors on self-signed hosts mean `ignore-cert=true` (or install the CA); "Error instantiating client" in guacd logs means a malformed parameter (apache-guacamole.troubleshooting-guacd-errors).

Verify: the connection reaches the Windows login or desktop with the expected security mode.
