---
id: computing-software.systems-network-administration.apache-tomcat.realm-userdatabase-and-memory
name: realm-userdatabase-and-memory
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, realm, userdatabaserealm, memoryrealm, tomcat-users, tomcat-users-xml, allrolesmode, transportguaranteeredirectstatus]
level: practitioner
status: docs-checked
description: "Configure the Tomcat 10.1 UserDatabaseRealm and MemoryRealm backed by tomcat-users.xml, plus the common Realm attributes allRolesMode and transportGuaranteeRedirectStatus."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/realm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# UserDatabaseRealm and MemoryRealm

Common Realm attributes: `className` (required), `allRolesMode` (default `strict`; also `authOnly`, `strictAuthOnly`; controls the `*` role), `transportGuaranteeRedirectStatus` (302), `X509UsernameRetrieverClassName` (default: certificate SubjectDN), `stripRealmForGss` (true). A Realm nests at most one CredentialHandler; by default a MessageDigestCredentialHandler is used (see `computing-software.systems-network-administration.apache-tomcat.credential-handler-password-digest`).

UserDatabaseRealm (reads a global `UserDatabase` JNDI resource):
```xml
<Realm className="org.apache.catalina.realm.UserDatabaseRealm"
       resourceName="UserDatabase"/>
```
- `resourceName` required.
- `localJndiResource` (false): use a UserDatabase defined in the Context.
- `useStaticPrincipal` (false): detached principal; set true if serialisation is used.

MemoryRealm (solely to get started, not for production; nothing updates the in-memory users when the file changes):
- `pathname`: URL, absolute path or path relative to `$CATALINA_BASE`; default `conf/tomcat-users.xml`. Root element `<tomcat-users>`, one `<user>` per user with `username` (or `name`), `password` (clear text) and comma-delimited `roles`.
```xml
<tomcat-users>
  <user username="alice" password="<PASSWORD>" roles="manager-gui"/>
</tomcat-users>
```

A container (Engine, Host or Context) holds at most one Realm; one set on an Engine or Host is inherited by lower containers unless they define their own. The page points to Single Sign On for virtual-host SSO.

Verify: log in to a protected URL with the user.

## Checked

2026-11-04. Read the Tomcat 10.1 Realm page (config/realm.html): confirmed allRolesMode values, transportGuaranteeRedirectStatus 302, X509UsernameRetrieverClassName default, stripRealmForGss, UserDatabaseRealm resourceName, localJndiResource and useStaticPrincipal, MemoryRealm pathname default and file format, the not-for-production warning, one Realm per container with inheritance, and at most one nested CredentialHandler. Removed the tomcat-users.xml claim for UserDatabaseRealm, the hashed-password hint for MemoryRealm (page says clear text), the SSO requirement and the restart advice.

Method: documentation only; no commands were run.
