---
id: computing-software.collaboration-platform-administration.google-workspace-admin.drive-dlp-labels
name: drive-dlp-labels
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [drive-dlp-labels]
level: advanced
status: draft
description: Detect and block sensitive content in Drive.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Drive DLP and labels
**Goal:** Detect and block sensitive content in Drive.

- Security > Access and data control > Data protection: create rules with detectors (predefined or regex).
- Actions: warn, block sharing, alert.
- Drive labels classify files; use with DLP rules (edition-dependent).
- Run in audit mode before blocking.

## Gotchas
- Predefined detectors can over-match; tune thresholds.
- Edition limits apply.

## Self-check
Upload a test file with sample numbers and confirm the rule triggers.
