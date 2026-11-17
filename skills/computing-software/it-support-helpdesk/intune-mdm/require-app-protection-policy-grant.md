---
id: computing-software.it-support-helpdesk.intune-mdm.require-app-protection-policy-grant
name: require-app-protection-policy-grant
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, require-app-protection, conditional-access, broker-app, authenticator, company-portal, mam]
level: practitioner
status: docs-checked
description: "Build the Conditional Access Require app protection policy grant for iOS/Android: policy steps, OR with approved app, report-only, EAS block, Android Company Portal need."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/conditional-access/howto-policy-approved-app-or-app-protection"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/app-protection-policy"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# require-app-protection-policy-grant

Intune app protection policies (APP) work on devices not enrolled in any MDM, and Microsoft
says to use Conditional Access together with them so the policies are enforced. The
**Require app protection policy** grant is the Conditional Access side of that pairing.

## Policy: approved client app or app protection (mobile)
Entra admin center (at least Conditional Access Administrator) > Entra ID > Conditional
Access > Create new policy:
1. Users: Include All users; Exclude at least one account (the policy cannot be created
   without an exclusion); exclude emergency access/break-glass accounts.
2. Target resources > Include **All resources**.
3. Conditions > Device platforms > Configure Yes > Include Android and iOS.
4. Grant access: select **Require approved client app** and **Require app protection
   policy**, and for multiple controls choose **Require one of the selected controls** (an
   OR: users can use apps supporting either control; the APP control is enforced when the
   app supports it).
5. Create with Enable policy **Report-only**, check impact, then switch to On.
- Report-only sign-in logs can show "Report-only: Failure" on the Conditional Access tab
  even when all conditions were met, because the control is not satisfied in report-only mode;
  once enabled the control applies to the app.
- Also deploy a policy blocking unsupported or unknown device platforms.
- Service accounts and service principals are not blocked by user-scoped policies.

## Block Exchange ActiveSync (basic auth)
Separate policy: All users (with exclusion), target Office 365 Exchange Online, Conditions >
Client apps > Configure Yes, only **Exchange ActiveSync clients**, grant **Require app
protection policy**, start Report-only.

## What the device and app need
- APP is supported on iOS and Android where the app meets requirements, and on Windows (in
  preview, Microsoft Edge only). Not every app supports it; check the list of protected
  apps or ask the app developer.
- iOS and Android devices must first be registered in Microsoft Entra ID.
- Android needs the **Intune Company Portal** installed to receive APP, even without
  enrollment. Android MAM for Microsoft 365 apps needs Entra device registration; users may
  be prompted to authenticate and register.
- The user signs in to the app with their Entra account and must be targeted by an APP for
  that app. APP can be targeted by device management state (for example, unenrolled devices
  only).

## Troubleshooting
Start from the user's Entra sign-in log Conditional Access tab to see which policy and
grant failed. Check that an APP targets the user and app, that the Android Company Portal
is installed, that the device is registered in Entra, and that the client supports APP.

## Checked
Date: 2026-11-07. Read in full: "Require approved client apps or app protection policy" (updated 2026-04-07) and, by searching
(not end to end), the 43 KB App Protection Policies Overview for broker, Company Portal and Conditional Access statements. The
policy-all-users-device-compliance-or-app-protection source returned 404 and was dropped. Removed as unconfirmed: that the
approved client app grant was "retired", the grant OR with device compliance, Microsoft Authenticator as the iOS broker, Teams
dual-app and multi-account gotchas, errors 53005 and 530021, native Mail/Gmail guidance, the "organization is now protecting its
data" message, and the Verify step.
Method: documentation only; no commands were run.
