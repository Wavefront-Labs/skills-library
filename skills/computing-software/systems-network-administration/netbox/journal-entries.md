---
id: computing-software.systems-network-administration.netbox.journal-entries
name: journal-entries
category: computing-software
field: systems-network-administration
product: netbox
tags: [journaling, journal-entry, audit-notes]
level: intro
status: docs-checked
description: "Record human notes on objects alongside the automatic change log."
sources: ["https://netboxlabs.com/docs/netbox/features/journaling/", "https://netboxlabs.com/docs/netbox/features/change-logging/", "https://netboxlabs.com/docs/netbox/administration/permissions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Journaling

Goal: keep human context about an object.

All primary and organizational models in NetBox support journaling. A journal is a collection of human-generated notes and comments about an object, maintained for historical context. It supplements the change log, which records automated before and after snapshots.

**Entry fields**

- **Kind**: one of info, success, warning or danger.
- **Comments**: a user-populated text field.

Each entry automatically records the date, time and the user who created it.

**Use for**

- Why a device was moved.
- Notes from an outage.
- Decommissioning comments.

**Permissions.** The permissions documentation shows the `$user` token with a `created_by` constraint as a way to limit users to editing their own journal entries.

**Compared with the change log**

- Change log: automatic, serialized, tied to a request ID.
- Journal: manual, narrative, with a kind label.

**Checklist**

1. Pick the right kind.
2. Write the reason, not the diff.
3. Constrain edit rights with `$user` if needed.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Journaling, Change Logging and Object-Based Permissions pages (all read in full). Removed the unconfirmed claim that journal entries have their own permissions.
