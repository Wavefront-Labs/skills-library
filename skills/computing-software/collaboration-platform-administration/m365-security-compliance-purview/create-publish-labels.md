---
id: computing-software.collaboration-platform-administration.m365-security-compliance-purview.create-publish-labels
name: create-publish-labels
category: computing-software
field: collaboration-platform-administration
product: m365-security-compliance-purview
tags: [create-publish-labels, pv-sensitivity-labels]
level: practitioner
status: draft
description: Define a label taxonomy and publish it with a label policy.
sources: ['https://learn.microsoft.com/en-us/purview/', 'https://learn.microsoft.com/en-us/defender-office-365/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Create and publish sensitivity labels
**Goal:** Define a label taxonomy and publish it with a label policy.

- Purview portal > Information Protection > Labels > Create; set scope (Files and emails, Groups and sites), encryption, content marking.
- Publish via label policy to users/groups; set default label and mandatory labelling.
- Keep 3-5 top-level labels (for example Public, General, Confidential, Highly Confidential).
- Enable labels for SharePoint/OneDrive files in the tenant (`Enable-SPOTenant`-style step per docs, confirm).

## Gotchas
- Policy takes up to 24 hours to reach clients.
- Encryption locks out users who lose rights; test recovery.

## Self-check
Apply the label in Word and confirm marking and permissions.
