---
id: computing-software.data-engineering.snowflake.sso-and-scim-provisioning
name: sso-and-scim-provisioning
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, scim-provisioning, sso, saml2, identity-provider]
level: advanced
status: docs-checked
description: "Set up Snowflake SSO (SAML2) and SCIM user/role provisioning from Okta or Entra ID: security integrations, provisioner roles, tokens, and common sync issues."
sources:
  - https://docs.snowflake.com/en/user-guide/scim-intro
  - https://docs.snowflake.com/en/user-guide/scim-okta
  - https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-security-integration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSO and SCIM provisioning

**Goal:** users log in via the corporate IdP and their Snowflake users and roles are created, updated and deactivated automatically.

## SSO (SAML2)
A SAML2 security integration replaces the deprecated SAML_IDENTITY_PROVIDER account parameter. The preferred way to give Snowflake the IdP details is METADATA_URL, which lets Snowflake fetch the IdP settings including its certificate; `ALTER SECURITY INTEGRATION ... REFRESH METADATA_URL` then simplifies certificate rotation.
```sql
CREATE SECURITY INTEGRATION my_idp
  TYPE = saml2
  ENABLED = true
  METADATA_URL = '<idp metadata url>'
  SAML2_SNOWFLAKE_ISSUER_URL = 'https://<orgname>-<account_name>.snowflakecomputing.com'
  SAML2_SNOWFLAKE_ACS_URL = 'https://<orgname>-<account_name>.snowflakecomputing.com/fed/login';
```
- The issuer and ACS URL formats must match the Snowflake account URL you gave the IdP; if omitted they default to the account's legacy URL.
- IdP-initiated SSO needs no Snowflake configuration. For Snowflake-initiated SSO set `SAML2_ENABLE_SP_INITIATED = true` and `SAML2_SP_INITIATED_LOGIN_PAGE_LABEL` (the label shown on the login page).
- Optional hardening: `SAML2_SIGN_REQUEST = true` (signed requests; the IdP verifies with the cert in `SAML2_SNOWFLAKE_X509_CERT`, readable via `DESC SECURITY INTEGRATION`), encrypted assertions, and `SAML2_REQUESTED_NAMEID_FORMAT`. If NameID format is not set, Snowflake requests the emailAddress format.

## SCIM (Okta example)
Snowflake supports SCIM 2.0 with Okta, Microsoft Entra ID and custom IdPs. The SCIM role must own any users or roles imported from the IdP, otherwise IdP updates are not synced. Roles: OKTA_PROVISIONER (Okta), AAD_PROVISIONER (Entra ID), GENERIC_SCIM_PROVISIONER (custom).
```sql
use role accountadmin;
create role if not exists okta_provisioner;
grant create user on account to role okta_provisioner;
grant create role on account to role okta_provisioner;
grant role okta_provisioner to role accountadmin;
create or replace security integration okta_provisioning
  type = scim
  scim_client = 'okta'
  run_as_role = 'OKTA_PROVISIONER';
```
Then generate the SCIM access token (see "Authenticating SCIM API requests" in the docs) and enter it as the API token in the Okta Snowflake app's integration settings. A less-privileged run-as role than ACCOUNTADMIN can cause unexpected errors; alternatives are a role with global MANAGE GRANTS, or a custom role with OWNERSHIP on every role SCIM will manage.

## What gets synced (Okta)
- Users: push new users, profile updates, deactivation (sets DISABLED = TRUE), reactivation, optional password sync.
- Groups to roles: Push Groups creates roles with the same names; create the group in Okta first. Okta cannot manage manually created Snowflake roles, and Push Groups does not create users.
- You still grant privileges to those roles inside Snowflake.

## Gotchas
- SCIM does not enable SSO; set that up separately (Snowflake-initiated SSO).
- Okta's default is to create a random password per user; unchecking it avoids a non-SSO login path (and set SYNC_PASSWORD to false on the integration).
- Existing roles cannot be brought under Okta management by ownership transfer; existing users can: `grant ownership on user <name> to role okta_provisioner;` (ensure login_name is set; the user's name is changed to the Okta username).
- If a user update fails, check that the user is owned by the run_as_role.
- Account names with underscores need hyphens in the Okta SubDomain; do not use private connectivity (privatelink) URLs there.
- Allow Okta IPs in the network policy; a network policy set on the SCIM integration overrides the account-level one for it.
- Limit: 500 concurrent requests per account per SCIM endpoint, then HTTP 429 (mostly during initial provisioning of more than 10 thousand objects).
- Users created via SCIM get invitation emails by default.

## Verify
Assign a test user in Okta and confirm it appears in Snowflake; deactivate it and confirm DISABLED. Audit incoming requests with `SELECT * FROM TABLE(REST_EVENT_HISTORY('scim'))` in snowflake.information_schema as ACCOUNTADMIN.

## Checked
Method: docs-only read on 2026-11-09 of scim-intro and scim-okta (read in full as text) and the first 150 lines of the SAML2 federated authentication page (partial read: the encryption, signing and NameID sections were covered; later sections not read). Dropped unstated claims: the token function name, a 6-month token expiry, Entra ID SCIM_CLIENT value, "do not grant ACCOUNTADMIN roles via groups", service-user advice, and the exact SAML2_ISSUER/SSO_URL/PROVIDER form of the SSO statement.
