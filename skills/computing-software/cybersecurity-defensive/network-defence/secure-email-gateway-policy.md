---
id: computing-software.cybersecurity-defensive.network-defence.secure-email-gateway-policy
name: secure-email-gateway-policy
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [email-security, secure-email-gateway, defender-for-office-365, safe-links, safe-attachments, impersonation-protection, anti-phishing-policy, external-sender-tagging]
level: practitioner
status: draft
description: "Configure email gateway protections: anti-phishing and impersonation, attachment sandboxing, URL rewriting, external tags, quarantine policy and tuning."
sources: ["CIS Control 9 (email and web browser protections)", "Microsoft Learn - Recommended settings for EOP and Microsoft Defender for Office 365", "CompTIA Security+ SY0-701 objective 4.5 (email security, gateway)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure email gateway policy

**Goal:** malicious mail (phishing, malware, BEC) is blocked or neutralised before users act,
with a quarantine and release process that does not overwhelm IT.

## Core protections (Microsoft Defender for Office 365 names; other SEGs have equivalents)
| Control | Setting |
|---|---|
| Anti-spam/malware | Standard or Strict preset security policies; enable zero-hour auto purge (ZAP) |
| Anti-phishing | Impersonation protection for executives and finance staff (user impersonation) and your domains + key partners (domain impersonation); mailbox intelligence; spoof intelligence |
| Safe Attachments | Dynamic Delivery or Block for detonation; apply to SharePoint/OneDrive/Teams too |
| Safe Links | Time-of-click URL checking, do not let users click through, include internal mail |
| Attachment filtering | Block risky types: .iso, .img, .vhd, .exe, .js, .vbs, .hta, .lnk, .one (if not used), macro-enabled from external |
| External tagging | `Set-ExternalInOutlook -Enabled $true` or banner transport rule |
| Authentication | Honour DMARC reject/quarantine from senders; treat failed auth from your own domain as phish |

Use **preset security policies** (Standard/Strict) as the baseline rather than hand-tuned
policies; Microsoft updates them as threats change.

## Quarantine and release
- Users may release spam but only request release for phish/malware; admins review.
- Quarantine notifications periodically, not per message.

## BEC focus
- Rules for payment change requests are process controls (call-back verification), but mail
  flags help: first-time sender to finance, display name matching an executive, reply-to differing from From.

## Tuning
- Allow lists (tenant allow/block list) only with expiry; never allow whole consumer domains.
- Review false positives and false negatives weekly via submissions (`Report message` data).

## Gotchas
- Third-party SEGs in front of Microsoft 365 need enhanced filtering (skip listing) configured or Microsoft sees the SEG's IP and spoof/SPF checks break.
- Transport rules that bypass filtering for "trusted partners" are a favourite abuse path.
- Safe Links rewriting breaks some signed messages and links in calendar invites; test.

## Verify
- [ ] Configuration analyser (Defender) shows no deviations from Standard/Strict presets.
- [ ] Test messages (EICAR attachment, phishing simulation URL) are blocked or rewritten.
