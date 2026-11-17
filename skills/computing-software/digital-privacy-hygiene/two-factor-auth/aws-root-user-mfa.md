---
id: computing-software.digital-privacy-hygiene.two-factor-auth.aws-root-user-mfa
name: aws-root-user-mfa
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, aws-root-mfa, security-keys, account-hardening-programs]
level: practitioner
status: docs-checked
description: "Lock down an AWS root user: register several MFA devices including a security key, avoid root access keys, use a group email and stop daily root use."
sources:
  - "https://docs.aws.amazon.com/IAM/latest/UserGuide/enable-virt-mfa-for-root.html"
  - "https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html"
  - "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AWS root user MFA

**Goal:** the account owner credential that has complete access to every resource in the
account is protected by MFA, ideally several devices, and used only for tasks that need it.

## Steps
1. Sign in as root, choose your account name in the navigation bar, then **Security
   credentials**.
2. In **Multi-factor authentication (MFA)**, choose **Assign MFA device** and give it a
   device name. Supported types are a passkey or FIDO security key, an authenticator
   app (virtual MFA) and a hardware TOTP token.
3. Register more than one device: up to eight MFA devices of any mix of supported types
   can be attached to the root user, and AWS strongly recommends several for resilience.
4. For an authenticator app, scan the QR code or use **Show secret key**, then type two
   consecutive six-digit codes (wait for the code to change between them) and choose
   **Add MFA**. Submit promptly; if you wait too long the device is out of sync and must
   be resynced.
5. **Access keys:** do not create root access keys. For programmatic use, AWS suggests
   `aws login` with root credentials for temporary credentials, or an admin identity.
6. Create an administrative user in IAM Identity Center (or use IAM roles for a single
   standalone account) for daily work.
7. Root email: use a business-managed address that forwards to a group and is not used
   for anything else.

## Context
- MFA is enforced for root users of all account types (standalone, management, member);
  register it within 14 days of the first console sign-in attempt if not already enabled.
- Consider multi-person approval so nobody holds both the root password and the MFA.
- Do not store the root password in a tool that depends on an AWS account reached with
  that same password.

## Organisations
For member accounts in AWS Organizations, you can centralise root access: remove the
root password, access keys, signing certificates and MFA from member accounts, and do
root-only tasks from the management account. Member accounts then cannot sign in as root
or recover the root password unless account recovery is enabled.

## Verify
- [ ] The MFA section lists at least two devices for the root user.
- [ ] No root access keys exist.
- [ ] Monitoring is in place: AWS Config managed rules, Security Hub CSPM controls or
      Trusted Advisor can report root MFA and root access keys.

## Gotchas
- If you lose all MFA devices you need the phone number and email on the account to be
  current and reachable to recover the MFA; failing that, you must contact customer
  service to remove MFA protection.
- Root password resets go to the root email inbox; keep that inbox and the registered
  phone number under different groups of people so no one person controls both recovery
  channels.

## Checked
Checked 2026-11-08 against the three cited IAM User Guide pages (enable virtual MFA for
root, root user best practices, AWS account root user). Removed: alternate contacts step
(the pages say alternate contacts do not need root), the credential-report command and
dashboard check, and the "identity verification" wording, none of which the pages state.

Method: docs-only read of cited pages, 2026-11-08
