---
id: computing-software.devops-ci-cd.spinnaker.ldap-authentication
name: ldap-authentication
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [ldap, authentication, active-directory, bind, user-dn-pattern, gate, ldaps]
level: advanced
status: docs-checked
description: "Configure LDAP bind authentication in Gate, work out the user DN from the URL root, userDnPattern or search filter, with gate-local.yml settings and ldapsearch tests."
sources:
  - https://spinnaker.io/docs/setup/other_config/security/authentication/ldap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Gate uses the standard **bind** approach: it logs in to the LDAP server with the username and password the user typed, and a successful connection means authenticated.

**Notes from the page:**
- This is mostly Spring LDAP configuration, so Spring documentation helps with configuration values.
- If the manager DN is not set, searches run as the logging-in user and you will see bind failures with LDAP error codes in logs.
- Spaces are escaped by the library.
- Use `ldaps://`; otherwise passwords cross the wire in clear text. Common ports: 636 LDAPS, 389 LDAP, 3268 and 3269 for AD Global Directory (non-SSL and SSL). With no port, `ldap://` implies 389 and `ldaps://` implies 636.

**Finding the user DN.** The root DN comes from the URL path (`ldaps://my.server/a/b/c` gives `a/b/c`). If `userSearchFilter` is set, Gate searches (in `userSearchBase`, or the root DN if unset) with a sub-tree search for that filter. Otherwise it builds the DN from `userDnPattern`: with root `dc=my-organization,dc=com` and pattern `uid={0},ou=users`, user `jdoe` gets `uid=jdoe,ou=users,dc=my-organization,dc=com`. Debug logging of `LdapUserRolesProvider` prints the extracted Root DN.

**Configuration** in `gate-local.yml`:

```yaml
ldap:
  enabled: true
  url: ldaps://host/a/b/c
  managerDn: <manager DN>
  managerPassword: <password or encrypted: secret reference>
  groupSearchBase: groupInfo
  userDnPattern: <optional>
  userSearchBase: <optional>
  userSearchFilter: <optional>
```

**Active Directory.** The page recommends leaving `userDnPattern` unset: AD groups store user DNs in `memberOf`, and the DN contains the CN, which cannot be built without sub searches. Use `userSearchFilter` (for example `(&(objectClass=user)(sAMAccountName={0}))`), with `managerDn` so the manager user finds the user by subtree search; `userSearchBase` can be set separately instead of on the URL.

**Testing.** Reproduce a lookup with `ldapsearch -D "MANAGER_DN" -w 'MANAGER_PASSWORD' -H ldaps://host -x -b "<userSearchBase>" "(UID=USERNAME)"` when a filter and base are set. For "Bad Credentials" with a correct password, confirm the fully qualified user DN with your LDAP administrator.

## Checked

2026-11-04. Bind approach, notes, ports, DN derivation rules, the gate-local.yml block, AD guidance and ldapsearch tests were confirmed on the LDAP page. Removed: the Halyard 1.20 note and the `hal config security authn ldap` commands (not on the page).

Method: documentation only; no commands were run.
