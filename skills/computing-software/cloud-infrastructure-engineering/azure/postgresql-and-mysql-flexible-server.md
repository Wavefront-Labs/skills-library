---
id: computing-software.cloud-infrastructure-engineering.azure.postgresql-and-mysql-flexible-server
name: postgresql-and-mysql-flexible-server
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, postgresql-flexible-server, mysql-flexible-server, flexible-server, azure-database-for-postgresql, azure-database-for-mysql, open-source-databases, zone-redundant-ha, same-zone-ha, read-replicas, pitr, geo-redundant-backup, private-access, vnet-integration, private-endpoint, entra-authentication, server-parameters, pgbouncer, connection-pooling, storage-autogrow, burstable, major-version-upgrade, maintenance-window, pg-extensions, citus, cosmos-db-for-postgresql, entra-authentication-postgres, entra-auth-mysql]
level: practitioner
status: docs-checked
description: "Run PostgreSQL/MySQL flexible server: compute and storage, zone-redundant HA vs read replicas, private access, Entra auth, PgBouncer, PITR and geo-backup, major upgrades."
sources: ["https://learn.microsoft.com/en-us/cli/azure/postgres/flexible-server", "https://learn.microsoft.com/en-us/cli/azure/postgres/flexible-server/replica", "https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server", "https://learn.microsoft.com/en-us/azure/postgresql/connectivity/concepts-pgbouncer", "https://learn.microsoft.com/en-us/azure/postgresql/security/security-entra-configure", "https://learn.microsoft.com/en-us/azure/postgresql/backup-restore/concepts-backup-restore", "https://learn.microsoft.com/en-us/azure/postgresql/read-replica/concepts-read-replicas"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# PostgreSQL and MySQL flexible server — managed open-source databases, sized and protected

**Goal:** a flexible server with the right compute/IOPS, HA that matches the tier,
private connectivity, Entra logins, pooled connections, and backups/upgrades handled
inside a maintenance window you chose.

## 1. Create
```bash
az postgres flexible-server create -g rg -n pg-orders-prod -l uksouth --version 16 --tier GeneralPurpose --sku-name Standard_D4ds_v5 \
  --storage-size 512 --storage-auto-grow Enabled --performance-tier P30 --zone 1 \
  --vnet vnet-data --subnet snet-pg --private-dns-zone <pg-private-zone-id> --public-access Disabled \
  --password-auth Disabled --backup-retention 35 --geo-redundant-backup Enabled   # HA mode and Entra admin: set in the portal/ARM per the HA and Entra articles (not flags of `create` in the current CLI reference)
az mysql flexible-server create ... --tier GeneralPurpose --sku-name Standard_D4ds_v4 --high-availability ZoneRedundant --storage-size 512 --storage-auto-grow Enabled --iops 3000
```
- Tiers (`--tier`): **Burstable**, **GeneralPurpose**, **MemoryOptimized**.
- Storage: the PostgreSQL CLI can create servers on **Premium SSD v2** disks, where IOPS and throughput are set independently (`--iops`, `--throughput`; only updatable on Premium SSD v2 servers).

## 2. Networking
- **Private access (VNet integration)**: the server sits in a delegated subnet (for MySQL the CLI delegates it to `Microsoft.DBforMySQL/flexibleServers`) and uses a private DNS zone linked to the virtual network.
- Firewall: `az postgres flexible-server firewall-rule create --start-ip-address ... --end-ip-address ...`. For `--public-access`, `0.0.0.0` allows access from any resource deployed within Azure; avoid it.

## 3. Identity and pooling
- Entra auth: set the Entra administrator on the server, then run `pgaadauth_create_principal` in the database to create a role for an identity; clients obtain a token (for example `az account get-access-token --resource-type oss-rdbms`) and use it as the password.
- Disable password auth (`--password-auth Disabled`) once apps are migrated.
- **PgBouncer** is built in: enable the `pgbouncer.enabled` server parameter and connect on port 6432. Transaction pooling breaks some session features; see `max_prepared_statements` on the PgBouncer page for prepared statements.

## 4. HA and replicas
| Need | Use |
|---|---|
| Survive zone loss, auto-failover | **Zone-redundant HA** (MySQL: `create --high-availability ZoneRedundant`) |
| Read scale-out / cross-region DR | **Read replicas** (`az postgres flexible-server replica create --name pg-orders-ukw --source-server pg-orders-prod -l ukwest`); PostgreSQL also has **virtual endpoints** (`az postgres flexible-server virtual-endpoint`) |
| Region loss with backups only | geo-redundant backup + `az postgres flexible-server geo-restore` |
- Failover drills: `az postgres flexible-server restart --failover ...`; clients must retry.
- Promote a replica with `az postgres flexible-server replica promote` (`--promote-mode standalone|switchover`, `--promote-option planned|forced`).

## 5. Backups, maintenance, upgrades
- Backup retention is 7 to 35 days for PostgreSQL (default 7; MySQL accepts 1 to 35). Point-in-time restore creates a new server: `az postgres flexible-server restore --source-server pg-orders-prod --restore-time "2026-10-14T03:00:00Z" --name pg-orders-restored`.
- **Maintenance window**: `--maintenance-window Day=Sat,StartHour=2,StartMinute=0` (custom schedule).
- Major version upgrade is an in-place command (`az postgres flexible-server upgrade`, `az mysql flexible-server upgrade`); test on a restored copy first.
- Server parameters: `az postgres flexible-server parameter set --name <parameter> --value <value>`.
- Stop for dev: `az postgres flexible-server stop`.

## Verify
- [ ] `az postgres flexible-server show` matches the design (SKU, HA, storage, network, auth, backup).
- [ ] A planned failover drill reconnects the app cleanly.
- [ ] App logs in with a managed identity token and password auth is disabled.
- [ ] A point-in-time restore to a new server succeeds.

## Checked
2026-10-31. Confirmed against the `az postgres flexible-server`, `az postgres flexible-server replica` and
`az mysql flexible-server` reference pages and the PostgreSQL PgBouncer, Entra configuration, backup and read-replica
pages: tier values, Premium SSD v2 IOPS/throughput, backup retention ranges, `0.0.0.0` meaning, promote options,
virtual endpoint and geo-restore commands, `pgaadauth_create_principal`, `oss-rdbms` token resource, `pgbouncer.enabled`
and port 6432. Removed as unconfirmed: specific version numbers, PgBouncer defaults, `require_secure_transport` and
TLS root guidance, private DNS zone names, replica lag metrics, the HA/same-zone comparison details, upgrade
prerequisites, extension allow-list guidance and most gotchas.
Method: documentation only; no commands were run.
