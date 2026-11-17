---
id: computing-software.messaging-and-integration.apache-zookeeper.pluggable-authentication
name: pluggable-authentication
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, pluggable-authentication, authenticationprovider, serverauthenticationprovider, authprovider]
level: sme
status: docs-checked
description: "Write a custom ZooKeeper auth scheme: AuthenticationProvider methods, ServerAuthenticationProvider since 3.6.0, and registering with authProvider.N on every server."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pluggable authentication

- Implement `AuthenticationProvider`: `getScheme`, `handleAuthentication`, `isValid`, `matches`, `isAuthenticated`.
- `isValid(id)` is called when an ACL is set (e.g. `ip:172.16.0.0/16` valid, `ip:host.com` not); `isAuthenticated` decides whether the scheme's info is added for `auth` ACL entries; `matches(id, aclExpr)` is called when checking an ACL.
- Since 3.6.0, extend `ServerAuthenticationProvider` so `handleAuthentication` and `matches` receive extra context (ZooKeeperServer, ServerCnxn, path, perm, setAcls).
- Register with `-Dzookeeper.authProvider.X=<class>` or `authProvider.N=<class>` in the server config.
- Suffixes must be unique (duplicates: only one is used); all servers need the same plugins or clients may fail to connect to some.

Verify: after `addauth <scheme> ...`, `whoami` shows the scheme and ACLs using it take effect.

## Checked

Method: docs-checked 2026-11-09 against the ZooKeeper Programmer's Guide (Pluggable ZooKeeper authentication section); the audit-logging getUserName claim was dropped as not found in the pages read.
