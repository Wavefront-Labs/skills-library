---
id: computing-software.cybersecurity-defensive.threat-intelligence.defanging-and-safe-ioc-handling
name: defanging-and-safe-ioc-handling
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [iocs, defanging, refanging, safe-handling, malware-sample-handling, ioc-sharing-hygiene]
level: intro
status: draft
description: "Defang and refang indicators safely in reports, tickets and chat, handle malicious URLs and samples without accidental clicks or execution, and keep machine formats clean."
sources: ["FIRST CTI SIG - IOC handling guidance", "ioc-fanger / ioc-finder open-source projects documentation", "CISA - Malware analysis report formats"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Defanging and safe IOC handling

**Goal:** humans cannot accidentally click or execute indicators, while machines still get exact values.

## Defanging conventions
- URL scheme: `http` -> `hxxp`, `https` -> `hxxps`.
- Dots: `evil.example.com` -> `evil[.]example[.]com`.
- IP: `198.51.100.7` -> `198.51.100[.]7`.
- Email: `user@evil.example` -> `user[@]evil[.]example`.
- Some teams also use `[:]//` for scheme separators.
Use defanged values in emails, tickets, chat, reports and wikis; many chat tools auto-link and unfurl otherwise (fetching the URL from corporate infrastructure).

## Refanging
Before loading into tools, refang programmatically (`ioc-fanger`, `ioc-finder`, CyberChef "Fang URL"); a defanged indicator pasted into a blocklist or SIEM search matches nothing. Machine exchange (STIX, MISP, CSV feeds) uses real values in fields - never defanged.

## Sample handling
- Share malware samples in password-protected archives (convention: ZIP with password `infected`) so mail gateways and AV do not quarantine or detonate them; label clearly.
- Store samples in a dedicated repository/sandbox with restricted access; never on general file shares.
- Rename extensions (`.exe_` or `.bin`) to prevent double-click execution.
- Analyse only in isolated VMs/sandboxes without corporate network access.

## Browsing safety
Investigate URLs via urlscan.io (private visibility), sandboxed browsers, or attribution-managed hosts; never from analyst workstations on the corporate network.

## Gotchas
- Partial defanging (`hxxp://evil.example.com`) still auto-links the domain in some tools.
- Wiki and ticket systems that unfurl links fetch the URL even when nobody clicks.

## Verify
- [ ] Report templates and chat snippets use defanged values.
- [ ] TIP ingest refangs automatically and rejects bracketed values.
