---
id: computing-software.cloud-infrastructure-engineering.azure.key-vault-backup-restore-and-multi-region-strategy
name: key-vault-backup-restore-and-multi-region-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, key-vault, backup, restore, disaster-recovery, soft-delete, multi-region]
level: practitioner
status: docs-checked
description: "Key Vault resilience: built-in replication, soft delete and purge protection, per-object backup and restore limits, and a vault-per-region design."
sources: ["https://learn.microsoft.com/azure/key-vault/general/backup", "https://learn.microsoft.com/azure/key-vault/general/disaster-recovery-guidance", "https://learn.microsoft.com/azure/key-vault/managed-hsm/backup-restore", "https://learn.microsoft.com/cli/azure/keyvault"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key Vault backup, restore and multi-region strategy

**Goal:** losing a region, a vault or an object doesn't lose keys or block the app.

## What Azure already does
- Contents replicate within the region and, asynchronously, to the paired region when that pair is in the same
  geography. For a prolonged regional failure Microsoft may initiate failover; the vault is then **read-only**
  (supported: list/get certificates, secrets and keys, encrypt, decrypt) and you cannot change vault properties,
  access policy or firewall settings. It can be unavailable for a few minutes during failover.
- Regions without a pair, and Brazil South, Brazil Southeast and West US 3, have no Microsoft-managed cross-region
  failover; plan your own.
- Soft delete (default retention 90 days) and purge protection guard against deletion; Microsoft strongly recommends
  both for production.
- Microsoft says to back up secrets only with a business justification: built-in redundancy plus soft delete suffice
  for most cases. Valid reasons: moving objects between vaults or regions, an offline copy for compliance, regions
  without automatic replication, protecting specific objects against deletion.

## Object backup / restore
```bash
az keyvault secret backup --vault-name kv-a -n db-password --file db-password.bak
az keyvault key backup --vault-name kv-a -n cmk --file cmk.bak
az keyvault certificate backup --vault-name kv-a -n tls --file tls.bak
az keyvault secret restore --vault-name kv-b --file db-password.bak
```
Constraints:
- A backup is an encrypted blob restorable **only into a vault in the same subscription and Azure geography**.
- At most **500** past versions of an object can be backed up; more may error, and previous versions cannot be deleted.
  Backing up secrets with many versions can time out.
- No whole-vault backup in one operation: back up each key, secret and certificate individually (script it).
- A backup is a point-in-time snapshot; throttling during a backup makes it fail.
- A restored key is independent of the original: disabling or purging the original does not revoke any restored copy.
- Managed HSM supports full backup to a storage container, for example
  `az keyvault backup start --use-managed-identity true --hsm-name <hsm> --storage-account-name <acct> --blob-container-name <container>`.

## Multi-region design (what most apps should do)
- **One vault per region per app/env** (for example `kv-orders-prd-weu` and `kv-orders-prd-neu`), deployed by IaC.
- Secrets: written to both by the pipeline or by the generator (a rotation Function writes to both).
- Keys for CMK: same key material via backup/restore (same geography) or separate keys per region.
- App config points to the regional vault; failover is a region switch with no dependency on Microsoft's failover.

## Restore scenarios
| Scenario | Action |
|---|---|
| Secret deleted | `az keyvault secret recover` (soft delete) |
| Vault deleted | `az keyvault recover -n kv-a` (within retention) |
| Bad secret value | Re-enable a previous version (`az keyvault secret set-attributes --version <old> --enabled true`) or set a new version from the old value |
| Region down, need writes | Switch app to the secondary vault |

## Gotchas
- Cross-geography DR (for example EU to US) cannot use backup/restore; create keys independently.

## Verify
- [ ] Quarterly test: restore a sample secret from backup into a test vault in the same geography.
- [ ] `az keyvault show --query "properties.{softDelete:enableSoftDelete,purge:enablePurgeProtection,retention:softDeleteRetentionInDays}"` on all prod vaults.
- [ ] Secondary-region vault contains the same secret names (diff script in pipeline).

## Checked
2026-10-27. Confirmed against Learn "Azure Key Vault backup", "Key Vault availability and redundancy", Managed HSM
backup/restore and the az keyvault CLI reference (commands `backup start`, `recover`, `secret backup/restore/recover`
exist; flags used here are listed). Removed: soft-delete minimum of 7 days, "required for CMK", Premium-only restore of
HSM-key backups, "cannot restore over an existing name", "purge protection cannot be disabled/name reuse" and vault
name reservation (not in fetched pages), and the unverified `--storage-container-SAS-token` form. The `--query`
property names in the Verify command were not checked against a schema.
Method: documentation only; no commands were run.
