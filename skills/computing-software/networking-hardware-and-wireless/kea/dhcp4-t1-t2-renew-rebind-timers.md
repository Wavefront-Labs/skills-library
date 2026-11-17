---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-t1-t2-renew-rebind-timers
name: dhcp4-t1-t2-renew-rebind-timers
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, renew-timer, rebind-timer, t1, t2, calculate-tee-times]
level: practitioner
status: docs-checked
description: "Control whether kea-dhcp4 sends T1 and T2 (options 58 and 59), as fixed values or as percentages of the lease time."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 T1 and T2 timers
RFC 2131 suggests T1 at 50% and T2 at 87.5% of the lease. By default kea-dhcp4 sends neither.

Fixed values: `renew-timer` (T1) and `rebind-timer` (T2), in seconds. T2 is sent only if below the valid lifetime; T1 only if below T2 (when T2 is sent) or below the lifetime (when it is not).

Calculated values:
- `calculate-tee-times`: true to compute from the lease time; default false.
- `t1-percent`: real number 0.0 to 1.0, must be less than `t2-percent`; default 0.50.
- `t2-percent`: must be greater than `t1-percent`; default 0.875.

If explicit values and `calculate-tee-times` are both set, the explicit values win. Where some subnets or shared networks use explicit values and others calculated ones, do not set the explicit values at a scope higher than where they are used: inheriting them from global gives every level beneath explicit values and effectively disables calculation.

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections Sending T1 (Option 58) and T2 (Option 59) in full. Confirmed fixed and calculated values, the defaults and the inheritance note. Nothing removed.

Method: documentation only; no commands were run.
