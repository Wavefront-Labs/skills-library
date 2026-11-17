---
id: computing-software.networking-hardware-and-wireless.tailscale.device-posture-management
name: device-posture-management
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [device-posture, postures, srcposture]
level: advanced
status: docs-checked
description: "Know the posture attribute types and where posture can be applied."
sources: ["https://tailscale.com/kb/1288", "https://tailscale.com/kb/1324"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Device posture

Goal: base access on device state as well as identity.

**Attributes.** Rules can use pre-populated host information such as OS version, custom attributes set through the postures API, or attributes synced from integrations.

By attribute type:

- Default: all plans.
- Third-party integration (MDM and EDR): Standard, Premium, Enterprise.
- Geolocation: Standard, Premium, Enterprise.
- Custom: Premium, Enterprise.

**Where it applies.** The `postures` section defines posture rules. Reference them with `srcPosture` in access rules. For grants, posture checks apply only to the source (`src`), never the destination.

**Docs-listed uses**

- Limit critical resources to compliant devices, or give elevated access to high-compliance devices.
- Tiered access for managed and unmanaged BYOD devices.
- Continuous verification of device health.
- Monitoring and alerts when postures fail.

**Related automation.** A device approval flow can approve devices that pass a third-party posture check.

**Checklist**

1. Define rules in `postures`.
2. Reference from `src` side only.
3. Confirm attribute availability for your plan.

## Checked

2026-11-09. Confirmed against the Tailscale Device posture management page (attribute sources, plan table, benefits and use cases), the Grants page (posture applies only to src) and the policy syntax page (postures section, srcPosture). Nothing removed.

Method: docs-checked 2026-11-09 against tailscale.com/kb/1288 (Device posture management), kb/1324 (Grants) and kb/1337 (policy syntax), read in full or searched for postures and srcPosture.
