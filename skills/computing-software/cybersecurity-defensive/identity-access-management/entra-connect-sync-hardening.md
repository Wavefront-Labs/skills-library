---
id: computing-software.cybersecurity-defensive.identity-access-management.entra-connect-sync-hardening
name: entra-connect-sync-hardening
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [identity-lifecycle, entra-connect, cloud-sync, hybrid-identity, password-hash-sync, sync-account, tier-0, msol-account]
level: advanced
status: docs-checked
description: "Harden Entra Connect and Cloud Sync: Tier 0 treatment, sync account permissions, PHS vs PTA vs federation risks, blocking hard-match takeover, and monitoring."
sources: ["https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-install-prerequisites", "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/reference-connect-accounts-permissions", "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-syncservice-features"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Connect / Cloud Sync hardening

The sync server can read password hashes from AD (for PHS) and write to Entra ID. Compromise of it
means compromise of both directories.

## Treat as Tier 0
- Entra Connect server managed like a domain controller: restricted admins, PAW-only access, EDR,
  patched, no other roles, no internet browsing.
- Treat local admins on the server as holding the privileges of the sync accounts.

## Accounts
- **AD DS connector account** (`MSOL_xxxxxxxx` or custom): has "Replicate Directory Changes All"
  for PHS, enabling DCSync. Protect it, scope write-back permissions minimally, and monitor its logons
  (should only come from the Connect server).
- **Entra connector account**: holds
  the Directory Synchronization Accounts role. After setup this role account is the only required one;
  see the accounts and permissions page for what can be removed.

## Choose the auth model consciously
- **PHS** (password hash sync): resilient; hashes of hashes in cloud.
- **PTA** (pass-through auth): agents on-prem validate passwords; agent servers are Tier 0.
- **Federation (AD FS)**: additional on-prem attack surface (Golden SAML); consider migrating to PHS/PTA with staged rollout.

## Protect cloud-only admins
- Cloud admin accounts must be cloud-only (not synced), so AD compromise does not yield Global Admin.
- Block **hard match / soft match takeover** of cloud accounts: disable soft match and hard-match
  takeover features (`Update-MgDirectoryOnPremiseSynchronization` features `BlockSoftMatchEnabled`,
  `BlockCloudObjectTakeoverThroughHardMatchEnabled`).
- Seamless SSO: roll over the Kerberos decryption key of the `AZUREADSSO` computer account regularly (see the Seamless SSO FAQ).

## Monitor
- Sign-ins of the sync account from anywhere except the Connect server IP.
- Audit: changes to sync features, new federated domains, `Set domain authentication` (federation
  backdoor), connector configuration changes.

## Gotchas
- Old Connect versions retire; unsupported versions stop syncing and miss security fixes.
- Filtering changes can delete many cloud objects; keep the export deletion threshold (accidental-delete prevention) enabled.

## Verify
Admin roles held only by cloud-only accounts, hard/soft match takeover blocked, sync account sign-ins
only from the server, and the server appears in Tier 0 asset lists and PAW-only access policies.

## Checked

2026-10-28. Confirmed against the Entra Connect accounts and permissions page and the sync service features page: MSOL_ prefixed AD connector account, Replicate Directory Changes All for password hash sync, Directory Synchronization Accounts role as the only required account after setup, soft match disable, BlockSoftMatchEnabled and BlockCloudObjectTakeoverThroughHardMatchEnabled features and Update-MgDirectoryOnPremiseSynchronization. Removed: Sync_ account name, certificate-based sync app claim, default 500 deletion threshold, Connect Health bullet, ADSync service account bullet, 30-day AZUREADSSOACC rotation (the FAQ names AZUREADSSO and says to roll the key over regularly).

Method: documentation only; no commands were run.
