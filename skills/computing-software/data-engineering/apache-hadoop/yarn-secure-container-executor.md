---
id: computing-software.data-engineering.apache-hadoop.yarn-secure-container-executor
name: yarn-secure-container-executor
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, security, container-executor, kerberos, banned-users]
level: advanced
status: docs-checked
description: "Securing YARN: ResourceManager and NodeManager principals and keytabs, LinuxContainerExecutor binary permissions 6050, and container-executor.cfg banned.users and min.user.id."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SecureMode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure YARN

From the Hadoop in Secure Mode page. yarn-site.xml:
- `yarn.resourcemanager.principal` = `rm/_HOST@REALM.TLD`; `yarn.resourcemanager.keytab` = `/etc/security/keytab/rm.service.keytab`. The page's example RM keytab holds `rm/` and `host/` principals for the host.
- `yarn.resourcemanager.webapp.https.address` = `${yarn.resourcemanager.hostname}:8090` (non-HA; HA uses `...https.address.<rm-id>`)
- `yarn.nodemanager.principal` = `nm/_HOST@REALM.TLD`; `yarn.nodemanager.keytab` = `/etc/security/keytab/nm.service.keytab` (example keytab likewise holds `nm/` and `host/`)
- `yarn.nodemanager.container-executor.class` = `org.apache.hadoop.yarn.server.nodemanager.LinuxContainerExecutor`
- `yarn.nodemanager.linux-container-executor.group` = `hadoop`
- `yarn.nodemanager.linux-container-executor.path`: path to the `container-executor` executable
- `yarn.nodemanager.webapp.https.address` = `0.0.0.0:8044`
- `yarn.http.policy` = `HTTPS_ONLY` enables SSL for the YARN daemons' web consoles. Core RPC authentication needs `hadoop.security.authentication` = `kerberos` in core-site.xml.

Optional WebAppProxy: `yarn.web-proxy.address` (the RM runs the proxy if it equals the RM web address or is unset), `yarn.web-proxy.keytab`, `yarn.web-proxy.principal` (`wap/_HOST@REALM.TLD`).

LinuxContainerExecutor: runs containers as the submitting user under full security (all user accounts must exist on the nodes), or as a dedicated user (default nobody) otherwise; DefaultContainerExecutor runs them as the NodeManager's user. The setuid executable is built with `mvn package -Dcontainer-executor.conf.dir=<conf dir>` and installed in `$HADOOP_YARN_HOME/bin`.
- Binary: mode 6050 (`--Sr-s---`), owner root, group a special group such as `hadoop` that contains the NodeManager user and no ordinary application user (otherwise security is compromised).
- container-executor.cfg (key=value lines, in the conf dir passed to mvn): mode 0400. The page is inconsistent on owner: the prose says owned by the NodeManager user, the permissions tables say root:hadoop.
- Keys: `yarn.nodemanager.linux-container-executor.group` (same as yarn-site), `banned.users` (example `hdfs,yarn,mapred,bin`), `allowed.system.users` (example `foo,bar`), `min.user.id` (example `1000`, "prevent other super-users").
- `yarn.nodemanager.local-dirs` and `log-dirs` (and the paths leading to them) need 755; recommended owner yarn:hadoop.

## Checked

Method: 2026-11-08, read the YARN, ResourceManager, NodeManager, WebAppProxy, LinuxContainerExecutor and path-permission sections of the project's SecureMode markdown source (other sections of that large page were not read). Removed an unsupported "Verify" step and presented banned.users as the page's example rather than a stated default; flagged the page's own owner inconsistency for container-executor.cfg. Other values were unchanged.
