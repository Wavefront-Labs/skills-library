---
id: computing-software.systems-network-administration.apache-tomcat.realm-jndi-ldap
name: realm-jndi-ldap
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, realm, jndirealm, ldap, active-directory, usersearch, userpattern, rolesearch, starttls, ldap-authentication]
level: advanced
status: docs-checked
description: "Authenticate Tomcat 10.1 users against LDAP with JNDIRealm: connectionURL, userPattern vs userSearch, role lookup, bind credentials, timeouts, StartTLS and AD referrals."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/realm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JNDIRealm (LDAP)

User lookup, pick one style:
- Direct: `userPattern="uid={0},ou=people,dc=example,dc=com"`.
- Search: `userSearch="(uid={0})"`, `userBase`, `userSubtree` (false).

Roles: `roleBase`, `roleName`, `roleSearch` (`{0}` user DN, `{1}` username, `{2}` `userRoleAttribute` value), `roleSubtree` (false), `roleNested` (false), or `userRoleName` for an attribute on the user entry.

Connection:

| Attribute | Default |
|---|---|
| `connectionURL` | URL passed to the JNDI driver |
| `alternateURL` | used if a socket connection cannot be made to `connectionURL` |
| `connectionName` / `connectionPassword` | anonymous |
| `authentication` | "none", "simple", "strong" or provider specific; provider default if unset |
| `userPassword` | unset: simple bind with the user's DN and presented password; set (name of the password attribute): binds with `connectionName`/`connectionPassword` and compares locally |
| `connectionTimeout`, `readTimeout` | 5000 ms |
| `connectionPoolSize` | 1 |
| `useStartTls` | false |
| `referrals` | "ignore", "follow" or "throw"; AD often returns referrals; if DNS is not part of AD, following may make the client resolve your domain in DNS |
| `adCompat` | false; true ignores AD PartialResultExceptions |
| `sizeLimit`, `timeLimit` | 0 (none) |

```xml
<Realm className="org.apache.catalina.realm.JNDIRealm"
       connectionURL="ldap://ldap.example.com:389" useStartTls="true"
       userSearch="(uid={0})" userBase="ou=people,dc=example,dc=com"
       roleBase="ou=groups,dc=example,dc=com"
       roleName="cn" roleSearch="(member={0})"/>
```

`connectionName`/`connectionPassword` are used for search operations; with neither set an anonymous connection is made, which is often sufficient unless you specify `userPassword`.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Realm reference (JNDI Directory Realm). Replaced the required/fallback/referral cells with the page's wording; removed the service-account tip and the generic verify line.

Method: documentation only; no commands were run.
