---
id: computing-software.it-support-helpdesk.device-provisioning.mobile-device-provisioning
name: mobile-device-provisioning
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, mobile, ios, ipados, android, apple-business-manager, apple-school-manager, vpp, volume-purchase-program, supervised-mode, android-enterprise, work-profile, fully-managed, byod, mam, intune-company-portal, apple-configurator, dep, knox]
level: practitioner
status: draft
description: "Enroll and manage iOS/iPadOS and Android devices: ABM VPP app licensing, supervised mode, Android Enterprise work profile vs fully managed, BYOD boundaries."
sources:
  - "https://support.apple.com/guide/apple-business-manager/welcome/web"
  - "https://developers.google.com/android/management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# mobile-device-provisioning

Goal: get phones and tablets enrolled with the right management level for
who owns them, and license apps correctly — distinct from the
`computing-software.it-support-helpdesk.device-provisioning.onboarding-and-offboarding-devices`
skill's laptop-centric Autopilot/imaging flow.

## Apple: company-owned via Apple Business Manager (ABM)
- Devices purchased through Apple or a reseller enrolled in ABM, or added
  via serial number, are tied to the org automatically on first setup —
  this is **Automated Device Enrollment (ADE)**, the successor name for
  what was "DEP". A device added to ABM cannot be removed from MDM
  supervision by the end user doing a factory reset; it re-enrolls on
  next setup. That's the point — don't treat "I reset it and it's not
  managed anymore" as expected, it means the ABM/MDM link is broken and
  needs fixing, not that the policy worked as designed.
- **Supervised mode** (set during ADE enrollment, not toggleable after
  without a wipe) unlocks restrictions BYOD can't have: disabling
  AirDrop, blocking App Store entirely, silent app installs without user
  interaction, kiosk/single-app mode. If a restriction isn't taking effect,
  check supervision status first — unsupervised devices silently ignore
  supervised-only payloads instead of erroring.
- **Apps and Volume Purchase Program (VPP)**: licenses are bought in ABM
  and assigned either to a device (device-based licensing, app installs
  without an Apple ID — preferred for shared/kiosk devices) or to a user's
  Managed Apple ID (user-based, follows the person across devices). Mixing
  the two models in the same MDM app policy is the most common "app won't
  install" ticket — check which licensing type the app was purchased under
  before troubleshooting the policy.
- **Apple Configurator** is the manual fallback for devices never bought
  through ABM (secondhand, pre-ABM stock) — can still add them to ABM
  retroactively via Configurator, which then lets ADE/MDM take over.

## Android: Android Enterprise
- **Work profile (COPE/BYOD)**: creates a separate, encrypted container on
  the phone — personal apps/data stay outside it, IT only sees and can
  wipe the work container. This is the right mode for BYOD; wiping the
  work profile does not touch personal photos/apps.
- **Fully managed (COBO)**: the entire device is under MDM, no personal
  side — for company-owned phones with no personal use policy. A factory
  reset provisioned via zero-touch (Google's silent re-enrollment for
  company-owned Android, analogous to Apple ADE) re-enrolls automatically
  on wipe; devices not enrolled in zero-touch just come up as a fresh,
  unmanaged phone after reset.
- **Dedicated/kiosk devices**: Android Enterprise's COSU mode locks to one
  or a few apps — common for warehouse scanners, shared devices.
- Samsung Knox adds a vendor layer (Knox Mobile Enrollment, Knox
  Platform for Enterprise policies) on top of Android Enterprise on
  Samsung hardware — check whether a Samsung-specific ticket needs the
  Knox console, not just Intune/your MDM's Android Enterprise policies.

## BYOD boundaries
- Personal devices should only ever get **work-profile (Android)** or
  **MAM without enrollment / app protection policies (iOS/Android)** —
  never full MDM enrollment on a device the user owns outright; full
  enrollment gives IT visibility/wipe power over the whole device, which
  is both a legal exposure and the fastest way to get a BYOD policy
  revoked after a complaint.
- MAM-only (Intune App Protection Policies, no enrollment) enforces PIN,
  encryption, and selective wipe of corporate data inside managed apps
  (Outlook, Teams) without the device ever showing as "managed" — this is
  the correct default for BYOD email/Teams access, not enrollment.

## Gotchas
- A device bought outside the org's normal procurement (user expense,
  secondhand) won't be in ABM/zero-touch and will enroll as BYOD-style
  user-driven unless manually added — check procurement source on any
  "enrollment profile didn't apply" ticket.
- Changing a device's Apple ID after ADE enrollment does not remove MDM
  supervision — Activation Lock and MDM are independent; both need
  clearing (Find My removal + MDM unenroll/retire) before reissuing.
- iOS updates can be deferred/forced via MDM, but a device below the
  minimum OS version for a new management payload will silently fail to
  apply it — check OS version before assuming the policy is broken.

## Verify
- Device shows correct ownership type (corporate-supervised, work profile,
  or MAM-only) in the MDM console, assigned apps install without user
  Apple ID/Google account prompts where device-based licensing was
  intended, and a test wipe/retire removes only the expected data scope.
