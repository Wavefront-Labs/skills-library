---
id: computing-software.networking-hardware-and-wireless.arista-eos.cvp-configlets-containers
name: cvp-configlets-containers
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, configlets, cvp-containers, configlet-builder, tasks]
level: practitioner
status: draft
description: "Organise devices into CVP containers, assign configlets and execute tasks to push config."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CloudVision containers and configlets
Goal: manage configuration centrally.

```
# In CloudVision Provisioning
Tenant > Container (e.g. DC1-Leafs) > Configlets assigned
Device > Assign configlet > Save > Create Task > Execute
```

- Configlets are config snippets; container assignment inherits to all devices below.
- Configlet builders generate configs dynamically (Python).
- Task execution applies the change and produces a rollback snapshot.
- The API (`cvprac` Python library) can script this:

```python
from cvprac.cvp_client import CvpClient
cv = CvpClient()
cv.connect(["192.0.2.90"], "automation", "<password>")
print(cv.api.get_configlets())
```

- CVaaS and CVP on-prem differ in UI; Studios are the newer approach (confirm availability).

Gotcha: configlets assigned at multiple levels merge in order; conflicting lines produce 'config differs from designed' compliance flags. Review the preview before executing tasks.

Operational tip: keep configlets small and role-based, avoid overlaps between container levels, and use configlet builders for anything that depends on device data so values do not drift.

## Verify
- The task completes and the device's Configuration Compliance is shown as compliant.
