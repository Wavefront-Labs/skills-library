---
id: computing-software.data-engineering.apache-hadoop.hdfs-secure-datanode-sasl
name: hdfs-secure-datanode-sasl
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, security, datanode, sasl, jsvc]
level: sme
status: docs-checked
description: "Securing HDFS DataNodes: privileged ports with jsvc versus SASL via dfs.data.transfer.protection, required companion settings, and dfs.encrypt.data.transfer."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SecureMode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure DataNodes

The data transfer protocol does not use Hadoop RPC, so a DataNode must prove it was started securely. Common settings: `dfs.datanode.kerberos.principal` = `dn/_HOST@REALM.TLD`, `dfs.datanode.keytab.file` = `/etc/security/keytab/dn.service.keytab`, `dfs.datanode.https.address` = `0.0.0.0:9865`, `dfs.datanode.data.dir.perm` = `700`.

Option 1, privileged ports (jsvc): `dfs.datanode.address` = `0.0.0.0:1004` and `dfs.datanode.http.address` = `0.0.0.0:1006`. Running `hdfs datanode` as root binds the privileged ports, then drops privilege to the account in `HDFS_DATANODE_SECURE_USER` using jsvc from `JSVC_HOME`; both variables go in hadoop-env.sh. This assumes an attacker cannot get root on DataNode hosts.

Option 2, SASL (Hadoop 2.6.0 and later): no root start or privileged ports needed. Set `dfs.data.transfer.protection` (unset by default) to `authentication`, `integrity` or `privacy`. Then `dfs.datanode.address` must use a non-privileged port, `dfs.http.policy` must be `HTTPS_ONLY` (to guarantee authentication of HTTP servers) and `HDFS_DATANODE_SECURE_USER` must be undefined. The page also allows a variant with `dfs.http.policy` HTTPS_ONLY or a privileged `dfs.datanode.http.address`, keeping `HDFS_DATANODE_SECURE_USER` and `JSVC_HOME` set.

Migrating from root authentication to SASL: first deploy 2.6.0 or later on all nodes and external applications (only 2.6.0+ clients can connect to a SASL DataNode), then enable SASL in client configuration (a SASL client can talk to both kinds of DataNode), then migrate each DataNode by changing configuration and restarting. Temporarily mixing root-authenticated and SASL DataNodes is acceptable.

Block transfer encryption: `dfs.encrypt.data.transfer` (default false) set to true; optionally `dfs.encrypt.data.transfer.algorithm` (`3des` or `rc4`; default is the JCE default, usually 3DES) and `dfs.encrypt.data.transfer.cipher.suites` = `AES/CTR/NoPadding` (unspecified by default; `SM4/CTR/NoPadding` is also possible) with `...cipher.key.bitlength` 128, 192 or 256 (default 128). `hadoop.rpc.protection` = `privacy` encrypts RPC data.

## Checked

Method: 2026-11-08 compared against the Hadoop Secure Mode page (apache/hadoop trunk markdown). Settings match. The draft's advice to avoid mixing DataNode modes contradicted the page (mixing is acceptable during migration) and was replaced with the page's migration order; the invented "Verify" step was removed.
