---
id: computing-software.it-support-helpdesk.remote-support-tools.ztna-client-support
name: ztna-client-support
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, ztna, zscaler, global-secure-access, netskope, cloudflare-warp, posture, private-access]
level: practitioner
status: draft
description: "Support zero trust network access clients (Zscaler, Entra Global Secure Access, Netskope, WARP): service status, posture failures, app segments, DNS, SSL inspection breaks."
sources:
  - "https://learn.microsoft.com/en-us/entra/global-secure-access/troubleshoot-global-secure-access-client-diagnostics-health-check"
  - "https://help.zscaler.com/zscaler-client-connector/troubleshooting-zscaler-client-connector"
  - "https://developers.cloudflare.com/cloudflare-one/connections/connect-devices/warp/troubleshooting/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ztna-client-support

ZTNA brokers per-application access instead of putting the device on the network. Most
tickets are "one app does not work" rather than "VPN down".

## First checks
1. Client status: signed in, all services On (Zscaler: Internet Security and Private
   Access; Global Secure Access: Microsoft, Internet, Private profiles; WARP:
   `warp-cli status` = Connected).
2. Is the device posture compliant? Most ZTNA checks Intune compliance, EDR running, OS
   version, or a certificate. A non-compliant device gets blocked per app.
3. Is the app defined? Private apps must be published as an application segment/enterprise
   app with the hostname and port the user uses. "Works by FQDN, fails by IP or short
   name" means only the FQDN is defined.

## DNS and routing
- ZTNA intercepts DNS for private app domains; a hard-coded DNS server, another VPN, or a
  hosts-file entry bypasses it.
- Legacy VPN and ZTNA together cause route and DNS fights; one should be disabled.

## SSL inspection breaks
Internet traffic inspection replaces certificates. Apps that pin certificates (some
dev tools, Git, Python/Node with their own CA store, banking apps) fail with TLS errors.
Fix with the inspection root CA in the tool's store or a bypass rule; never by turning
off the client.

## Logs
- Zscaler Client Connector: Troubleshoot > Export Logs, and Repair App.
- Global Secure Access client: Advanced diagnostics > Health check and Traffic tabs show
  which rule handled a flow.
- WARP: `warp-cli debug` bundle / `warp-diag`.
Escalate with user, device, time, destination host:port and the export.

## Gotchas
- Captive portals need the client's captive portal detection or a short fail-open window.
- Clock skew and expired device certificates fail posture silently.

## Verify
Health check passes, the private app opens by its published name, and the client log
shows the flow handled by the expected rule.
