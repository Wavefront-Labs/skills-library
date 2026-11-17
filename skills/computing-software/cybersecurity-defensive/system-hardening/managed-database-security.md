---
id: computing-software.cybersecurity-defensive.system-hardening.managed-database-security
name: managed-database-security
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [managed-database-security, amazon-rds, azure-sql, cloud-sql, iam-database-authentication, database-hardening]
level: practitioner
status: docs-checked
description: "Secure managed cloud databases (RDS/Aurora, Azure SQL, Cloud SQL): private networking, IAM or Entra auth, enforced TLS, encryption keys, secrets, audit logs and snapshot exposure."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.SSL.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html", "https://learn.microsoft.com/en-us/azure/azure-sql/database/security-overview", "https://learn.microsoft.com/en-us/azure/azure-sql/database/connectivity-settings", "https://docs.cloud.google.com/sql/docs/postgres/configure-ssl-instance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed cloud database security

The provider patches the OS and engine, but network exposure, identities, parameters, encryption keys, backups
and logs are still yours (shared responsibility).

## Network
- No public exposure: on Azure SQL Database set Public network access to Disable (the documented default) so only
  Private Endpoint (Private Link) connections work; with it disabled, firewall rules cannot be edited. Apply the same
  principle on RDS and Cloud SQL (private addressing, no wide-open authorised networks); look up the current setting
  names in each provider's networking page.
- Security groups / NSGs / firewall rules allow the engine port only from application subnets.
- Admin access through a bastion or the Cloud SQL Auth Proxy / connectors, not open IP ranges.

## Identity
- RDS IAM database authentication: each authentication token lives 15 minutes, so no database password is stored in
  the app; the token is only used to authenticate and does not affect an established session. Note that CloudWatch
  and CloudTrail do not log IAM database authentication itself.
- Azure SQL supports Microsoft Entra authentication (centrally managed identities, MFA and Conditional Access
  options) alongside SQL authentication.
- Cloud SQL: with `TRUSTED_CLIENT_CERTIFICATE_REQUIRED`, IAM database authentication clients must use the Cloud SQL
  Auth Proxy or Connectors.
- Master password: RDS can manage it in Secrets Manager (`--manage-master-user-password`), rotating it every seven
  days by default.
- App roles with least privilege inside the engine (same as self-hosted).

## TLS
- RDS for PostgreSQL: parameter `rds.force_ssl` defaults to 1 on version 15 and later and 0 on 14 and older. Set it
  to 1 in a custom parameter group (reboot needed if the instance already runs); non-SSL connections are then
  rejected.
- Azure SQL Database: the lowest supported minimum TLS version is 1.2; set it to 1.2 after compatibility testing.
- Cloud SQL `ssl_mode`: `ALLOW_UNENCRYPTED_AND_ENCRYPTED` (the default), `ENCRYPTED_ONLY`,
  `TRUSTED_CLIENT_CERTIFICATE_REQUIRED`. Enforcing SSL applies to new connections only; restart the instance to
  close existing unencrypted ones.
- Clients should verify the server certificate; "Allow only SSL connections" on Cloud SQL does not validate certificates.

## Encryption and keys
- RDS: you cannot create an encrypted snapshot of an unencrypted instance; to encrypt, copy a snapshot with
  encryption and restore from it (or use a blue/green deployment). You cannot un-encrypt an instance or restore an
  unencrypted snapshot into an encrypted one.
- Azure SQL: new databases are encrypted by default with TDE; customer-managed keys (Azure Key Vault) give control of
  rotation, revocation and auditing.
- Never share snapshots publicly. The AWS Config managed rule `rds-snapshots-public-prohibited` flags public RDS
  snapshots.

## Logging and threat detection
Azure SQL auditing records database events to a customer-owned storage account and can feed Azure Monitor logs and
Event Hubs; Microsoft Defender for SQL includes vulnerability assessment. For RDS and Cloud SQL pgAudit, see
`database-audit-logging`. Alert on login anomalies and public-exposure changes.

## Verify
A configuration scan (for example the Config rule above) shows no public snapshots; a non-TLS connection is refused;
the app connects with an IAM/Entra token; a restore from backup was tested this quarter.

## Checked
2026-10-31. Confirmed in AWS RDS pages (IAM token lifetime and logging note, `rds.force_ssl` defaults, encryption
limits, Secrets Manager 7-day default), the AWS Config rule page, Azure SQL pages (public network access default,
minimum TLS 1.2, Entra authentication, TDE default, CMK, auditing, Defender for SQL) and the Cloud SQL SSL page
(`ssl_mode` values and default). Removed as unconfirmed: `PubliclyAccessible`, "Microsoft Entra-only
authentication", MySQL `require_secure_transport`, `local_infile`, `xp_cmdshell`, deletion protection, AWS Backup
vault lock, GuardDuty RDS Protection, Security Command Center, SSM port forwarding and Cloud SQL private-IP
specifics.
Method: documentation only; no commands were run.
