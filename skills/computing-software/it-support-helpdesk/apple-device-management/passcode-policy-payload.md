---
id: computing-software.it-support-helpdesk.apple-device-management.passcode-policy-payload
name: passcode-policy-payload
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, passcode, passcode-policy-payload, password-policy, restrictions]
level: practitioner
status: docs-checked
description: "Enforce passcode rules with the com.apple.mobiledevice.passwordpolicy payload or the DDM passcode.settings configuration, including User Enrolment limits and macOS-specific keys."
sources:
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.mobiledevice.passwordpolicy.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/declarative/declarations/configurations/passcode.settings.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# passcode-policy-payload

Goal: enforce credential rules on managed devices.
- Profile payload `com.apple.mobiledevice.passwordpolicy` (iOS 4, macOS 10.7 and later; marked deprecated at 27.0). Keys and limits: `forcePIN`, `allowSimple` (default true), `requireAlphanumeric` (default false), `minLength` (0 to 16, default 0), `minComplexChars` (0 to 4, default 0), `maxFailedAttempts` (2 to 11, default 11), `maxInactivity` (0 to 15 minutes; on macOS the maximum is 60), `maxGracePeriod` (minutes, default 0), `maxPINAgeInDays` (1 to 730), `pinHistory` (1 to 50).
- macOS-only keys: `minutesUntilFailedLoginReset` (needs `maxFailedAttempts`), `changeAtNextAuth` (default false; in a device profile it affects all users and admin authentication may fail until the admin password is also reset) and, from macOS 14, `customRegex` with `passwordContentRegex` (ICU syntax, at most 2048 characters) and a localised `passwordContentDescription`. Apple advises using the simpler restrictions whenever possible.
- After the final failed attempt the system locks a macOS device, or erases an iOS, visionOS or watchOS device. The delay starts after the sixth attempt, so a `maxFailedAttempts` of six or lower has no time delay.
- User Enrolment: the payload is allowed on iOS but most keys are ignored. The presence of the payload forces `allowSimple` false, `forcePIN` true and `minLength` 6, and removes the "never" auto-lock option. It is forbidden for macOS User Enrolment.
- DDM equivalent: `com.apple.configuration.passcode.settings` (iOS 15, macOS 13 and later) with keys such as `RequirePasscode`, `RequireAlphanumericPasscode`, `MinimumLength`, `MaximumFailedAttempts`, `MaximumInactivityInMinutes`, `PasscodeReuseLimit` and `ChangeAtNextAuth`.
- Status: `passcode.is-compliant` reports compliance on iOS, visionOS and watchOS (not macOS).
Gotcha: on a User Enrolment the profile keys are mostly ignored, so do not expect `maxFailedAttempts` or `pinHistory` to apply.
Verify: `passcode.is-compliant` reports `true` once the passcode meets the policy (iOS, visionOS, watchOS).

## Checked

Date: 2026-11-07. Read in full: apple/device-management `com.apple.mobiledevice.passwordpolicy.yaml` (all keys, ranges, defaults, the User Enrolment note) and, for `passcode.settings.yaml`, the key names and introduced versions only (searched, not read line by line); `passcode.is-compliant` status was read in the DDM batch. Removed: "macOS enforced at next password change" (only `changeAtNextAuth` does this), "may not apply to accounts bound to an IdP", the Platform SSO sync claim and the shared/kiosk exception advice.
Method: documentation only; no commands were run.
