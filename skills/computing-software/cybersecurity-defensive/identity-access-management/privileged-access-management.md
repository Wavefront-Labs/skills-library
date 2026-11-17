---
id: computing-software.cybersecurity-defensive.identity-access-management.privileged-access-management
name: privileged-access-management
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [pam, privileged-access-management, just-in-time-access, vaulting, session-recording, tier-0, tiered-admin-model, service-accounts, break-glass, credential-rotation, cyberark, standing-privilege]
level: advanced
status: draft
description: "Reduce standing privilege with a PAM program: vaulting, just-in-time elevation, tiered admin model, service-account lifecycle, and break-glass accounts that don't become the real backdoor."
sources: ["Microsoft - Securing Privileged Access tiered model (public docs)", "NIST SP 800-53 - AC-6 Least Privilege control family", "CyberArk/BeyondTrust PAM vendor documentation (general public docs)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Privileged access management — eliminate standing privilege, don't just vault it

**Goal:** get privileged accounts out of "always-on admin" and into
checked-out-when-needed, recorded, time-boxed access — vaulting passwords alone
without just-in-time elevation still leaves an attacker who compromises a session
with full standing rights.

## 1. The tiered admin model comes before the tooling
Define tiers before buying/configuring a PAM product: Tier 0 (domain controllers,
identity infrastructure, PKI, PAM itself — compromise here is total), Tier 1
(servers, applications), Tier 2 (workstations). The hard rule that makes this work:
a Tier 0 admin credential is **never used to log into a Tier 1 or Tier 2 asset**,
and a Tier 1 admin never logs into Tier 2 — credential theft on a lower tier then
can't escalate upward (this is specifically what stops "helpdesk admin logs into a
user's infected workstation with domain admin creds, attacker harvests it").
Without this separation, vaulting the password changes nothing structural.

## 2. Just-in-time elevation over standing privilege
Standing admin group membership (permanently in Domain Admins, permanently
sudo-capable) is the single biggest reducible risk in most environments. Move to
just-in-time: a user requests elevation (self-service with approval, or
automatic for low-risk scoped actions), gets time-boxed membership (e.g. 1–4
hours), and is automatically removed — not manually, which rots. This shrinks the
window an attacker who phishes the credential can exploit it as a privileged
account, and makes privileged use auditable by request rather than inferred from
logon events.

## 3. Vault and rotate, but check the rotation actually happens
Password vaulting (checkout, use, auto-rotate after use) stops credential reuse
across sessions and stops anyone memorising a shared admin password. The common
silent failure: rotation jobs fail quietly for accounts the vault can't manage
(a service account whose password is hardcoded in a config file elsewhere, an
appliance with a vendor-specific API) — these show as "rotated" in the vault's
log but the actual account still has the old password active somewhere.
Reconcile periodically: attempt to use the vaulted current password against the
real system, don't just trust the vault's own rotation success flag.

## 4. Service accounts are usually the weak point
Service accounts tend to accumulate excess privilege (granted broadly "to make it
work" once, never revisited), use non-expiring passwords, and often aren't owned
by anyone who remembers what they do. Run a service-account inventory with an
owner, a documented purpose, and a review cadence; migrate what you can to
managed identities (cloud) or group-managed service accounts (Windows gMSA) which
rotate automatically and can't be used interactively — removing the "someone knows
this password" risk entirely for those.

## 5. Break-glass accounts
Keep a small number of emergency accounts (for when the PAM system or SSO itself
is down) in a physically/procedurally separate control — sealed envelope, split
knowledge, or a separate vault with alerting on any access. A break-glass account
used routinely because the normal PAM workflow is "annoying" has become the real
privileged access path and defeats the whole program; alert on every use and
require same-day justification.

## Gotchas
- PAM session recording that isn't actually monitored or reviewed is theatre —
  decide who reviews recordings and on what trigger (random sample, every Tier 0
  session, alert-driven) before assuming the recording itself is a control.
- A "temporary" standing exception for a legacy app that can't support
  just-in-time becomes permanent without an expiry and review owner — same
  discipline as the exception-and-exposure-tracking pattern in vulnerability
  management.
- Local admin rights on workstations (separate from domain privilege) are
  frequently forgotten in a PAM rollout that focuses only on domain/cloud admin —
  local admin is still a privilege escalation path (credential dumping,
  persistence) and belongs in the same program.
- Emergency/break-glass credentials that are never rotated after creation are a
  standing risk hiding behind the "it's for emergencies" label.

## Verify
- [ ] Tiering is enforced technically (credential/logon restrictions), not just
      written in a policy document.
- [ ] Standing privileged group membership has been replaced with just-in-time
      elevation for the majority of admin accounts.
- [ ] Vault-reported rotation success was spot-checked against the real system,
      not trusted blindly.
- [ ] Service accounts have a named owner, documented purpose, and review date.
- [ ] Break-glass account use triggers an alert and same-day justification.

Related: computing-software.cybersecurity-defensive.identity-access-management.sso-and-mfa-rollout,
computing-software.cybersecurity-defensive.security-architecture.zero-trust-segmentation,
computing-software.cybersecurity-defensive.security-operations.incident-response-coordination
