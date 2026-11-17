---
id: computing-software.it-support-helpdesk.desktop-support.cloud-service-models-for-support-staff
name: cloud-service-models-for-support-staff
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, virtualization, cloud-service-models, saas, paas, iaas, shared-responsibility, vdi, service-health, cloud-outage, comptia-a-plus]
level: intro
status: draft
description: "Apply IaaS/PaaS/SaaS and shared responsibility to support work: who fixes what, checking provider service health, SaaS outage handling, and VDI/DaaS basics (A+ 220-1201 4.x)."
sources:
  - "https://csrc.nist.gov/pubs/sp/800/145/final"
  - "https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# cloud-service-models-for-support-staff

Goal: when a cloud-hosted thing breaks, know within a minute whether it's
yours to fix, the provider's, or the user's.

## Models (NIST SP 800-145)
| Model | Provider runs | Customer runs | Support examples |
|---|---|---|---|
| **SaaS** | everything up to the app | data, users, access, config | M365, Salesforce, Zoom |
| **PaaS** | runtime, OS, infra | app code, data, access | Azure App Service, databases |
| **IaaS** | hardware, virtualisation, network fabric | OS, patching, apps, data | Azure/AWS VMs |
| **DaaS / VDI** | host infra (DaaS) | images, apps, profiles | Windows 365, AVD, Citrix |
Deployment models: public, private, hybrid, community. Characteristics:
on-demand self-service, broad network access, resource pooling, rapid
elasticity, measured service (A+ terms).

## Shared responsibility in tickets
Always the customer's (your org's) responsibility, even in SaaS: identities
and MFA, access permissions, data classification and retention, endpoint
devices, configuration of the tenant. "Microsoft lost my file" is almost
always a retention/permissions/sync issue on our side.

## Is it the provider? — checks
1. Provider status: Microsoft 365 admin centre → Service health (tenant-
   specific, more accurate than public status pages), Azure Service Health,
   vendor status pages (status.<vendor>.com).
2. Scope: one user / one site / everyone. Everyone + status incident →
   provider.
3. Log the provider incident ID in a parent incident; link child tickets;
   communicate once to all affected.
4. Your configuration changes in the last 24 h (conditional access, DNS,
   firewall) — rule them out before blaming the provider.

## SaaS outage playbook (service desk)
- Post a banner/status message and IVR message early.
- Offer workarounds (web vs desktop client, alternative channel).
- Don't mass-reset passwords or reinstall clients during a provider outage.
- After resolution: confirm with a few affected users, close child tickets
  with the provider's root cause summary.

## Verify
For any cloud-hosted service in your catalogue you can name the model, the
provider's status page, and which parts your team owns.
