---
id: computing-software.cloud-infrastructure-engineering.azure.conditional-access-troubleshooting-sign-in-logs-and-aadsts-codes
name: conditional-access-troubleshooting-sign-in-logs-and-aadsts-codes
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, conditional-access, ca-troubleshooting, ca-sign-in-logs, aadsts-errors, entra-id, what-if]
level: practitioner
status: gated
description: "Diagnose why a sign-in was blocked or prompted: sign-in log CA tab, AADSTS codes, KQL over applied policies, sign-in diagnostic and the What If tool."
sources: ["https://learn.microsoft.com/entra/identity/conditional-access/troubleshoot-conditional-access", "https://learn.microsoft.com/entra/identity-platform/reference-error-codes", "https://learn.microsoft.com/entra/identity/monitoring-health/concept-sign-in-diagnostics-scenarios"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshoot Conditional Access

**Goal:** answer "why was I blocked / asked for MFA again" with evidence in minutes.

## 1. Get the sign-in
From the user's error page copy the **Correlation ID / Request ID / timestamp**, then find the event in the
Microsoft Entra sign-in logs.

## 2. Read the sign-in record
- *Conditional Access* tab: the specific policy or policies that interrupted the sign-in, with their results.
- *Basic info, Location, Device info, Authentication details, Additional details* tabs hold the supporting data.
- The sign-in diagnostic is under **Basic info > Troubleshoot Event**.

## Common codes (error-code reference)
| Code | Name | Meaning |
|---|---|---|
| 53003 | BlockedByConditionalAccess | Access blocked by Conditional Access policies |
| 53000 | DeviceNotCompliant | Policy requires a compliant device |
| 53001 | DeviceNotDomainJoined | Policy requires a domain-joined device |
| 50076 | UserStrongAuthClientAuthNRequired | Admin configuration requires MFA |
| 50079 | UserStrongAuthEnrollmentRequired | User must register for MFA |
| 50074 | UserStrongAuthClientAuthNRequiredInterrupt | Strong authentication required, MFA challenge not passed |
| 50057 | UserDisabled | Account disabled (not a policy problem) |
| 50158 | | External security challenge not satisfied |
Microsoft publishes a lookup at `login.microsoftonline.com/error?code=<number>`; codes and messages can change.

## KQL across many sign-ins
Log Analytics `SigninLogs` has a `ConditionalAccessStatus` field and a `ConditionalAccessPolicies` array; the exact
property names for filtering per policy result were not confirmed on the fetched pages
(gated: unconfirmed, source is paywalled or blocked). Check the schema in your workspace before relying on a query.

## 3. Reproduce safely
- **What If** tool in Conditional Access: pick user, app, location and conditions to see which policies would apply.
- Use report-only policies to test impact; their results show in the Conditional Access tab.
- Check the audit logs for recent policy changes.

## Gotchas
- Location conditions use the IP Entra sees, often a proxy or VPN egress, which may not be in your named locations.
- Check non-interactive sign-ins as well as interactive ones when a refresh fails.

## Verify
- [ ] Root cause tied to a specific policy + unsatisfied control, and What If confirms the fix.

## Checked
2026-10-28. Confirmed (Learn: troubleshoot-conditional-access, reference-error-codes): CA tab, other record tabs, Troubleshoot
Event path, error-code names and meanings above, error?code lookup URL, report-only. Corrected: sign-in diagnostic was
placed under "Diagnose and solve problems". Removed: the 53003 fix advice, Intune/hybrid-join remediations, KQL
mv-expand example, log-lag claim, exact audit-log activity name. Gated: SigninLogs property names. Name for 50158 is not given in the page.
Method: documentation only; no commands were run.
