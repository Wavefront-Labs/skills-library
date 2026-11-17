---
id: computing-software.it-support-helpdesk.intune-mdm.account-driven-user-enrollment-for-byod
name: account-driven-user-enrollment-for-byod
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, account-driven-user-enrollment, user-enrollment, byod, managed-apple-id, service-discovery, well-known, apple-enrollment, intune]
level: practitioner
status: docs-checked
description: "Set up Intune account-driven Apple User Enrollment for BYOD iPhones/iPads: well-known discovery file, managed Apple IDs, enrollment profile, user steps, Sign-in Failed fix."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/apple-account-driven-user-enrollment"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# account-driven-user-enrollment-for-byod

The user starts enrollment by signing in to their work account in the iOS/iPadOS Settings
app. After they approve management the enrollment profile installs silently and Intune
policies apply. Intune uses just-in-time (JIT) registration and Microsoft Authenticator to
cut repeat sign-ins.

## Prerequisites
1. Platform: iOS/iPadOS 15 or later. A user on 14.9 or earlier who is assigned an account
   driven profile is enrolled automatically with user enrollment with Company Portal.
2. MDM authority set, Apple MDM Push certificate, and **managed Apple IDs** for users.
   Federating Apple Business with Microsoft Entra ID (recommended) means users do not need
   separate Apple IDs and sign in with their work credentials.
3. **Service discovery**: publish a well-known file on the domain users sign in to. Apple
   fetches it with an HTTP GET at `https://<your-domain>/.well-known/com.apple.remotemanagement`.
   - Save it **without a file extension** (no `.json`); content type must be `application/json`.
   - Replace `YourAADTenantID` with your Entra tenant ID. Commercial Intune:
   ```json
   {"Servers":[{"Version":"mdm-byod", "BaseURL":"https://manage.microsoft.com/EnrollmentServer/PostReportDeviceInfoForUEV2?aadTenantId=YourAADTenantID"}]}
   ```
   The page gives the same JSON with host `manage.microsoft.us` for US Government and
   `manage.microsoft.cn` for 21Vianet.
4. Recommended: deploy the Company Portal web app (home-screen link to device status,
   actions and compliance).
5. JIT registration set up and Microsoft Authenticator assigned as a required app (see the
   Intune "Set up JIT registration" article).

## Enrollment profile
Intune admin center > Devices > Enrollment > Apple tab > Enrollment options > **Enrollment
types** > Create profile > iOS/iPadOS. On Settings, Enrollment type is either:
- **Account driven user enrollment**: assigned users are enrolled this way.
- **Determine based on user choice**: user picks "I own this device" (can secure the whole
  device or only work apps and data) or "(Company) owns this device" (Apple Device
  Enrollment).

Assign to all users or specific groups; device groups are not supported because user
enrollment needs user identities. If a user has several profiles, the higher-priority one
applies; reorder by dragging in the Enrollment types list.

## User steps
Settings > General > VPN & Device Management > sign in with work or school account (or the
Apple ID the organization provided) > Sign In to iCloud > enter password > Continue >
**Allow Remote Management**. Wait a few minutes. The work account should then appear under
MANAGED ACCOUNT in VPN & Device Management. Authenticator installs a few minutes after
enrollment; work apps error without it, and the user may be asked to tap Install for apps.

## Failure: Sign-in Failed
Message: "Your Apple ID doesn't support the expected services on this device. Contact your
administrator to sign in." Cause: service discovery not configured correctly. Check the
server returns `Content-Type: application/json` for both:
```text
curl -I "https://contoso.com/.well-known/com.apple.remotemanagement"
curl -I "https://contoso.com/.well-known/com.apple.remotemanagement?user-identifier=firstname.surname@contoso.com&model-family=iPhone"
```

## Unenroll
When the device unenrolls from Intune, the volume and cryptographic keys that manage the
work data are erased.

## Checked
Date: 2026-11-07. Read in full: Intune "Set up account driven Apple User Enrollment" (page updated 2026-11-03). The two Apple
Support sources were not re-read and were dropped. Removed as unconfirmed on the Intune page: macOS 14+ support, the APFS volume
detail, "no redirect", the Can/Cannot table (serial number, UDID, location, passcode), the VPP licence and "Available with or
without enrollment" app claims, the sign-in loop and already-enrolled causes, and the Verify step.
Method: documentation only; no commands were run.
