---
id: computing-software.networking-hardware-and-wireless.tailscale.tailscale-cert-https
name: tailscale-cert-https
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [https-certificates, tailscale-cert, certificate-transparency]
level: practitioner
status: docs-checked
description: "Turn on HTTPS, understand the public ledger exposure and run tailscale cert."
sources: ["https://tailscale.com/kb/1153", "https://tailscale.com/kb/1080"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPS certificates

Goal: get Let's Encrypt certificates for MagicDNS names.

**Enable**

1. Enable MagicDNS.
2. Admin console DNS page, HTTPS Certificates, Enable HTTPS.
3. Acknowledge that machine names and the tailnet DNS name are published on a public ledger.
4. On each machine run `tailscale cert`.

**Public ledger.** All TLS certificates are recorded in Certificate Transparency logs. The tailnet name hides your organization name, but machine names are still published, so do not enable HTTPS if machine names contain sensitive information. Only devices where you ran `tailscale cert` appear. Access is still restricted as normal. Changing tailnet name is only allowed between the default and a randomized name.

**Command**
```
tailscale cert hostname.tails-scales.ts.net
tailscale cert --cert-file=cert.pem --key-file=key.pem hostname.tails-scales.ts.net
```
- Let's Encrypt certificates expire after 90 days, so renew periodically; file-based installs need your own renewal handling, while integrations such as Caddy renew automatically.
- You cannot get an HTTPS URL for a bare hostname such as `https://machine-name`.
- Tailscale creates a `*.ts.net` DNS TXT record to complete the challenge.
- To serve files or proxy HTTP, use `tailscale serve` instead.

**Checklist**

1. Review machine names.
2. Run cert on needed hosts only.
3. Plan renewal.

## Checked

2026-11-03. Read Set up HTTPS certificates (kb/1153) and CLI reference (kb/1080) and confirmed Enable HTTPS, the public ledger caveat, `tailscale cert` flags, 90-day expiry and the bare-hostname limit. Nothing else was removed.

Method: documentation only; no commands were run.
