---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.configuration-ownership-and-change-tracking
name: configuration-ownership-and-change-tracking
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [config-ownership, config-change-tracking, configuration-design, codeowners, gitops, audit-log]
level: practitioner
status: docs-checked
description: "Give every configuration an owner and a versioned, logged history so 'what changed?' is answerable during an incident and rollbacks are confident."
sources: ["https://sre.google/workbook/configuration-design/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration ownership and change tracking

SRE Workbook chapter 14: configuration can affect critical systems, so ensure good user isolation and know
what changes happened. During an incident or postmortem it is helpful to know who changed a configuration
and how the change affected the system, whether the cause was an accident or a malicious actor. Postmortem
culture stays blameless; the purpose is understanding.

## Ownership
- Each configuration snippet should have a clear owner. Example from the chapter: directories owned by a
  single production group; if files in a directory can have only one owner, tracking who changes them is easier.

## Versioning
- Version configuration so you can see what it looked like at any point in time. Checking files into a
  version control system such as Subversion or Git is common practice, and equally important for
  configuration ingested through a web UI or remote API.
- Consider coupling configuration tightly to the software version, so you do not configure features that are
  not yet available or no longer supported.

## Logging changes
- Log both changes to configuration and their application to the system. Committing a new version does not
  always mean it is applied.
- When a configuration change is suspected during an incident, be able to quickly list the full set of edits
  in the change. This enables confident rollbacks and lets you notify parties whose configurations were impacted.
- Storing metadata on how configuration was ingested (for example the original file path) helps find the authors.

## Gotchas
- Changes made outside the versioned path (UI or API edits not recorded) break the trail.
- A shared configuration with no single owner is hard to track; give it one owning group.

## Verify
- [ ] Every configuration directory or snippet has one named owner.
- [ ] You can list every edit that went into a given applied change.

## Checked
2026-11-01. Confirmed against SRE Workbook chapter 14 (Ownership and Change Tracking, versioning, change logging, ingestion metadata).
Removed: the CODEOWNERS and branch protection details, the Grafana annotation curl, the git log, Argo CD and kubectl commands, and the dashboard annotation timing, because no page read states them.
Method: documentation only; no commands were run.
