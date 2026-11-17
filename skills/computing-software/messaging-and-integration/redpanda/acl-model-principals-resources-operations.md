---
id: computing-software.messaging-and-integration.redpanda.acl-model-principals-resources-operations
name: acl-model-principals-resources-operations
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [acl, authorization, principals, resource-pattern-type, operations, rpk-security-acl, least-privilege]
level: practitioner
status: docs-checked
description: "Build least-privilege Redpanda ACLs: principals, hosts, resources incl. Schema Registry subjects, prefixed patterns, operations, and how rpk security acl create multiplies."
sources:
  - https://docs.redpanda.com/streaming/current/manage/security/authorization/acl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
After authorization is enabled, only superusers have access, so create ordinary users and grant ACLs. An ACL rule is principal + resource + operation + host + permission, such as `ALLOW User:analytics-user to READ topic:sensor-data from host:192.168.1.100`. ACLs are stored internally and replicated with Raft, and work with SASL/SCRAM and mTLS.

**Principals** have a type and a name: `User`, `RedpandaRole` or `Group` (OIDC groups use `Group:`). `--allow-principal` and `--deny-principal` add the prefix; `User:*` matches any user. Quote principals that contain commas, for example `--allow-principal='"C=UK,ST=London,L=London,O=Redpanda,OU=engineering,CN=__schema_registry"'`.

**Hosts** default to `*`. `--allow-host` pairs with `--allow-principal`, and `--deny-host` with `--deny-principal`.

**Resources:** `cluster`, `topics`, `groups`, `transactionalid`, and from v25.2 `subject` (`--registry-subject`) and `registry` (`--registry-global`). Schema Registry ACLs must be enabled per cluster. Matching is literal by default; `--resource-pattern-type prefixed` matches everything with the prefix.

**Operations:** READ, WRITE, CREATE, DELETE, DESCRIBE, ALTER, DESCRIBE_CONFIGS, ALTER_CONFIGS, IDEMPOTENT_WRITE, ALL.

```bash
rpk security user create analytics-user --password 'secure-password'
rpk security acl create --allow-principal analytics-user \
  --operation read,describe --topic 'logs-' \
  --resource-pattern-type prefixed
rpk security acl create --allow-principal analytics-user \
  --operation write,describe --topic processed-data
```

ACL commands are multiplicative: two principals and two permissions make four ACLs.

## Checked

2026-11-04. Terminology, flags, resources, operations and the example commands were confirmed on the Configure Access Control Lists page.

Method: documentation only; no commands were run.
