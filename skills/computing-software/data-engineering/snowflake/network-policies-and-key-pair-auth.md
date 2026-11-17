---
id: computing-software.data-engineering.snowflake.network-policies-and-key-pair-auth
name: network-policies-and-key-pair-auth
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, network-policy, network-rules, key-pair-authentication, service-users, mfa, authentication-policy, private-link, rsa-key-rotation, snowflake-security]
level: advanced
status: docs-checked
description: "Lock down Snowflake access: network rules and policies, key-pair auth for TYPE=SERVICE users with rotation, MFA and authentication policies, and PrivateLink."
sources:
  - https://docs.snowflake.com/en/user-guide/network-policies
  - https://docs.snowflake.com/en/user-guide/key-pair-auth
  - https://docs.snowflake.com/en/user-guide/authentication-policies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network policies and key-pair authentication

**Goal:** only expected networks can reach the account, humans use SSO+MFA, and services use keys (not passwords).

## Network rules and policies
```sql
create network rule admin.net.corp_vpn type = ipv4 mode = ingress value_list = ('203.0.113.0/24');
create network rule admin.net.etl_egress type = ipv4 mode = ingress value_list = ('198.51.100.10/32', '198.51.100.11/32');
create network policy corp_access allowed_network_rule_list = ('admin.net.corp_vpn', 'admin.net.etl_egress');
alter account set network_policy = corp_access;            -- account-wide
create network policy etl_only allowed_network_rule_list = ('admin.net.etl_egress');
alter user svc_airflow set network_policy = etl_only;       -- user-level policy
```
Test with a user-level policy on yourself before setting account-level, and keep a break-glass path (an admin user with its own policy) or you can lock everyone out. Private connectivity rules use `type = awsvpceid` or `azurelinkid` and take precedence over IPv4/IPv6 rules.

## Service users with key pairs
```bash
openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 aes-256-cbc -inform PEM -out rsa_key.p8   # encrypted private key, 2048-bit minimum
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```
```sql
create user svc_dbt_prod type = service default_role = transformer_prod default_warehouse = transforming_m;
alter user svc_dbt_prod set rsa_public_key = 'MIIBIjANBgkqh...';
-- rotation: set the second slot, deploy new private key to clients, then unset the old one
alter user svc_dbt_prod set rsa_public_key_2 = 'MIIBIjANBgkqh...new';
alter user svc_dbt_prod unset rsa_public_key;
desc user svc_dbt_prod;   -- RSA_PUBLIC_KEY_FP / _2_FP fingerprints
```
Users with `TYPE = SERVICE` must use key-pair authentication or OAuth. Snowflake is deprecating single-factor password logins: users who sign in with a password will need to enrol in MFA.

## Humans
- SSO via SAML, or Snowflake MFA enrolment.
- Authentication policies restrict methods/clients per account or user:
```sql
create authentication policy admin.auth.humans_sso authentication_methods = ('SAML') mfa_enrollment = 'REQUIRED';
alter account set authentication policy admin.auth.humans_sso;
```

## Audit
Review login history and alert on logins from outside allowed ranges or password logins by service users.

## Verify
- [ ] Login from a non-allowed IP is rejected (test from a different network).
- [ ] No service user authenticates with a password.
- [ ] Key rotation runbook tested.

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: ALTER USER SET NETWORK_POLICY, awsvpceid/azurelinkid rule types and precedence, RSA_PUBLIC_KEY_2 rotation, 2048-bit minimum and AES-256-CBC key generation, TYPE = SERVICE must use key pair or OAuth, password-login deprecation, MFA_ENROLLMENT and AUTHENTICATION_METHODS (network-policies, key-pair-auth, authentication-policies pages).

Removed or corrected: user-level precedence wording, Business Critical claim, Okta/Entra/Duo/passkey names, the account_usage login_history path and the has_password check (not on the pages read); corrected the openssl cipher flag to aes-256-cbc and quoted MFA_ENROLLMENT.

Method: documentation only; no commands were run.
