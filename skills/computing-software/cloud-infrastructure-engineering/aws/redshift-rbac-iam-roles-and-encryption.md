---
id: computing-software.cloud-infrastructure-engineering.aws.redshift-rbac-iam-roles-and-encryption
name: redshift-rbac-iam-roles-and-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, redshift, redshift-rbac, redshift-iam-role, row-level-security, dynamic-data-masking, encryption]
level: advanced
status: docs-checked
description: "Secure Amazon Redshift: role-based access control in SQL, IAM roles for COPY/UNLOAD/Spectrum, IAM and Identity Center sign-in, row-level security, masking, and encryption."
sources: ["https://docs.aws.amazon.com/redshift/latest/dg/t_Roles.html", "https://docs.aws.amazon.com/redshift/latest/dg/r_roles-default.html", "https://docs.aws.amazon.com/redshift/latest/dg/r_GRANT.html", "https://docs.aws.amazon.com/redshift/latest/dg/t_rls.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/authorizing-redshift-service.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/authorizing-redshift-service-database-users.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-db-encryption.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/changing-cluster-encryption.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-parameter-groups.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redshift RBAC, IAM roles and encryption

## 1. Database RBAC
```sql
CREATE ROLE analyst;
CREATE ROLE etl_writer;
GRANT USAGE ON SCHEMA sales TO ROLE analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA sales TO ROLE analyst;
ALTER DEFAULT PRIVILEGES IN SCHEMA sales GRANT SELECT ON TABLES TO ROLE analyst;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA sales TO ROLE etl_writer;
GRANT ROLE sys:monitor TO ROLE ops;               -- system-defined role
```
- Roles can be nested (you can grant roles to users and to roles). System-defined roles start with `sys:`:
  `sys:monitor` (catalog and system tables), `sys:operator` (adds analyze, vacuum, cancel queries), `sys:dba`
  (schema and table DDL, inherits `sys:operator`), `sys:secadmin` (users, roles, RLS and masking policy management)
  and `sys:superuser`. Roles with the `ds:` prefix are internal to data sharing.
- `ALTER DEFAULT PRIVILEGES` so new tables are covered; forgetting it is the usual "analyst cannot see the new table".
- Audit with `SVV_ROLES`, `SVV_ROLE_GRANTS` and `SVV_RELATION_PRIVILEGES`.
- Column-level `GRANT SELECT (col1, col2) ON table TO ROLE ...` is supported.

## 2. Authentication options
- Database users with passwords (avoid for humans).
- **IAM**: temporary database credentials from `GetClusterCredentials` or `GetClusterCredentialsWithIAM` (provisioned) and
  `GetCredentials` (Serverless); JDBC/ODBC drivers support IAM authentication.
- **IAM Identity Center** and native IdP federation are supported connection paths; follow the Redshift Management
  Guide pages for the user and role name mapping, which differ by method.

## 3. IAM roles Redshift assumes
For `COPY`, `UNLOAD`, Spectrum, ML and external functions, Redshift uses IAM roles associated with the cluster or namespace:
```bash
aws redshift modify-cluster-iam-roles --cluster-identifier dw --add-iam-roles arn:aws:iam::<ACCOUNT_ID>:role/RedshiftS3Read
aws redshift modify-cluster-iam-roles --cluster-identifier dw --default-iam-role-arn arn:aws:iam::<ACCOUNT_ID>:role/RedshiftS3Read
```
```sql
COPY sales.orders FROM 's3://lake/orders/2026/10/' IAM_ROLE default FORMAT AS PARQUET;
```
- The trust policy principal is `redshift.amazonaws.com`.
- By default every database user on the cluster can use every IAM role associated with it. Two documented controls:
  `GRANT ASSUMEROLE ON { 'iam_role' | default | ALL } TO { user | ROLE role | GROUP group | PUBLIC } FOR { ALL | COPY |
  UNLOAD | EXTERNAL FUNCTION | CREATE MODEL }`, or an `sts:ExternalId` condition in the role trust policy listing
  database user ARNs (`arn:aws:redshift:<REGION>:<ACCOUNT_ID>:dbuser:<CLUSTER>/<USER>`).
- Role chaining puts several role ARNs in one quoted, comma-separated `IAM_ROLE '<arn1>,<arn2>'` string, which is how
  a cluster reaches resources in another account.

## 4. Fine-grained controls
- **Row-level security**: `CREATE RLS POLICY name WITH (col type) USING (predicate)`, `ATTACH RLS POLICY name ON table
  TO { user | ROLE role | PUBLIC }`, then `ALTER TABLE ... ROW LEVEL SECURITY ON`. Superusers and `sys:secadmin` can
  create policies and turn RLS on. Policies cannot reference catalog tables, cross-database relations, external
  tables, regular or late-binding views, temporary tables or tables that already have RLS.
- **Dynamic data masking**: `CREATE MASKING POLICY name WITH (input_columns) USING (masking_expression)`, attached to
  columns for roles.
- Lake Formation permissions apply to Spectrum tables it manages.

## 5. Encryption
- At rest: new clusters are encrypted by default with an AWS-owned key unless you choose a customer managed KMS key.
  `aws redshift modify-cluster --cluster-identifier <id> --encrypted --kms-key-id <key>` moves an unencrypted cluster
  to KMS (or a customer managed key); Redshift migrates data to a new encrypted cluster and the cluster is read-only
  and shows `resizing` meanwhile. Disable cross-Region snapshot copy first. HSM encryption cannot be set by modifying
  a cluster.
- In transit: SSL for JDBC/ODBC connections; the `require_ssl` parameter-group value defaults to true as of
  10 January 2025.
- Cross-Region snapshot copy of a KMS-encrypted cluster: configure a snapshot copy grant for a key in the
  destination Region; without one, destination snapshots use a default AWS-owned key.

## Verify
- [ ] No human uses a superuser; roles cover schemas with default privileges.
- [ ] `GRANT ASSUMEROLE` or an `ExternalId` condition restricts COPY/UNLOAD roles to intended identities.
- [ ] `require_ssl` is true; encryption uses the intended KMS key (`describe-clusters --query 'Clusters[].{enc:Encrypted,key:KmsKeyId}'`).

## Checked
Date: 2026-10-27. Documentation release: Amazon Redshift Database Developer Guide and Management Guide (latest),
botocore redshift and redshift-serverless models. Confirmed: system-defined role names and permissions, role
nesting, `GRANT ASSUMEROLE` syntax and `FOR` list, default availability of IAM roles and the `ExternalId` trust
condition, `modify-cluster-iam-roles` parameters, RLS and masking syntax and limits, `sys:secadmin` rights, encryption
default and migration behaviour, `require_ssl` default, and the snapshot copy grant behaviour. Removed the `IAMR:` and
`IAMIDC:` user-name prefixes and the Serverless TLS-default claim (not found in the docs read), the `serverless`
trust principal, and the statement that a snapshot copy grant is required (the page says destination snapshots
fall back to an AWS-owned key).
Method: documentation only; no commands were run.
