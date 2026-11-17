---
id: computing-software.it-support-helpdesk.intune-mdm.platform-sso-for-macos-with-entra-id
name: platform-sso-for-macos-with-entra-id
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, macos-management, platform-sso, enterprise-sso-extension, entra-id, company-portal-macos, secure-enclave-key, password-sync, app-sso-platform]
level: advanced
status: docs-checked
description: "Deploy Platform SSO on Macs with Entra ID: settings catalog policy, Secure Enclave vs password vs smart card, registration, assignment rules, errors 10001/10002."
sources:
  - "https://learn.microsoft.com/en-us/intune/intune-service/configuration/platform-sso-macos"
  - "https://learn.microsoft.com/en-us/entra/identity/devices/macos-psso"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# platform-sso-for-macos-with-entra-id

Goal: users sign in to the Mac with an Entra method and get SSO to Entra-protected apps. Platform SSO includes the SSO app extension, so do not configure that separately. Included in all Intune licensing plans.

## Prerequisites
- macOS 13.0 or later (Microsoft strongly recommends macOS 14 or later).
- Company Portal for macOS 5.2404.0 or later, deployed as a required app; an older version makes Platform SSO fail.
- Supported browsers: Edge, Chrome with the Microsoft Single Sign On extension, Safari, Firefox (MicrosoftEntraSSO policy).
- Users must be allowed to join devices to Entra. Intune role needs Device Configuration Read, Create, Update, Assign (Policy and Profile Manager has them).
- Devices must be MDM enrolled: ADE or Apple Configurator direct enrollment (corporate), or device enrollment via Company Portal (personal).

## Choose the method (Microsoft recommends Secure Enclave)
| Method | Local Mac password | Notes |
|---|---|---|
| Secure Enclave key (`UserSecureEnclaveKey`) | Unchanged | Passwordless, phishing resistant, Touch ID unlock after first password unlock, usable as passkey; setup can be bootstrapped with an authenticator app or Temporary Access Pass |
| Smart card (`SmartCard`) | Unchanged | macOS 14+; passwordless; not supported in Setup Assistant (register after it) |
| Password (`Password`) | Replaced by and kept in sync with Entra password | macOS 13+; users enter the Entra password after reboot; Intune password policy also applies, so match it to the Entra policy or sync can fail |
The local password is never fully removed because FileVault uses it as the unlock key. Optional KeyVault (Institutional FileVault recovery key) recovery applies to password sync.

## Policy (Devices > Manage devices > Configuration > Create > New policy > macOS > Settings catalog)
Add Authentication > Extensible Single Sign On (SSO), with these values:
- Extension Identifier `com.microsoft.CompanyPortalMac.ssoextension`; Team Identifier `UBF8T346G9`; Type Redirect.
- URLs `https://login.microsoftonline.com`, `https://login.microsoft.com`, `https://sts.windows.net` (plus sovereign cloud URLs if needed).
- Platform SSO > Authentication Method (macOS 14+) `Password`, `UserSecureEnclaveKey` or `SmartCard`; for macOS 13 use "Authentication Method (Deprecated)". With mixed 13 and 14+ devices set both in one profile.
- Platform SSO > FileVault Policy (macOS 15+, Password method) `AttemptAuthentication`; Use Shared Device Keys `Enabled`; Registration token `{{DEVICEREGISTRATION}}`; Screen Locked Behavior `Do Not Handle`.
- Token To User Mapping: Account Name `com.apple.PlatformSSO.AccountShortName` (recommended; UPN prefix) or `preferred_username`; Full Name `name`.

Only one SSO policy can be assigned to a group, so add scenario settings (Kerberos, Touch ID, non-Microsoft apps) to this same policy. Changing Authentication Method or Use Shared Device Keys makes devices reregister.

## Assignment
Devices with user affinity: assign to users or user groups. Device groups or filters are not supported there and can block access to Conditional Access protected resources. Userless multi-user devices: assign to device groups. Unassign any older SSO app extension profile made with the Device Features template once the new one works.

## User experience
After the policy lands, a Registration required notification appears in Notification Center. The user selects it, signs in with the work account and completes MFA if required; the Mac is then Entra joined with a hardware-bound WPJ certificate. Users who ignore the notification stay unregistered.

## Troubleshooting
- Error 10001: SSOe payload misconfigured, a required setting missing or one not valid for a redirect payload; often the macOS 13 vs 14 authentication settings.
- Error 10002: multiple SSOe payloads in conflict; keep only the settings catalog profile.
- Confirm on the device: Settings > Privacy and security > Profiles > com.apple.extensiblesso profile; and the Entra registration status check from Microsoft's docs. See Microsoft's "macOS Platform single sign-on known issues and troubleshooting" for more.
- Optional `enable_se_key_biometric_policy` = true in the extension data forces Touch ID for every Secure Enclave key use, with no password fallback; needs macOS 14.6+ and Company Portal 2504+, and enabling it after registration needs admin-driven re-registration.

## Verify
The device is registered in Entra, the profile shows under com.extensiblesso, and Microsoft 365 web and apps sign in without a password prompt.

## Checked
Method: documentation only; no commands were run. Checked 2026-11-08 against the Intune platform-sso-macos page and the Entra macos-psso overview (both read in full). Removed because the pages do not support them: the app-sso command-line diagnostics and log predicate, the Repair-in-Users-and-Groups fix, the "create user at login" gotcha, the claim that macOS 13 is limited, and the Apple deployment guide source (unchecked).
