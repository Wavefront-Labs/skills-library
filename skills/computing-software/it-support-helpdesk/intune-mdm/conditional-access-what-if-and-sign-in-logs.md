---
id: computing-software.it-support-helpdesk.intune-mdm.conditional-access-what-if-and-sign-in-logs
name: conditional-access-what-if-and-sign-in-logs
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, conditional-access-what-if, conditional-access, sign-in-logs, report-only, device-compliance, entra-id]
level: practitioner
status: docs-checked
description: "Work out which Conditional Access policy blocked a user: sign-in log Conditional Access tab, error codes, the What If tool and its limits, and what to send an admin."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/conditional-access/what-if-tool"
  - "https://learn.microsoft.com/en-us/entra/identity/conditional-access/troubleshoot-conditional-access"
  - "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# conditional-access-what-if-and-sign-in-logs

"Access blocked" tickets are answered from the sign-in log, not by guessing.

## Find the sign-in
1. Sign in to the Microsoft Entra admin center as at least a **Reports Reader**; go to
   Entra ID > Monitoring & health > **Sign-in logs**.
2. The user's error page has a **More Details** option with troubleshooting information
   (including the request ID, time and date) that helps find the exact event.
   Filter by Correlation ID, Conditional Access (limit to failures), Username, Date and
   Resource.
3. Open the event and select the **Conditional Access** tab: it lists the policy or
   policies that interrupted the sign-in. The Troubleshooting and support tab may give a
   clear reason such as a device failing compliance. Basic Info, Location, Device Info,
   Authentication Details and Additional Details hold the user and device data used in the
   evaluation.
4. Select the ellipsis on a policy for details: the left side shows data collected at
   sign-in, the right shows whether it satisfied the policy. A policy applies only when all
   its conditions are satisfied or not configured.
5. Still unclear: Basic info > **Troubleshoot Event** opens the sign-in diagnostic.
- Sign-in logs come in four types: interactive user, non-interactive user, service
  principal and managed identity sign-ins. Entries cannot be changed or deleted.

## Common Conditional Access error codes
| Code | String |
|---|---|
| 53000 | DeviceNotCompliant |
| 53001 | DeviceNotDomainJoined |
| 53002 | ApplicationUsedIsNotAnApprovedApp |
| 53003 | BlockedByConditionalAccess |
| 53004 | ProofUpBlockedDueToRisk |
| 53009 | Application needs to enforce Intune protection policies |
In the browser they appear as `AADSTS` plus the code, for example AADSTS53002.

## What If
Entra admin center > Entra ID > Conditional Access > Policies > **What If**.
- Required conditions: identity, target resource, device platform and client app; the
  other conditions default to none.
- The report lists policies that apply (with the grant and session controls to satisfy)
  and policies that do not apply, with the first condition that was not met.
- Only enabled and report-only policies are evaluated.
- It does not test Conditional Access service dependencies (for example a Teams test
  ignores a policy on Exchange Online).
- It expects all sign-in parameters; supply the App ID, because app groups such as Office
  365 do not match.
- For report-only policies use per-policy reporting or the Conditional Access insights and
  reporting workbook.

## Other causes
- **Service dependencies**: a user can be blocked because an app depends on a resource a
  policy blocks. Check the application and the resource in the sign-in log.
- **Audience reporting**: a sign-in to an app such as Teams requests several resources, and
  policies apply across them. The Audience under Resource, after selecting a policy on the
  Conditional Access tab, shows why a policy applied.
- **Locked-out admins**: another unblocked admin can disable the policy; otherwise raise a
  Microsoft support request.
- **Risky "all users, all resources" settings**: block access, require compliant device,
  require hybrid joined device and require app protection policy can lock out everyone,
  including admins without an enrolled device.

## Escalation to identity admins
Send the UPN, timestamp, correlation or request ID, app, error code, failing policy name,
and device ID and compliance state, not "user can't log in".

## Checked
Date: 2026-11-07. Read in full: What If tool, "Troubleshoot sign-in problems with Conditional Access" and "What are Microsoft
Entra sign-in logs". Removed as unconfirmed: the Security Reader and Conditional Access Administrator role claims, error codes
50076 and 530003, the Device info "blank device ID" Chrome/Edge workaround, the "Report-only: Failure" result label, the
"Protection > Conditional Access" navigation (page says Entra ID > Conditional Access), the "sign-in logs take a few minutes"
and Teams non-interactive claims, advice per error code, and the Verify step.
Method: documentation only; no commands were run.
