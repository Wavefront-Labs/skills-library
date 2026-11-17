---
id: computing-software.collaboration-platform-administration.google-workspace-admin.spam-phishing-delegation
name: spam-phishing-delegation
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [spam-phishing-delegation]
level: practitioner
status: draft
description: Configure spam filters, allowlists and mail delegation.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spam, phishing settings and delegation
**Goal:** Configure spam filters, allowlists and mail delegation.

- Gmail > Spam, phishing and malware: enhanced pre-delivery scanning, attachment safety, spoofing protection.
- Approved senders list and IP allowlist (use sparingly).
- Email delegation: Gmail > User settings > Mail delegation, then users add delegates.
- Quarantines: Gmail > Manage quarantines.

## Gotchas
- Allowlisted IP bypasses spam checks; restrict to known gateways.
- Delegation needs to be enabled for the OU.

## Self-check
A known phishing test is quarantined or flagged.
