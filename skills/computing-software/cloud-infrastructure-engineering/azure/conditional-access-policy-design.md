---
id: computing-software.cloud-infrastructure-engineering.azure.conditional-access-policy-design
name: conditional-access-policy-design
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, conditional-access, mfa, authentication-strength, phishing-resistant-mfa, named-locations, identity-protection, sign-in-risk, user-risk, report-only, what-if, break-glass, device-compliance, hybrid-joined, session-controls, sign-in-frequency, token-protection, continuous-access-evaluation, cae, security-defaults, zero-trust]
level: advanced
status: draft
description: "Build a Conditional Access baseline: MFA/phishing-resistant strength by persona, risk-based policies, report-only rollout, break-glass exclusions and CAE."
sources: ["Microsoft Learn - Conditional Access policy templates and common policies", "Microsoft Learn - Authentication strengths", "Microsoft Learn - Conditional Access report-only mode", "Microsoft Learn - Microsoft Entra ID Protection risk-based policies", "Microsoft Learn - Continuous access evaluation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conditional Access — a baseline you can roll out without locking the tenant

**Goal:** every sign-in meets a policy you can explain; admins use phishing-resistant MFA;
no policy ever ships straight to *On*.

## 1. Baseline policy set (name them with numbers; order is only for humans)
| # | Policy | Users | Grant/Session |
|---|---|---|---|
| CA001 | Require MFA for all users | All users, exclude break-glass + sync account | Require **authentication strength: MFA** |
| CA002 | Phishing-resistant MFA for admins | Directory roles (GA, PRA, SA, Exchange/SharePoint admin, CA admin, etc.) | Strength: **Phishing-resistant** (FIDO2, Windows Hello, CBA) |
| CA003 | Block legacy authentication | All users | Client apps: Exchange ActiveSync + Other clients → **Block** |
| CA004 | Require compliant or hybrid-joined device for M365 | All users (pilot group first) | Require one of: compliant device, hybrid joined |
| CA005 | Block high sign-in risk / require MFA medium | All users | Sign-in risk High → Block; Medium → MFA |
| CA006 | High user risk → password change | All users | Require password change (needs SSPR + PHS) |
| CA007 | Block unapproved countries | All users | Named locations (countries) not in allow list → Block |
| CA008 | Sign-in frequency on unmanaged devices | All users, filter: device not compliant | Session: frequency 1 h, no persistent browser |
| CA009 | Protect Azure management | Target resource: Windows Azure Service Management API | Strength MFA + compliant device |
Security defaults must be **off** before CA policies apply.

## 2. Rollout mechanics
1. Create every policy in **Report-only**. Wait ≥ 7 days; read `SigninLogs | where
   ConditionalAccessStatus == "reportOnlyFailure"` in Log Analytics, or the *Insights and
   reporting* workbook. Fix exclusions, then enable.
2. Use **What If** with a specific user/app/location/platform before enabling anything
   that blocks.
3. Exclusions: two break-glass accounts (excluded everywhere), the Entra Connect sync
   account (from MFA/device policies), and a `CA-Exclusions-<policy>` group with an
   access review on it. Never exclude *All guests* casually.
4. Templates (`Conditional Access > New policy from template`) cover 1–6 above; they
   create in report-only by default.

## 3. Conditions worth knowing
- **Authentication strength** replaces plain "Require MFA" — define a custom strength if
  you need to exclude SMS. SMS/voice are the weakest allowed methods; disable them in
  *Authentication methods* policy once Authenticator is rolled out.
- **Filter for devices** (`device.deviceOwnership -eq "Company"`, `device.extensionAttribute1`)
  lets you target privileged access workstations.
- **Named locations**: mark corporate IPs as *trusted* so Identity Protection stops flagging them;
  country lookup can use GPS from Authenticator (`Determine location by GPS`).
- **Continuous access evaluation**: enabled by default for Exchange/SharePoint/Teams/Graph —
  revokes tokens within minutes on user disable, password change, or leaving a trusted IP
  (with *strictly enforce location policies* on). Non-CAE apps keep a 1 h token.
- **Token protection** (preview/GA by platform): binds tokens to the device — Windows + Office
  only; don't enable tenant-wide.
- Workload identities (service principals) need a separate *Conditional Access for workload
  identities* licence; policies there only support block/location/risk.

## 4. Identity Protection inputs
P2 feature. Sign-in risk (atypical travel, anonymous IP, token anomaly, password spray)
and user risk (leaked credentials — requires PHS). Use the CA risk conditions, not the
legacy Identity Protection policies (those are being retired). Dismiss/confirm risk from
*Risky users* so the model learns; auto-remediation via password change clears user risk.

## Gotchas
- Policy evaluation is **AND across policies**: a user hit by CA001 and CA004 must satisfy both.
  Blocks always win over grants.
- "All cloud apps" + require compliant device will block Intune enrolment itself unless
  Microsoft Intune Enrollment is excluded.
- Excluding a user from one policy but not another is the usual "why am I still prompted".
- Report-only can still trigger the Authenticator prompt for strength policies that evaluate
  device state — tell the pilot group.
- Rename nothing until the SIEM queries that key on policy display names are updated.

## Verify
- [ ] Report-only 7-day review shows zero unexpected `reportOnlyFailure` for break-glass/service accounts.
- [ ] Legacy auth sign-ins in `SigninLogs` drop to 0 after CA003.
- [ ] Admin sign-in with SMS OTP is rejected; FIDO2 succeeds.
- [ ] Disabling a test user revokes Teams/Outlook access within ~5 min (CAE).
