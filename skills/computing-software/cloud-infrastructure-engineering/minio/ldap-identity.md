---
id: computing-software.cloud-infrastructure-engineering.minio.ldap-identity
name: ldap-identity
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, ldap-identity, active-directory, mc-idp-ldap-add, lookup-bind-dn, user-dn-search-filter, assume-role-with-ldap-identity, mc-idp-ldap-disable]
level: advanced
status: docs-checked
description: "Configure MinIO Active Directory or LDAP identity with mc idp ldap add: required lookup bind and search settings, env variable equivalents and enable or disable."
sources: ["https://github.com/minio/docs/blob/main/source/operations/external-iam/configure-ad-ldap-external-identity-management.rst", "https://github.com/minio/docs/blob/main/source/includes/baremetal/steps-configure-ad-ldap-external-identity-management.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO AD/LDAP identity management

MinIO needs a read-only account to **bind** and run user and group lookups. Each AD/LDAP user and group intended for MinIO needs a corresponding MinIO policy: a user with no policy and in groups with no policy has no permissions. The deployment needs bidirectional connectivity to the directory.

## mc idp ldap add
Minimum required settings: `server_addr`, `lookup_bind_dn`, `lookup_bind_password`, `user_dn_search_base_dn`, `user_dn_search_filter`.
```
mc idp ldap add ALIAS \
  server_addr="ldaps.example.net:636" \
  lookup_bind_dn="CN=xxxxx,OU=xxxxx,OU=xxxxx,DC=example,DC=net" \
  lookup_bind_password="xxxxxxxx" \
  user_dn_search_base_dn="DC=example,DC=net" \
  user_dn_search_filter="(&(objectCategory=user)(sAMAccountName=%s))" \
  group_search_filter="(&(objectClass=group)(member=%d))" \
  group_search_base_dn="ou=MinIO Users,dc=example,dc=net" \
  tls_skip_verify="off" server_insecure=off server_starttls="off"
```
`mc idp ldap` is recommended over `mc admin config set` because it adds features and validation; the `identity_ldap` key still works for old scripts.

## Environment variables
Same settings as `MINIO_IDENTITY_LDAP_SERVER_ADDR`, `..._LOOKUP_BIND_DN`, `..._LOOKUP_BIND_PASSWORD`, `..._USER_DN_SEARCH_BASE_DN`, `..._USER_DN_SEARCH_FILTER`, `..._GROUP_SEARCH_FILTER`, `..._GROUP_SEARCH_BASE_DN`, `..._TLS_SKIP_VERIFY`, `..._SERVER_INSECURE`, `..._SERVER_STARTTLS`, `..._SRV_RECORD_NAME`, `..._COMMENT`. Every node must use identical values or startup or config fails.

## Apply
Restart with `mc admin service restart ALIAS` (not needed when configured from the Console). Since RELEASE.2023-03-20T20-16-18Z, `mc idp ldap disable` and `mc idp ldap enable` toggle the connection. Users can log in to the Console with directory credentials, or applications can use the `AssumeRoleWithLDAPIdentity` STS API.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Configure AD/LDAP page and its steps include (configure-ad-ldap-external-identity-management.rst, steps-configure-ad-ldap-external-identity-management.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
