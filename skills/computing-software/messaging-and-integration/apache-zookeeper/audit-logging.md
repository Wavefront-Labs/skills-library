---
id: computing-software.messaging-and-integration.apache-zookeeper.audit-logging
name: audit-logging
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, audit-log, audit-enable, logback, slf4jauditlogger, security]
level: advanced
status: docs-checked
description: "Enable ZooKeeper audit logging with audit.enable=true: logback appender RFAAUDIT, log fields, audited operations and how the user field is derived."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAuditLogs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audit logs (3.6.0+)

- Off by default; set `audit.enable=true` in `conf/zoo.cfg`. Entries are written only on the server the client is connected to.
- Uses logback: the audit section of `conf/logback.xml` ships commented out; uncomment it. Appender `RFAAUDIT`, file `zookeeper_audit.log` (property `zookeeper.auditlog.file`), threshold INFO (`zookeeper.auditlog.threshold`), rolling policy `maxIndex` 10, `MaxFileSize` 10MB, logger `org.apache.zookeeper.audit.Slf4jAuditLogger`. Edit these to change the file, backups, size or logger.
- Fields (key=value pairs): `session`, `user`, `ip`, `operation`, `znode`, `znode type` (creation only; the samples print `znode_type`), `acl` (setAcl only), `result` (success, failure, invoked; "invoked" is used for serverStop because it is logged before the stop is confirmed).
- `operation` values: serverStart, serverStop, create, delete, setData, setAcl, multiOperation, reconfig, ephemeralZNodeDeleteOnSessionClose (the sample log prints `ephemeralZNodeDeletionOnSessionCloseOrExpire`).
- `user` depends on the auth provider: IPAuthenticationProvider gives the authenticated IP, SASLAuthenticationProvider the client principal, X509AuthenticationProvider the client certificate, DigestAuthenticationProvider the authenticated user. A client with several schemes gets a comma-separated list. Custom providers can override `AuthenticationProvider.getUserName(String id)`; otherwise `Id.id` is used.
- Server-initiated (system) operations, such as deleting ephemeral nodes when a session closes, use the server's own principal, or the OS user that started the server if it has none.

Example from the page: `session=0x19344730000   user=192.168.1.2,zkcli@HADOOP.COM  ip=192.168.1.2    operation=create    znode=/a    znode_type=persistent  result=success`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the ZooKeeper Audit Logging page in full. Removed: the "Verify" claim that a zkCli create adds a matching line (inferred, not stated as a test) and the Administrator's Guide source, which was not needed.
