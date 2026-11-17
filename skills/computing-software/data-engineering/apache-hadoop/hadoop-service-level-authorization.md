---
id: computing-software.data-engineering.apache-hadoop.hadoop-service-level-authorization
name: hadoop-service-level-authorization
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, security, authorization, hadoop-policy, acl, refreshserviceacl]
level: advanced
status: docs-checked
description: "Hadoop service-level authorization: hadoop-policy.xml ACL format, default and blocked ACLs, host-based control, and refreshing with refreshServiceAcl without restart."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/ServiceLevelAuth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service-level authorization

The initial authorization check: it runs well before other checks such as file permissions and job-queue ACLs. Off by default; set `hadoop.security.authorization` to true in `$HADOOP_CONF_DIR/core-site.xml`. Per-service ACLs live in `$HADOOP_CONF_DIR/hadoop-policy.xml`, for example:
- `security.client.protocol.acl`: ClientProtocol, used by user code via DistributedFileSystem
- `security.datanode.protocol.acl`: DataNodes talking to the NameNode
- `security.job.client.protocol.acl`: job clients talking to the ResourceManager
- `security.ha.service.protocol.acl`: HAAdmin managing active/standby NameNode states
- `security.refresh.policy.protocol.acl`: used by dfsadmin and rmadmin to refresh the policy

ACL format: comma-separated users, a space, comma-separated groups, e.g. `user1,user2 group1,group2`. A leading blank means groups only; users followed by a space or nothing means users only; `*` means everyone.

Defaults: a service with no ACL uses `security.service.authorization.default.acl`; if that is undefined, `*`.

Blocked lists: suffix the property with `.blocked` (e.g. `security.client.protocol.acl.blocked`). A user is authorised if in the ACL and not in the blocked list. Fallback is `security.service.authorization.default.acl.blocked`, else an empty blocked list.

Host control: the matching `.hosts` property (e.g. `security.client.protocol.hosts`) takes IP addresses, host names and IP ranges. `.hosts.blocked` blocks; fallbacks are `security.service.authorization.default.hosts` (else `*`) and `security.service.authorization.default.hosts.blocked` (else empty).

Refresh without restarting the NameNode or ResourceManager, after editing hadoop-policy.xml on the master nodes:

```
bin/hdfs dfsadmin -refreshServiceAcl
bin/yarn rmadmin -refreshServiceAcl
```

Use `security.refresh.policy.protocol.acl` to restrict who may refresh.

Page examples: `alice,bob mapreduce` for `security.job.client.protocol.acl`; `datanodes` for `security.datanode.protocol.acl`.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (ServiceLevelAuth.md in the apache/hadoop repo). Removed an unsupported "Verify" step about authorization exceptions; the rest was accurate and is expanded slightly.
