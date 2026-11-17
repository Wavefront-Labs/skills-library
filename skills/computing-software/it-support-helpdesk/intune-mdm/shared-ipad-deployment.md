---
id: computing-software.it-support-helpdesk.intune-mdm.shared-ipad-deployment
name: shared-ipad-deployment
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, shared-ipad, managed-apple-account, ade, guest-sessions, ipados, apple-enrollment]
level: practitioner
status: docs-checked
description: "Deploy Shared iPad with Intune: ADE profile without user affinity, Entra federation, device vs user policy scope, temporary sessions, device-licensed apps, limits."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/device-enrollment-shared-ipad"
  - "https://support.apple.com/guide/deployment/shared-ipad-overview-dep9a34c2ba2/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# shared-ipad-deployment

Shared iPad lets several people use one supervised iPad, each with their own user partition (apps, data, preferences), or a guest temporary session. Common in schools, retail and shift work.

## Requirements
- Supervised iPad enrolled with automated device enrollment (ADE) and without user affinity. Apple lists at least 32 GB storage and supports all iPad Pro models, iPad (5th generation) or later, iPad Air 2 or later, iPad mini (4th generation) or later. Not supported on iPhone.
- Intune's page says iPadOS 13.4 and later (and elsewhere 13.3); sending a Shared iPad enrollment policy to an unsupported device requires a wipe.
- Managed Apple Accounts issued by the organisation. Federating Microsoft Entra with Apple Business or School Manager lets users sign in with their Entra username and password; a Managed Apple ID matching the Entra username is created at first sign-in, and the user sets an alphanumeric passcode for their partition. Follow Apple's federated authentication guide for the Apple-side steps (the cited Apple page for it was not readable).

## Intune configuration
1. Devices > By platform > iOS/iPadOS > Device onboarding > Enrollment > Bulk Enrollment Methods > Enrollment program tokens > the token > Profiles > Create profile > iOS/iPadOS. In Management settings set **User affinity: Enroll without user affinity**, **Supervised: Yes**, **Shared iPad: Yes**. Save, then assign devices synced from Apple Business.
2. Optionally create a dynamic device group with rule property `enrollmentProfileName` equal to the profile name, and assign required apps and profiles to it.
3. Prepare devices: turn on new devices, or factory reset existing ones, and follow the setup prompts.
4. Temporary sessions are allowed by default; the device restriction "Block Shared iPad temporary sessions" is device-only. See Intune's "Shared iPad - Automated device enrollment (supervised)" settings list for quota and timeout options.

## Device vs user applicability
- Device-assigned policies apply to any active user and to temporary sessions; they apply on device sync or check-in.
- User-assigned policies apply when a federated user signs in, and are not reported per user in Intune.
- User-applicable settings: home screen layout, app notifications, single sign-on app extension, email (but email profiles are not supported, see limitations), and most device restrictions. Device-only: AirPrint, lock screen message, web content filter, Block Shared iPad temporary sessions, defer software updates, force automatic date and time, block auto lock, and VPN, Wi-Fi and certificate profiles.
- Configure each setting once; with conflicting values the winner can't be predicted.

## Apps
- Assign line-of-business apps and device-licensed VPP or custom apps to Entra **device** groups as Required. User-licensed VPP apps, App Store apps and Available assignments do not work. Web apps are user-group assigned only.
- To show or hide apps per role, assign all apps to the device group and use allowed/blocked app lists on user groups.

## Known limitations (from the Intune page)
- Company Portal app and website are not supported.
- App Store installs are disabled; Intune recommends disabling the App Store in a profile.
- Passcodes must be eight alphanumeric characters and Intune complexity settings don't apply; only the grace period can be set.
- Not supported: app-based and device-based Conditional Access, app protection policies, compliance policies, email profiles.
- Temporary sessions delete all data (including browsing history) at sign-out and may not support apps needing iCloud or cloud storage; purchased books cannot be assigned in temporary sessions.

## Support cases
- Sign-in fails: the user may lack a federated Managed Apple Account; check federation for that domain in Apple Business or School Manager.
- Apps missing: confirm they are Required, device-licensed and assigned to the device group.
- Profile not applying to a user: user-group policies need the Managed Apple ID to match the Entra UPN.

## Verify
Two different users sign in, see their own data and required apps, and sign out; the sign-in screen offers the Guest option unless blocked; the device syncs in Intune.

## Checked
Method: documentation only; no commands were run. Checked 2026-11-08 against the Intune Shared iPad page and Apple's Shared iPad overview (both read in full). Corrected: 32 GB was framed as "64 GB+ realistic" and quotas/user-session timeouts and Delete user actions were asserted without support; removed those, the "Unable to sign in via directory sync" claim, the ABM menu path, the claim that switching modes needs an erase, and the cached-user cleanup actions. The Apple federation page returned only a stub, so its details are deferred to Apple's guide.
