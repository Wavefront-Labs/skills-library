---
id: computing-software.cloud-infrastructure-engineering.azure.stored-access-policies-and-sas-revocation
name: stored-access-policies-and-sas-revocation
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, storage-security, stored-access-policies, sas-revocation, service-sas, sas, shared-access-signature]
level: practitioner
status: docs-checked
description: "Use stored access policies so service SAS tokens can be revoked or extended, and know how to revoke every other kind of SAS (account, user delegation) in an incident."
sources: ["https://learn.microsoft.com/rest/api/storageservices/define-stored-access-policy", "https://learn.microsoft.com/azure/storage/common/storage-sas-overview", "https://learn.microsoft.com/azure/storage/blobs/storage-blob-user-delegation-sas-create-cli#revoke-a-user-delegation-sas"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stored access policies and SAS revocation

**Goal:** every SAS you hand out can be killed in minutes without rotating account keys for
everyone.

## How each SAS type is revoked
| SAS type | Signed with | Revoke by |
|---|---|---|
| Service SAS **with stored access policy** | Account key | Delete/modify the policy |
| Service SAS ad hoc | Account key | Rotate the key that signed it |
| Account SAS | Account key | Rotate the key |
| User delegation SAS | Entra user delegation key | `revoke-delegation-keys` (all UD SAS on account) or remove the signer's RBAC |
Stored access policies give per-container granularity — the reason to use them when you must use key-signed SAS.

## Create a policy and a SAS bound to it
```bash
az storage container policy create --account-name stdata -c exports -n partner-acme \
  --permissions rl --start 2026-10-16T00:00Z --expiry 2026-11-16T00:00Z --auth-mode key
az storage container generate-sas --account-name stdata -n exports --policy-name partner-acme -o tsv
```
The SAS contains `si=partner-acme` and no `sp/se` (they come from the policy).

## Revoke / extend
```bash
az storage container policy delete --account-name stdata -c exports -n partner-acme   # revoke now
az storage container policy update --account-name stdata -c exports -n partner-acme --expiry 2026-12-31T00:00Z   # extend
```
A create or change can take up to 30 seconds to take effect.

## Incident playbook: leaked SAS of unknown type
1. Decode the token's query string: `si` → stored policy; `skoid/sktid` → user delegation; `srt/ss` → account SAS.
2. Apply the revocation from the table.
3. If key rotation is needed, move apps to the other key before regenerating the one that signed the SAS.

## Better defaults
- Prefer **user delegation SAS** (Entra-signed, user delegation key valid at most 7 days).
- Set a **SAS expiration policy** on the account: it gives a recommended upper limit on SAS validity for service and account SAS.

## Gotchas
- Stored access policies apply to service SAS only; an account SAS is not bound to one.
- Clock skew: set `start` 15 minutes in the past or omit it.

## Verify
- [ ] `az storage container policy list --account-name stdata -c exports` shows expected policies.
- [ ] After deletion, `curl "<blob-url>?<sas>"` is rejected.

## Checked

Date: 2026-10-28.

Confirmed against Learn (define-stored-access-policy, storage-sas-overview, user delegation SAS revocation): stored policies revoke a service SAS without regenerating keys, up to 30 seconds to take effect, `revoke-delegation-keys` revokes all user delegation SAS, 7-day user delegation key limit, SAS expiration policy, 15-minute start-time guidance. CLI commands via check_commands.py.
Removed: the 5-policy cap, rename invalidation, key rotation order, the StorageBlobLogs query, allowSharedKeyAccess line, container recreate note and the 403 error name (not on fetched pages).

Method: documentation only; no commands were run.
