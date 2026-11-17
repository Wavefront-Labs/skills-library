---
id: computing-software.it-support-helpdesk.intune-mdm.mam-policy-not-applying-troubleshooting
name: mam-policy-not-applying-troubleshooting
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, mam-troubleshooting, app-protection-policy, company-portal, app-protection-status, intune, app-protection-reports, policy-delivery-timing]
level: practitioner
status: docs-checked
description: "Find why Intune app protection isn't applying: licence, user targeting, SDK-enabled app, work-account sign-in, Android Company Portal, delivery timing and the status report."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/mem/intune/app-protection-policies/troubleshoot-app-protection-policy-deployment
  - https://learn.microsoft.com/en-us/mem/intune/apps/app-protection-policies-validate
  - https://learn.microsoft.com/en-us/mem/intune/apps/app-protection-policy-delivery
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# mam-policy-not-applying-troubleshooting

## Collect first
Which setting or policy is missing, all users or some, which platform, which apps (LOB apps built with the Intune App SDK versus store apps), when it started, and whether the device uses Intune, a third-party MDM or none.

## Checklist (Microsoft's flow)
1. **Prerequisites**: the user has an Intune licence and is in a security group targeted by an app protection policy that also targets the app. Android needs the Company Portal app to receive policies. Word, Excel and PowerPoint also need a Microsoft 365 Apps licence and a managed save location (for example OneDrive, which must also be targeted). On-premises Exchange or Skype for Business needs Hybrid Modern Authentication.
2. **Status**: Apps > Monitor > App protection status > Assigned users tile > Select user. It shows licence state, Microsoft 365 licence, targeted apps, policies, check-in state and last sync. Statuses are Checked in and Not checked in. Policies apply only in the work context.
3. **User targeted**: policies target users or user groups, not device groups. Check Groups > the group > Members and the exclusion groups. A newly targeted user can take up to 24 hours to appear in reports. On Android Enterprise only personally-owned work profiles support app protection policies. With Apple ADE, User Affinity must be enabled.
4. **App targeted**: the app must use the Intune App SDK and be in Microsoft Intune protected apps. Keep LOB apps on the latest SDK. On Android the Company Portal is the policy broker, so keep it current.
5. **Signed in with the corporate account**: identity must match between app and SDK. A UPN that differs from the Entra UPN breaks policy; Microsoft recommends matching the UPN to the primary SMTP address and using modern authentication. Only one work or school account per device is supported.
6. **Device data**: on iOS or Android, in Microsoft Edge go to `about:intunehelp`, then View Intune App Status (a bare version and timestamp means no policy is applied to that app) or Get Started to collect logs for a Microsoft support ticket.

## Timing
| User state | Retry interval |
|---|---|
| Tenant not onboarded | 24 hours |
| User not licensed | 12 hours (24 hours on Android SDK older than 5.6.0) |
| No policy assigned, or app not in the policy | 12 hours |
| Registered | Typically 30 minutes |
Retries need the app to be in use. Apps not checked in for 90 days may be deregistered and re-register on next launch. Selective wipe is checked every 30 minutes, but changes to existing policy for signed-in users can take up to 8 hours; signing out and in, or restarting, speeds it up. Failed registration from network problems retries at lengthening intervals up to 60 minutes.

## iOS managed devices
When a policy targets only Intune-managed apps on iOS, app configuration must also deliver IntuneMAMUPN and IntuneMAMOID (all MDM-managed apps) and IntuneMAMDeviceID (third-party and LOB apps, value `{{deviceID}}`). If only IntuneMAMDeviceID is set, APP treats the device as unmanaged.

## Checked
Date: 2026-11-08. Read in full: the three cited Learn pages (updated 2026-03-30, 2026-04-14 and 2026-04-14). Removed as unconfirmed: Microsoft Authenticator as an iOS broker, "missing broker is the most common cause", the Troubleshooting + support user tab, Company Portal Help > Send logs, the symptoms table, Conditional Access "blocks before policy applies", and the multi-identity Outlook example.
Method: documentation only; no commands were run.
