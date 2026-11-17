---
id: computing-software.data-engineering.snowflake.service-users-and-programmatic-access-tokens
name: service-users-and-programmatic-access-tokens
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, programmatic-access-token, service-users, type-service, key-pair-authentication, password-deprecation, authentication-policy, workload-identity]
level: practitioner
status: docs-checked
description: "Authenticate pipelines to Snowflake without passwords: TYPE=SERVICE users, key-pair auth, programmatic access tokens, workload identity federation, and authentication policies."
sources:
  - https://docs.snowflake.com/en/user-guide/admin-user-management#types-of-users
  - https://docs.snowflake.com/en/user-guide/programmatic-access-tokens
  - https://docs.snowflake.com/en/user-guide/key-pair-auth
  - https://docs.snowflake.com/en/user-guide/authentication-policies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service users and programmatic access tokens

**Goal:** dbt, Airflow, Fivetran and apps log in with machine credentials that are rotatable.

## User types
```sql
create user SVC_DBT type = SERVICE
  default_role = DBT_TRANSFORMER default_warehouse = TRANSFORM_WH
  comment = 'dbt prod';
alter user SVC_LEGACY_APP set type = LEGACY_SERVICE;   -- transitional type
```
- `PERSON`: humans.
- `SERVICE`: programmatic clients.
- `LEGACY_SERVICE`: transitional type for apps that cannot change yet.
See the user types page for how authentication differs between them.

## Key-pair (most universal)
```bash
openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 aes256 -inform PEM -out rsa_key.p8
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```
```sql
alter user SVC_DBT set rsa_public_key = 'MIIBIjANBgkqh...';
-- rotation: set RSA_PUBLIC_KEY_2, switch clients, then unset the old one
alter user SVC_DBT set rsa_public_key_2 = 'MIIB...new';
alter user SVC_DBT unset rsa_public_key;
```

## Programmatic access tokens (PATs)
```sql
alter user SVC_BI add programmatic access token bi_token
  role_restriction = 'BI_READER'
  days_to_expiry = 90
  comment = 'Tableau extract refresh';
-- returns the token secret once
alter user SVC_BI rotate programmatic access token bi_token;
alter user SVC_BI remove programmatic access token bi_token;
```
Service users (TYPE = SERVICE or LEGACY_SERVICE) can only generate or use a token if they are subject to a **network policy**.

## Authentication policies
```sql
create authentication policy svc_policy
  authentication_methods = ('KEYPAIR', 'PROGRAMMATIC_ACCESS_TOKEN')
  client_types = ('DRIVERS', 'SNOWFLAKE_CLI');
alter user SVC_DBT set authentication policy svc_policy;
```

## Inventory and audit
```sql
select user_name, first_authentication_factor, count(*)
from snowflake.account_usage.login_history
where event_timestamp > dateadd(day, -30, current_timestamp()) group by 1,2;
```
Find services still using `PASSWORD` and migrate them first.

## Verify
- [ ] `login_history` shows no password logins for service users.
- [ ] Token expiry dates tracked with rotation reminders.

## Checked
2026-10-28. Confirmed against the Snowflake programmatic access token page (DAYS_TO_EXPIRY, ROTATE PROGRAMMATIC ACCESS TOKEN, token shown once, network policy required for TYPE = SERVICE or LEGACY_SERVICE users, PROGRAMMATIC_ACCESS_TOKEN authentication method), the key-pair page (RSA_PUBLIC_KEY and RSA_PUBLIC_KEY_2 rotation), the authentication policy page (SNOWFLAKE_CLI client type) and LOGIN_HISTORY (first_authentication_factor). Removed: MFA and deprecation statements, per-type authentication rules, the SHOW tokens command, workload identity section, the users-view inventory query and the RSA_KEYPAIR login value.
Method: documentation only; no commands were run.
