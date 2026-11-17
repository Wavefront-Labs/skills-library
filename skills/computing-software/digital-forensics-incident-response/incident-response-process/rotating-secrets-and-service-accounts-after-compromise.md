---
id: computing-software.digital-forensics-incident-response.incident-response-process.rotating-secrets-and-service-accounts-after-compromise
name: rotating-secrets-and-service-accounts-after-compromise
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [secret-rotation, eradication, leaked-credentials, service-accounts, dfir]
level: advanced
status: docs-checked
description: "Rotate exposed service account passwords, access keys and tokens after an incident: find exposed secrets, order the rotation, monitor old keys, and move to managed identities."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html", "https://learn.microsoft.com/en-us/windows-server/security/group-managed-service-accounts/group-managed-service-accounts-overview", "https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rotating secrets and service accounts after compromise

**Goal:** remove the attacker's non-interactive access. Keys and secrets survive user password resets and are a classic re-entry path.

## Find what was exposed
- Secrets readable on compromised hosts: config files, scripts, scheduled tasks with stored credentials, shared credential files. AWS notes that access keys in the shared AWS credentials file are stored in plaintext, and that you should not put access keys in application files or project areas.
- Secrets in code the attacker could clone: GitHub secret scanning scans the entire Git history on all branches for hardcoded credentials, and also issues, pull requests, discussions, wikis and secret gists. It supports custom patterns and optional validity checks that show whether a detected secret is still active (availability depends on repository type and plan; see the page).
- Secret stores and key usage the attacker may have touched: review their audit logs (practice; the cited pages do not name specific logs). For AWS access keys, AWS recommends monitoring usage with CloudTrail and CloudWatch alarms for denied access attempts.
- CI/CD variables, deploy keys, certificates and private keys are further places to check (practice).

## Rotate (practice: order by blast radius)
1. Highest blast radius first: cloud admin keys, CI/CD tokens, signing keys, service accounts with admin rights.
2. Customer-impacting integrations next, then remaining application secrets.
For each: create the new secret, deploy it to consumers, confirm they are healthy, then revoke the old one and record its identifier so later use can be detected.

## Specifics from the pages
- AWS IAM: an access key has an access key ID and a secret access key, and a user can have at most two access keys. The secret can be retrieved only at creation; if lost, delete the key and create a new one. AWS says to prefer temporary credentials such as IAM roles over long-term access keys, and to review, update and delete keys regularly.
- GitHub: when secret scanning alerts, rotate the credential immediately. GitHub notes that rewriting Git history to remove the secret is time-intensive and often unnecessary once the credential is revoked.
- Active Directory: a group Managed Service Account (gMSA) lets Windows manage the password, and the domain controller computes it from the Key Distribution Service; member hosts obtain current and preceding values from a DC. gMSAs are not applicable to Windows earlier than Windows Server 2012, failover clusters do not support them directly (services on the cluster may use one if they are a Windows service, app pool or scheduled task), and MSAs depend on Kerberos encryption types, so configure AES.

## Verify
- Old keys no longer authenticate, and log entries for the revoked key ID after the revocation time are attempted attacker use.
- List every credential per identity, not just the known one; an attacker may have added their own key or credential.

## Gotchas
- Hard-coded secrets in images and backups come back on restore.
- Moving service accounts to gMSA or roles during recovery removes the stored-password problem.

## Checked
Dated 2026-11-08. Confirmed against the AWS IAM "Manage access keys for IAM users" page (key structure, two-key limit, plaintext credentials file, CloudTrail and CloudWatch monitoring), the Microsoft Learn gMSA overview (password management, KDS, limitations, AES) and the GitHub secret scanning page (scan scope, rotate-first guidance, validity checks, custom patterns). Removed as not on those pages: the CLI verification commands, the Secrets Manager GetSecretValue, event IDs 4625/4771, gitleaks, SAML signing-certificate and AD CS CA rebuild claims, and tool-specific audit-log guidance.
Method: docs-only read of cited pages, 2026-11-08
