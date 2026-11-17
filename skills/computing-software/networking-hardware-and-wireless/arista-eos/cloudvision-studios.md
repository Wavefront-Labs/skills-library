---
id: computing-software.networking-hardware-and-wireless.arista-eos.cloudvision-studios
name: cloudvision-studios
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, studios, cv-studios, workspace, inventory-and-topology]
level: practitioner
status: draft
description: "Use CloudVision Studios and workspaces to design, review and deploy configuration."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CloudVision Studios and workspaces
Goal: build and deploy via the Studios workflow.

```
# Workflow in CloudVision
Provisioning > Studios > e.g. "Inventory and Topology" > Create Workspace
Add devices / topology > Review > Submit Workspace > Create Change Control > Approve & Execute
```

- Studios hold templates and inputs; Workspaces are Git-like drafts that you review and submit.
- Pre-built studios cover L3 leaf-spine and EVPN (names vary by CloudVision version: confirm).
- Submitting a workspace creates a change control, not an immediate push.
- API/CLI: use the `cloudvision` resource APIs or the Terraform provider (confirm availability).

Gotcha: Workspaces can be abandoned with unsubmitted changes, which hold locks on inputs. Close or delete finished ones.

Operational tip: treat workspace submission like a pull request: have a second person review the generated configuration diff before creating the change control, and delete stale workspaces.

## Verify
- After execution the change control shows `Completed` and devices show compliance.
