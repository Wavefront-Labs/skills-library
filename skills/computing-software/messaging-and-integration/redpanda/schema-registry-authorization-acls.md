---
id: computing-software.messaging-and-integration.redpanda.schema-registry-authorization-acls
name: schema-registry-authorization-acls
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [schema-registry, authorization, acls, registry-subject, registry-global, enterprise]
level: practitioner
status: docs-checked
description: "Restrict Schema Registry with ACLs on registry and subject resources: operation-to-endpoint map, schema_registry_enable_authorization, and consumer, producer, admin recipes."
sources:
  - https://docs.redpanda.com/streaming/current/manage/schema-reg/schema-reg-authorization/
  - https://docs.redpanda.com/streaming/current/manage/schema-reg/schema-reg-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Available from v25.2 and requires an enterprise license. Before 25.2 an authenticated user had full access. Authorization adds two ACL resource types beside `topic`, `group`, `cluster` and `transactional_id`: `registry` (global operations, flag `--registry-global`) and `subject` (flag `--registry-subject`). Manage them with `rpk security acl create`, the Schema Registry `/security/acls` endpoint or Redpanda Console.

Enable it with `rpk cluster config set schema_registry_enable_authorization true`, with authentication set through `schema_registry_api.authn_method`. When SASL is on, the registry's own Kafka client needs credentials, or storing schemas fails with `broker_not_available`:

```bash
--set schema_registry_client.scram_username=<username>
--set schema_registry_client.scram_password=<password>
--set schema_registry_client.sasl_mechanism=SCRAM-SHA-256
```

Operations: `read` (schema content by ID or version), `write` (register), `delete`, `describe` (list subjects and versions), `describe_configs` and `alter_configs` (compatibility and mode). Examples from the page: `GET /subjects` needs describe on subject; `POST /subjects/{subject}/versions` needs write on subject; `/config` and `/mode` need describe_configs or alter_configs on registry or subject; `/schemas/types` and `/status/ready` are open.

Recipes:

```bash
rpk security acl create --allow-principal consumer-app --operation read \
  --registry-subject "orders-*" --resource-pattern-type prefixed
rpk security acl create --allow-principal producer-app --operation read,write,describe \
  --registry-subject "orders-*" --resource-pattern-type prefixed
rpk security acl create --allow-principal schema-admin --operation all --registry-global
```
For migration, source needs `read,describe` on registry-global, the target `write,describe,alter_configs,describe_configs`, plus Kafka ACLs; the target must be in IMPORT mode.

## Checked

2026-11-04. Resource types, operation map, enabling steps, credentials caution and recipes were confirmed on the Schema Registry Authorization page. The page's own examples are not combined here beyond what it shows.

Method: documentation only; no commands were run.
