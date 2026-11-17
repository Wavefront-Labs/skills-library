---
id: computing-software.cybersecurity-defensive.endpoint-security.av-signature-updates
name: av-signature-updates
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [signature-updates, security-intelligence-updates, defender-update-channels, platform-updates, wsus-definitions, antimalware]
level: practitioner
status: draft
description: "Manage anti-malware security intelligence and platform updates: sources and fallback order, gradual rollout channels, offline/air-gapped updating, and stale-definition alerts."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-updates", "https://learn.microsoft.com/en-us/defender-endpoint/manage-protection-updates-microsoft-defender-antivirus", "https://learn.microsoft.com/en-us/defender-endpoint/manage-gradual-rollout"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security intelligence update management

## Update types (Microsoft Defender Antivirus)
- **Security intelligence** (definitions): multiple times a day.
- **Engine** and **platform** updates: monthly.
Cloud-delivered protection reduces dependence on local definitions, but offline devices rely on them.

## Sources and fallback order
`Set-MpPreference -SignatureFallbackOrder "MicrosoftUpdateServer|MMPC|InternalDefinitionUpdateServer"`
Sources: Microsoft Update, WSUS/ConfigMgr (InternalDefinitionUpdateServer), file share (UNC, `-SignatureDefinitionUpdateFileSharesSources`), MMPC (Microsoft Malware Protection Center direct download).
Check interval: `-SignatureUpdateInterval 4` (hours).

## Gradual rollout channels (Intune/GPO)
Platform and engine channels: Beta, Current Channel (Preview), Current Channel (Staged), Current Channel (Broad), Critical - time delay.
Put a pilot ring on Preview/Staged, production on Broad; servers on Broad. Definitions can also be staged
(`Security intelligence update channel`).

## Air-gapped / offline
Download `mpam-fe.exe` (and platform updates) on a connected system, scan/verify signature, transfer to a
UNC share in the isolated network, configure the file share source.

## Monitoring
- Defender for Endpoint "Device health -> Antivirus health" report; `Get-MpComputerStatus | Select AntivirusSignatureAge, AntivirusSignatureLastUpdated, AMProductVersion`.
- Alert when signature age > 3 days or platform version is out of support (> 12 months old platforms lose updates).

## Third-party AV
Same principles: internal relay/caching servers, staged rings, stale-definition alerts, offline packages.

## Gotchas
- WSUS approvals not automated for definitions -> fleet goes stale; use an auto-approval rule for Definition Updates.
- Proxy authentication blocks SYSTEM-context downloads; allow update URLs unauthenticated.

## Verify
- [ ] No device with signature age > 3 days (or documented offline exception).
- [ ] Pilot ring receives platform updates before broad ring.
