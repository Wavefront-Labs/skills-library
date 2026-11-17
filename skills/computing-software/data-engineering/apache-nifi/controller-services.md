---
id: computing-software.data-engineering.apache-nifi.controller-services
name: controller-services
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, controller-services, enable-disable, scope, reporting-tasks]
level: practitioner
status: docs-checked
description: "Controller service scope and lifecycle: management services vs process group services, enabling with or without referencing components, disable order, default WARN bulletin."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller services

- Shared by processors, reporting tasks and other services.
- Services created under Controller Settings > Management Controller Services serve only reporting tasks and other services there.
- Services for processors must be defined in the root group or a sub-group where they are used (Configure > Controller Services tab).
- A service must be enabled to run, using the Enable button on its row.
- To modify a running service, disable it together with its referencing reporting tasks and controller services; the Disable dialog can stop or disable the referencing components for you. When enabling, you can enable the service alone or the service and all referencing components.
- Bulletin level defaults to WARN.

Verify: the service shows Enabled and its referencing processors validate.

## Checked

Confirmed against the NiFi user guide (Controller Services; Adding Management Controller Services; Adding Controller Services for Dataflows; Enabling/Disabling Controller Services). Removed the rewording that disabling requires stopping referencing components by hand, since the guide offers to do it in the disable action.

Method: docs-only read of cited pages, 2026-11-08
