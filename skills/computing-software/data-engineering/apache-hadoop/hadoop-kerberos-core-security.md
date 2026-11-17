---
id: computing-software.data-engineering.apache-hadoop.hadoop-kerberos-core-security
name: hadoop-kerberos-core-security
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, security, kerberos, auth-to-local, rpc-protection, secure-mode]
level: advanced
status: docs-checked
description: "Hadoop secure mode core-site settings: hadoop.security.authentication, authorization, hadoop.rpc.protection levels, auth_to_local rules, NameNode principals and keytabs."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SecureMode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure mode: core and NameNode

core-site.xml, on all nodes:
- `hadoop.security.authentication`: `simple` (default, no authentication) or `kerberos`
- `hadoop.security.authorization`: `true` enables RPC service-level authorization
- `hadoop.rpc.protection`: `authentication` (default), `integrity` (adds an integrity check), `privacy` (adds data encryption)
- `hadoop.security.auth_to_local`: newline-separated `RULE:` expressions, ending with `DEFAULT`
- `hadoop.proxyuser.<superuser>.hosts` and `.groups`: hosts allowed to impersonate and groups of impersonated users (`*` wildcard)

auth_to_local: maps Kerberos principals to OS accounts; evaluation depends on `hadoop.security.auth_to_local.mechanism`. In the default `hadoop` mode a principal must match a rule that reduces it to a simple name without `@` or `/`, otherwise it is not authorized and an error is logged; `MIT` mode follows krb5.conf rules without that restriction (keep them in sync with /etc/krb5.conf). Rules apply to all principals regardless of realm, except `DEFAULT`, which takes the first component only when the realm is the default realm. With no rules set, Hadoop uses `DEFAULT`, which the page says is probably not suitable for most clusters. Hadoop does not check that the local account exists. Do not rely on auth_to_local as an ACL. Example rule: `RULE:[2:$1/$2@$0]([ndj]n/.*@REALM.\TLD)s/.*/hdfs/` maps nn, dn and jn principals to `hdfs`. Test rules with `hadoop kerbname`. Hadoop adds a `/L` flag to lowercase the result.

NameNode, hdfs-site.xml:
- `dfs.block.access.token.enable` = `true`
- `dfs.namenode.kerberos.principal` = `nn/_HOST@REALM.TLD`
- `dfs.namenode.keytab.file` = `/etc/security/keytab/nn.service.keytab`
- `dfs.namenode.kerberos.internal.spnego.principal` = `HTTP/_HOST@REALM.TLD`; the page says that for most deployments it can be `${dfs.web.authentication.kerberos.principal}`; `*` makes the web server try every principal in the keytab
- `dfs.web.authentication.kerberos.keytab` = `/etc/security/keytab/spnego.service.keytab` (in HA clusters shared with the JournalNodes)
- Optional SSL for the web UI: `dfs.http.policy` = `HTTP_ONLY`, `HTTPS_ONLY` or `HTTP_AND_HTTPS` (`HTTPS_ONLY` turns off http); `dfs.namenode.https-address` = `0.0.0.0:9871` (non-HA, no federation)

Users authenticate interactively with `kinit` or programmatically with keytab files.

## Checked

Method: 2026-11-08 compared against the Hadoop Secure Mode page (apache/hadoop trunk markdown, config tables and principal-mapping sections). Settings and defaults match; auth_to_local detail and the SPNEGO wildcard note added, and the invented "Verify" step removed. Some table values were reworded from the draft's `dfs.web.authentication.kerberos.principal` guidance, which the page lists under WebHDFS.
