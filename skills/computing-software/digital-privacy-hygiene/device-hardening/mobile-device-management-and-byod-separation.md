---
id: computing-software.digital-privacy-hygiene.device-hardening.mobile-device-management-and-byod-separation
name: mobile-device-management-and-byod-separation
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, mdm, byod, work-profile, android-enterprise, apple-business-manager, apple-user-enrollment, intune, jamf, supervised-mode, mobile-application-management, mam, remote-wipe, selective-wipe, containerization, personal-privacy-at-work]
level: practitioner
status: draft
description: "Keep a personal phone usable when IT enrolls it: understand work-profile containers, what MDM can and can't see, and how to keep personal data out of a corporate wipe."
sources:
  - "https://support.google.com/work/android/answer/10319333"
  - "https://support.apple.com/guide/deployment/user-enrollment-depece845fdd/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MDM and BYOD — keeping work and personal data apart on one device

**Goal:** use a personal phone or laptop for work without IT's management tool
touching your photos, texts or accounts, and without a offboarding wipe deleting
anything personal.

## 1. The two models, and why the difference matters
- **Full/device enrollment (Apple Business Manager "Supervised", Android
  "Device Owner")**: the organisation manages the *entire* device. This is normal
  for a company-issued device, not for your own — if asked to enroll a personal
  phone this way, push back or get a company device instead. A full remote wipe
  erases everything, personal data included, and the admin typically sees the full
  app list and can enforce device-wide policies (password rules, disabled camera,
  blocked app stores).
- **Work profile / User Enrollment (Android Enterprise work profile, Apple's
  "Managed Apple Account" User Enrollment)**: a cryptographically separate
  container. IT manages only what's inside it — work apps, work contacts, work
  mail — and cannot see personal apps, browsing, photos or installed app list
  outside the container. An offboarding wipe removes only the work profile.
  **This is the version to insist on for BYOD.**

## 2. What a work profile actually isolates (and what it doesn't)
- Isolated: app data, notifications content (though notification *presence* may
  still show), copy/paste between profiles is blocked by default, separate
  storage and separate badge/icon treatment for work apps.
- **Not** isolated: the OS itself still sees everything happening on the device
  at the kernel level in theory, but a well-implemented work profile (Android
  Enterprise since Android 11+, Apple User Enrollment since iOS 15) is built so
  the MDM agent's visibility and remote actions are scoped to the managed
  container's APIs — the enterprise is not supposed to get OS-level surveillance
  of the personal side through the MDM API. Treat a security update, jailbreak/root,
  or sideloaded MDM profile outside this model as capable of breaking that boundary.
- On Android, going further than the standard Android Enterprise work-profile
  consent screen (e.g. being told to install a device-admin or accessibility-based
  "MDM" app for a BYOD phone) is a red flag — that older model has full-device
  visibility and is what the work-profile model exists to replace.

## 3. Before you enroll
- Ask explicitly: "full management or work profile/User Enrollment?" Get it in
  writing if the answer matters (e.g. for a contractor).
- Check what the company's MDM policy document says it collects — Apple's User
  Enrollment flow shows this consent screen to you directly before enrollment;
  Android's work-profile setup shows a similar "what your admin can and can't see"
  screen. Read it rather than tapping through.
- Back up personal data before enrolling in anything you're unsure about — a
  mis-enrollment is much easier to recover from with a recent backup.

## 4. Mobile Application Management (MAM) without any enrollment
Some organisations use **MAM** (e.g. Microsoft Intune App Protection Policies)
layered onto normal, unmanaged work apps (Outlook, Teams) instead of full MDM/work
profile. This is lighter-weight: it enforces app-level PIN/encryption and blocks
copy-paste out of the app, with no device enrollment at all. If offered a choice,
this is often the least invasive option for occasional contractors.

## 5. Offboarding
- Confirm in writing what a "remote wipe" will target before it happens — full
  wipe vs. work-profile-only wipe are very different outcomes for your data.
- Remove the work profile yourself (Android Settings → Accounts → work profile →
  Remove; iOS Settings → General → VPN & Device Management → remove the
  management profile) once you no longer need it, rather than waiting for IT.

## Gotchas
- A device-admin-based "MDM" on an older Android version, or a root/jailbreak,
  can give far more visibility than the modern work-profile model — verify which
  model is actually being used, not just that "MDM" is mentioned.
- Disk encryption and screen-lock policies pushed by MDM apply device-wide even
  under a work profile; that's expected and not a privacy issue by itself.
- Uncertain: exact data visible to an admin varies by MDM vendor configuration —
  the platform-level isolation described above is the floor, not a guarantee
  every vendor's dashboard respects it.

## Verify
- [ ] You know whether you were asked for full enrollment or work-profile/User
      Enrollment, and it matches what you agreed to.
- [ ] You read the platform's own "what your admin can see" consent screen before
      enrolling.
- [ ] Personal data was backed up before enrollment.
- [ ] You know in writing what an offboarding wipe will and won't erase.
