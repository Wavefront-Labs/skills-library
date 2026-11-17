---
id: computing-software.it-support-helpdesk.intune-mdm.windows-hello-for-business-deployment
name: windows-hello-for-business-deployment
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, windows-hello-for-business, whfb, cloud-kerberos-trust, pin-reset, biometrics, account-protection, passwordless]
level: advanced
status: docs-checked
description: "Support Windows Hello for Business with Intune: trust models, cloud Kerberos trust for hybrid devices, destructive vs non-destructive PIN reset, and verifying with dsregcmd."
sources:
  - "https://learn.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/"
  - "https://learn.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/deploy/hybrid-cloud-kerberos-trust"
  - "https://learn.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/pin-reset"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# windows-hello-for-business-deployment

WHfB replaces the password at Windows sign-in with a PIN or biometric. Provisioning
requests an asymmetric key pair for the user, from the TPM where available (required if
policy says so), so credentials are not replayable like passwords.

## Configure
- Set WHfB through Intune (the Windows enrolment Windows Hello for Business setting, or a
  settings catalog / account protection policy per group). Look up exact setting names in the
  Intune settings picker rather than trusting a remembered name.
- **Hybrid joined devices** that must reach on-prem resources: the cloud Kerberos trust
  deployment guide (third source) lists the prerequisites and the Entra Kerberos server
  setup. Cloud Kerberos trust is supported on Entra joined and hybrid joined devices; follow
  that guide for the policy to enable on clients.

## Troubleshooting
- Run `dsregcmd /status` and read the Ngc prerequisite section for why provisioning did not
  start; `NgcSet : YES` after provisioning shows a Hello credential exists.
- Hybrid user cannot reach file shares after a WHfB sign-in: check cloud Kerberos trust
  prerequisites from the deployment guide.

## PIN reset
- **Destructive** (default, no configuration): the existing PIN and credentials in the Hello
  container are deleted and a new sign-in key and PIN are provisioned.
- **Non-destructive**: container and keys are preserved; needs the Microsoft PIN reset service
  deployed and client policy enabling PIN recovery. The service relies on Entra identities, so
  it is available only for Entra joined and Entra hybrid joined devices.
- Support for above-the-lock-screen reset depends on trust type (Key trust does not support
  it on hybrid joined devices); see the PIN reset page's table.

## Verify
`dsregcmd /status` shows `NgcSet : YES`; PIN sign-in works; on hybrid devices on-prem shares
open without a password prompt.

## Checked
2026-11-01. Confirmed against the three Learn pages: key pair from TPM, trust types by join
type, destructive default and non-destructive requirements, `NgcSet : YES`. Removed unconfirmed
claims: PowerShell cmdlet and policy names, PIN length, event IDs, certutil container reset,
error message strings, DC patch level, kiosk and camera advice.
Method: documentation only; no commands were run.
