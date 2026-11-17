---
id: computing-software.data-engineering.snowflake.security-and-data-sharing
name: security-and-data-sharing
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, secure-data-sharing, snowflake-marketplace, secure-views, role-hierarchy, row-access-policy, masking-policy, reader-account, data-clean-room, cross-cloud-sharing, snowflake-security]
level: advanced
status: docs-checked
description: "Set up Snowflake's role hierarchy (ACCOUNTADMIN, SYSADMIN, functional and access roles) and use Secure Data Sharing, reader accounts and listings correctly."
sources:
  - https://docs.snowflake.com/en/user-guide/data-sharing-intro
  - https://docs.snowflake.com/en/user-guide/security-access-control-considerations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowflake security and Secure Data Sharing

**Goal:** share live data across accounts without copying it, and build a role hierarchy that does not collapse into "just grant SYSADMIN to make it work." (See computing-software.data-engineering.data-warehouse-architecture.access-control-and-governance for the cross-platform principles.)

## 1. Role hierarchy
- ACCOUNTADMIN is the most powerful role, but not a superuser: it only manages objects where it, or a role below it in the hierarchy, holds the privileges. Only it configures account-level parameters and sees billing and credit data.
- USERADMIN creates users and roles; SYSADMIN creates warehouses, databases and the objects in them.
- Do not create objects with ACCOUNTADMIN, and do not use it for automated scripts. Build a hierarchy of roles aligned to business functions and assign the top roles to SYSADMIN. All warehouse and database object operations can then use SYSADMIN or lower; only user and role creation or modification needs SECURITYADMIN or another role with enough privileges.
- Objects created by a custom role cannot be modified or dropped even by ACCOUNTADMIN unless that custom role is granted to it, preferably through a hierarchy under SYSADMIN.
- Recommended pattern: **access roles** (permissions on objects, such as read or read-write on a database) granted to **functional roles** (accountant, analyst) granted to SYSADMIN. There is no technical difference between the two kinds; the difference is how you use them.
- ACCOUNTADMIN precautions: require MFA, assign to at least two users, use email addresses of current employees, and never make it any user's default role.
- Consider managed access schemas, where only the schema owner or a role with MANAGE GRANTS can grant on objects, centralising privilege decisions.

## 2. Secure Data Sharing (zero copy)
A provider shares selected objects (databases, schemas, tables, secure views, secure UDFs) with other Snowflake accounts through a named **share**. No data is copied or moved; consumers query the provider's data in place through a read-only database created from the share.
- Per-consumer restriction: a raw shared table gives every consumer the same access, so wrap what differs per consumer in a secure view or secure UDF (check the secure view and sharing pages for the exact pattern).
- Consumers with `IMPORTED PRIVILEGES` see everything in the share; database roles let providers grant subsets, otherwise you need multiple shares.
- **Reader accounts** let a consumer without a Snowflake account use shared data. The reader account belongs to and is paid for by the provider, can only consume from that provider, and cannot do DML such as loading or inserts.
- **Listings** are used to share across regions, publish publicly on the Snowflake Marketplace, charge for access, add metadata, or see consumer usage metrics. A direct share can be converted to a listing.
- A clean room lets you share data while controlling which queries can be run on it; consider it for cross-organisation analysis where neither side can share raw data. Read the clean room documentation for how it is configured.

## Verify
- [ ] No pipeline or service account holds ACCOUNTADMIN; each has a purpose-built functional role under SYSADMIN.
- [ ] ACCOUNTADMIN users have MFA and none use it as their default role.
- [ ] Objects intended to differ per consumer are exposed through secure views or secure UDFs, not raw tables.
- [ ] Cross-region or paid sharing is done through a listing rather than a direct share.

## Checked
2026-11-09. Confirmed on "Considerations for access control" and "About Secure Data Sharing": role descriptions, hierarchy recommendations, ACCOUNTADMIN precautions, object ownership behaviour, managed access schemas, database roles versus IMPORTED PRIVILEGES, share contents, in-place query, reader accounts, listings uses, clean room mention. Removed (not on the fetched pages): the optimizer predicate push-down explanation of secure views and their performance cost, the row access/masking policy comparison, the CREATE SHARE/ALTER SHARE syntax, CURRENT_ACCOUNT() consumer-keyed views, and the cross-cloud replication claim.
Method: documentation only; no commands were run.
