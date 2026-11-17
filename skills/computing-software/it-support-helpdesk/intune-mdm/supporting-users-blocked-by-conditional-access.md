---
id: computing-software.it-support-helpdesk.intune-mdm.supporting-users-blocked-by-conditional-access
name: supporting-users-blocked-by-conditional-access
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, conditional-access-blocked, conditional-access, entra-sign-in-logs, require-compliant-device, error-53000, error-53003, what-if, intune]
level: practitioner
status: docs-checked
description: "Unblock a user stopped by Entra Conditional Access: read the sign-in log, decode the AADSTS 5300x codes, fix device state, and use What If before exceptions."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/conditional-access/troubleshoot-conditional-access"
  - "https://learn.microsoft.com/en-us/entra/identity/conditional-access/what-if-tool"
  - "https://learn.microsoft.com/en-us/entra/identity-platform/reference-error-codes"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# supporting-users-blocked-by-conditional-access

User says "it says my device doesn't meet requirements". Diagnose from the **sign-in log**,
not from the user's description.

## Step 1: find the sign-in
- Read the error page first; ask for **More Details** on it, which reveals troubleshooting
  information to search the sign-in logs with (request ID, time and date also help a
  support case).
- Entra admin center (at least Reports Reader) > Entra ID > Monitoring & health >
  **Sign-in logs**. Filter by Correlation ID, Username, Date, Resource, or Conditional
  Access = failure.
- On the event, the **Conditional Access** tab lists the policy or policies that
  interrupted the sign-in; the Troubleshooting and support tab may state the reason (for
  example a device that did not meet compliance requirements). Basic Info, Location,
  Device Info, Authentication Details and Additional Details show the data used.

## Common codes
In the browser they appear with the `AADSTS` prefix, for example AADSTS53002.
| Code | String and meaning (error-code reference) | What to do |
|---|---|---|
| 53000 | DeviceNotCompliant: policy requires a compliant device and it is not. | User must enroll with an approved MDM such as Intune; check compliance state. |
| 53001 | DeviceNotDomainJoined: policy requires a domain joined device. | Use a domain joined device. |
| 53002 | ApplicationUsedIsNotAnApprovedApp. | Use an app from the approved list. |
| 53003 | BlockedByConditionalAccess: policies do not allow token issuance. | Review the policy that applied; if unexpected, contact the admin. |
| 53004 | ProofUpBlockedDueToRisk. | User must complete MFA registration. |
| 50076 | UserStrongAuthClientAuthNRequired: MFA required by policy, enforcement or new location. | Retry with MFA. |
| 50079 | UserStrongAuthEnrollmentRequired: managed user must register security info. | Register for MFA. |
Also 53009: application needs to enforce Intune protection policies (troubleshooting page).

## Before making exceptions
1. Run **What If** (Entra ID > Conditional Access > Policies > What If). Identity, target
   resource, device platform and client app are required. Only enabled and report-only
   policies are evaluated, service dependencies are not, and the App ID is needed for
   app matching.
2. Check **service dependencies** and **audience reporting** in the sign-in log: a sign-in
   to Teams can be blocked by a policy on a resource Teams requests, such as SharePoint.
3. Prefer fixing the device or app. Any exception is a policy change by the Conditional
   Access owner; record the ticket.

## Gotchas
- "Require device to be marked as compliant" for all users and all resources blocks users
  who have not enrolled, including access to the Intune portal, and can lock out admins.
- Locked-out admin: another unblocked admin can disable the policy; otherwise raise a
  Microsoft support request.

## Checked
Date: 2026-11-07. Read in full: "Troubleshoot sign-in problems with Conditional Access", the What If tool page, and the AADSTS
error-code reference lines for 50076, 50079, 53000-53004 (searched the 65 KB reference by code rather than reading it end to end).
Removed as unconfirmed: error 530003 and its tag/meaning (the code is not in the reference; tag renamed to error-53003), the
Chrome SSO extension, InPrivate and Safari causes, the `dsregcmd` advice, Users > user > Sign-in logs path, the Blank Device ID
claim, the duplicate-device and token-revocation gotchas, the exclusion-group-with-end-date advice, and the Verify step.
Method: documentation only; no commands were run.
