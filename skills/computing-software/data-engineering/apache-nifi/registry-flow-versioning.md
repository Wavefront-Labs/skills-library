---
id: computing-software.data-engineering.apache-nifi.registry-flow-versioning
name: registry-flow-versioning
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, nifi-registry, version-control, registry-client, flow-versions]
level: practitioner
status: docs-checked
description: "Version-control process groups with NiFi Registry: registry clients, version states, root group limit, import parameter context default, and local-change rules."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flow versioning with NiFi Registry

- Register a client in the NiFi Settings window, Registry Clients tab (+ button): name, type, optional description.
- Start version control: right-click the process group, Version, Start version control; pick Registry and Bucket, name the flow, Save creates Version 1. The root process group cannot be placed under version control.
- Version states: Up to date, Locally modified, Stale, Locally modified and stale, Sync failure. The Process Groups tab of the Summary page also shows them; right-click the canvas and Refresh for the latest states.
- Show, revert or commit local changes from the Version context menu. "Change version" is only available once local changes are reverted.
- Not counted as local changes: starting or stopping processors, modifying sensitive property values, modifying remote process group URLs, and assigning, creating, modifying or deleting parameter contexts or variables (variables are being removed in a future release).
- On import, "Keep Existing Parameter Contexts" is the default (contexts of the same name are reused); unchecking it creates a new, independent set filled from the registry snapshot.
- A sensitive parameter's value is not sent to the registry, only that a property references it.

Verify: after commit, the group shows Up to date, and a second instance can import the same version.

## Checked

Confirmed against the NiFi user guide (Versioning a DataFlow: Registry Clients, version states, Import, Start Version Control, Managing Local Changes, Change Version).

Method: docs-only read of cited pages, 2026-11-08
