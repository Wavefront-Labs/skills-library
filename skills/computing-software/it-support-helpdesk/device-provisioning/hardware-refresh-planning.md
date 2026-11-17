---
id: computing-software.it-support-helpdesk.device-provisioning.hardware-refresh-planning
name: hardware-refresh-planning
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, refresh-cycle, hardware-refresh, lifecycle, budgeting, windows-11-readiness, endpoint-analytics]
level: practitioner
status: draft
description: "Plan hardware refresh from data: lifecycle policy, asset-age and warranty cohorts, health and OS-support signals, budget forecasts, standard models and staggered rollouts."
sources:
  - "https://learn.microsoft.com/en-us/windows/whats-new/windows-11-requirements"
  - "https://learn.microsoft.com/en-us/lifecycle/products/windows-10-home-and-pro"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# hardware-refresh-planning

## Policy
Set lifecycles by device type and role, e.g. laptops 4 years, desktops 5, phones 3,
heavy-workload users 3. Align warranty length to the lifecycle so devices never run out
of cover in service.

## Build the forecast
1. Export the asset register: purchase date, warranty end, model, user, department.
2. Group into quarterly cohorts by refresh due date; multiply by standard model cost
   including accessories and labour.
3. Add signals that pull devices forward:
   - Battery health (wear level over ~20%), repeated repairs.
   - Endpoint analytics (Intune): startup performance and resource performance scores per
     model; app reliability.
   - OS support: devices that cannot run a supported Windows version (Windows 11 needs TPM
     2.0, UEFI Secure Boot and a supported CPU) must be replaced or isolated; Windows 10
     reached end of support in October 2025.
4. Subtract devices to redeploy (good condition, light users) and spares.

## Execution
- Stagger: smooth cohorts so the desk is not swamped (e.g. a fixed number per week).
- Standard catalogue of 2-3 models per tier with vendor supply commitments.
- Autopilot + OneDrive make swaps quick; book users in slots and use self-service
  where possible.
- Old devices: sanitise and redeploy, sell via ITAD, or recycle with certificates.

## Communicate
Publish the schedule to managers; users are more patient when they know their date.

## Gotchas
- Buying all devices in one year creates the same spike every 4 years.
- Leasing ties you to return conditions; track missing accessories.

## Verify
Budget and quarterly plan approved, each cohort's devices listed with users, and actual
refresh progress tracked against plan each month.
