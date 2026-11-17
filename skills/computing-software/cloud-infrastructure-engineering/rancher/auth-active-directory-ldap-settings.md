---
id: computing-software.cloud-infrastructure-engineering.rancher.auth-active-directory-ldap-settings
name: auth-active-directory-ldap-settings
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [active-directory, ldap, ldaps, service-account, search-base, upn, samaccountname]
level: practitioner
status: docs-checked
description: "Configure Active Directory authentication in Rancher over LDAP: service account, ports, default login domain, search bases, and login attribute for UPN versus NetBIOS names."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/authentication-config/configure-active-directory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rancher talks to Active Directory over LDAP, so the flow matches the OpenLDAP integration. Create or obtain a dedicated AD **service account** that can search and read users and groups. A non-admin Domain User normally has enough read-only access; in locked-down domains it needs at least Read and List Content on the base OU or the whole domain. With TLS, have the CA certificate (plus intermediates) in PEM format ready to paste in.

Configure it as the initial local admin under **Users & Authentication > Auth Provider > ActiveDirectory**, then **Enable**.

Server settings: hostname, port (389 for plain LDAP, 636 for LDAPS), the TLS checkbox, a connection timeout, and service account username in NetBIOS (`DOMAIN\serviceaccount`) or UPN (`serviceaccount@domain.com`) form. **Default Login Domain** converts bare usernames like `jdoe` into `LOGIN_DOMAIN\jdoe`; if users log in with a UPN it **must be left empty**. **User Search Base** is the DN to search from (for example `ou=people,dc=acme,dc=com`) and every user must sit beneath it; Group Search Base is only needed when groups live elsewhere.

The schema section must match your directory. **Login Attribute** is `userPrincipalName` for UPN logins and usually `sAMAccountName` for old NetBIOS-style names. Search Attribute can list several attributes separated by a pipe. User Enabled Attribute normally stays at `userAccountControl`, which Rancher uses to detect disabled accounts.

Known TLS trap after upgrading to v2.6.0: AD certificates lacking SAN attributes fail with an x509 "legacy Common Name field" error. Replace the certificates, or set `GODEBUG=x509ignoreCN=0` on the Rancher server container.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Configure Active Directory (AD). Nothing removed.

Method: documentation only; no commands were run.
