---
id: computing-software.it-support-helpdesk.remote-support-tools.securing-vendor-and-admin-remote-access
name: securing-vendor-and-admin-remote-access
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, tiered-admin-model, vendor-remote-access, rmm-compromise, privileged-access, third-party-access, incident-response]
level: practitioner
status: draft
description: "Secure support access with a tiered admin model, give third-party vendors controlled remote access, and respond fast if the RMM or remote tool is compromised."
sources:
  - "https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model"
  - "https://www.cisa.gov/resources-tools/resources/remote-monitoring-and-management-cyber-defense-guide"
  - "https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-025a"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# securing-vendor-and-admin-remote-access

## Tiered admin model for support staff
- Separate accounts per privilege level: daily account (email, browsing), helpdesk
  account (user and workstation admin), server/infra admin, and identity (tier 0) admin.
- Helpdesk accounts never log on to domain controllers or identity systems; tier 0
  accounts never log on to workstations. Enforce with logon restrictions (GPO deny
  logon rights, Authentication Policy Silos) and Entra role scoping with administrative
  units.
- Elevate just in time with PIM where possible; no standing global admin for the desk.
- Admin work from a privileged access workstation or at least a hardened device, not
  the email-and-browser laptop.

## Third-party vendor remote access
- No shared or permanent vendor accounts. Named accounts, MFA, expiry dates.
- Prefer a brokered method: your remote tool session that you start and watch, a
  privileged access management (PAM) gateway with recording, or a time-boxed ZTNA
  policy to only the systems they support.
- Approval per session or per change ticket; log who connected, when, to what.
- Contract: security requirements, notification of their own breaches, right to audit.
- Remove vendor-installed remote tools found on endpoints (see unapproved tool
  detection) and offer the approved route instead.

## If the RMM / remote tool is compromised
Attackers use RMM consoles to push ransomware to every endpoint at once.
1. **Contain**: disable the RMM console access (SSO app disabled, API keys revoked), stop
   script/automation execution and scheduled jobs; if the vendor is compromised, follow
   their advisory, possibly blocking agent traffic at the firewall.
2. **Preserve**: export audit logs of console logins, scripts run, sessions opened.
3. **Assess**: which devices received scripts or sessions since the earliest suspicious
   login; hunt with EDR for the payload.
4. **Rotate**: all RMM accounts, API keys, credentials stored in the RMM, and any
   credentials typed in sessions.
5. **Restore** access with MFA enforced, IP restrictions, and least-privilege roles;
   report as a security incident (and to clients for MSPs).

## Verify
Helpdesk accounts can't sign in to tier 0 systems, vendor sessions all have tickets and
recordings, and an RMM compromise runbook exists with tested console-disable steps.
