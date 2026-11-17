---
id: computing-software.cybersecurity-defensive.identity-access-management.windows-hello-for-business-deployment
name: windows-hello-for-business-deployment
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [mfa, windows-hello-for-business, whfb, cloud-kerberos-trust, passwordless, tpm, intune, phishing-resistant-mfa]
level: advanced
status: gated
description: "Deploy Windows Hello for Business: choosing cloud Kerberos trust vs key/cert trust, Intune policy, TPM requirements, PIN rules, on-prem SSO, and troubleshooting provisioning."
sources: ["https://learn.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/", "https://learn.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/deploy/hybrid-cloud-kerberos-trust", "https://learn.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/faq"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Hello for Business deployment

WHfB replaces the Windows password with an asymmetric key bound to the device TPM, unlocked by PIN or
biometrics. It is phishing-resistant MFA for Windows sign-in and Entra apps.

## Choose a trust model
- **Cloud-only** (Entra joined, no AD): simplest.
- **Hybrid cloud Kerberos trust** (recommended for hybrid): Entra issues partial TGTs; requires
  an Entra Kerberos server object for the domain (created with the Microsoft Entra Kerberos PowerShell module),
  plus supported client and DC versions (see the cloud Kerberos trust prerequisites). No PKI needed.
- **Key trust**: needs DCs with certificates; more moving parts.
- **Certificate trust**: AD CS and enrolment infrastructure; only if you need certificates for RDP
  or specific legacy scenarios.

## Configure (Intune)
Devices > Enrollment > Windows Hello for Business (tenant-wide), or a Settings catalog policy:
- Use Windows Hello for Business: enabled; Require TPM (hardware): yes.
- PIN: set a length and complexity policy (it is device-bound, so length beats complexity),
  history, no expiry needed.
- Biometrics allowed; enhanced anti-spoofing on.
- "Use cloud trust for on-prem authentication": enabled (cloud Kerberos trust).
Provisioning happens at next sign-in after an MFA-backed session; users create a PIN.

## Security notes
- TPM-backed keys cannot be exported; prefer TPM 2.0.
- PIN is local to the device; a stolen PIN without the device is useless.
- Lockout: TPM anti-hammering plus Windows lockout policy.
- WHfB counts as phishing-resistant in authentication strengths.
- For shared devices, consider FIDO2 keys instead (WHfB is per user per device).

## Troubleshooting
- `dsregcmd /status`: check the join state, the Hello key (NGC) status and the cloud and on-prem TGT fields (gated: unconfirmed, source is paywalled or blocked)
  for successful on-prem SSO.
- Event Viewer: the Windows Hello for Business and User Device Registration event logs.
- Provisioning not starting: policy not applied, MFA not satisfied, TPM not ready.
- On-prem resource access failing: Kerberos server object missing or DCs unpatched.

## Gotchas
- Remote Desktop with WHfB needs certificate trust or Remote Credential Guard/RDP with Entra auth.
- Disable password sign-in only after WHfB coverage is near complete and recovery paths exist
  (Temporary Access Pass, self-service PIN reset).

## Verify
On a pilot device: `dsregcmd /status` shows the Hello key set and both TGT fields populated; sign-in logs show
"Windows Hello for Business" as the authentication method; file share access works without a password prompt.

## Checked

2026-10-28. Confirmed against the WHfB FAQ and overview pages: cloud Kerberos trust uses an Entra Kerberos server object, TPM 2.0 recommended, TPM anti-hammering lockout, Remote Credential Guard as RDP alternative. Gated: dsregcmd field names. Removed: Windows version and DC 2016 requirements, 6-digit PIN minimum, Set-AzureADKerberosServer name, event log path, Get-Tpm.

Method: documentation only; no commands were run.
