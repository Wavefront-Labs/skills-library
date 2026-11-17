---
id: computing-software.collaboration-platform-administration.m365-security-compliance-purview.auto-labeling
name: auto-labeling
category: computing-software
field: collaboration-platform-administration
product: m365-security-compliance-purview
tags: [auto-labeling]
level: advanced
status: draft
description: Auto-apply labels using sensitive info types and trainable classifiers.
sources: ['https://learn.microsoft.com/en-us/purview/', 'https://learn.microsoft.com/en-us/defender-office-365/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Auto-labeling policies
**Goal:** Auto-apply labels using sensitive info types and trainable classifiers.

- Information Protection > Auto-labeling > Create policy; choose sensitive info types and locations.
- Run in simulation, review matches, then turn on.
- Client-side recommended labelling in Office apps is a separate option.
- Service-side labelling has per-day file limits (confirm).

## Gotchas
- Always simulate; auto-labels with encryption can block user access.
- Labelling large libraries takes days.

## Self-check
Simulation results list expected files with no false positives.
