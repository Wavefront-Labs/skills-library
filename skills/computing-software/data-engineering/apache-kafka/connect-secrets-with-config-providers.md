---
id: computing-software.data-engineering.apache-kafka.connect-secrets-with-config-providers
name: connect-secrets-with-config-providers
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-connect, config-provider, secrets, fileconfigprovider, directoryconfigprovider, envvarconfigprovider, vault, secret-management]
level: practitioner
status: docs-checked
description: "Keep passwords out of Kafka Connect connector configs using ConfigProviders (file, directory, env, Vault/AWS): worker setup, placeholder syntax and rotation."
sources:
  - https://kafka.apache.org/documentation/#config_providers
  - https://github.com/apache/kafka/blob/trunk/docs/configuration/configuration-providers.md
  - https://github.com/apache/kafka/blob/trunk/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfigTransformer.java
  - https://github.com/apache/kafka/blob/trunk/docs/security/security-model-connect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connect secrets with ConfigProviders

**Goal:** connector JSON in git and in the REST API contains references, not passwords. The worker resolves them at task start.

## Worker config
```properties
config.providers=file,dir,env
config.providers.file.class=org.apache.kafka.common.config.provider.FileConfigProvider
config.providers.dir.class=org.apache.kafka.common.config.provider.DirectoryConfigProvider
config.providers.env.class=org.apache.kafka.common.config.provider.EnvVarConfigProvider
# restrict readable paths (if allowed.paths is unset, all paths are allowed)
config.providers.file.param.allowed.paths=/opt/connect/secrets
config.providers.dir.param.allowed.paths=/opt/connect/secrets
# restrict readable environment variables with a regex
config.providers.env.param.allowlist.pattern=^MY_ENVAR1_.*
```
Provider parameters use `config.providers.<alias>.param.<name>`.
Every worker in the cluster needs the same providers and secret files.

## Placeholder syntax `${provider:[path:]key}`
```json
{
  "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
  "database.hostname": "pg.internal",
  "database.user": "${file:/opt/connect/secrets/pg.properties:user}",
  "database.password": "${file:/opt/connect/secrets/pg.properties:password}",
  "database.sslrootcert": "${dir:/opt/connect/secrets/pg-tls:ca.crt}",
  "topic.prefix": "${env:ENV_NAME}"
}
```
- `FileConfigProvider`: properties file, `key=value` lines.
- `DirectoryConfigProvider`: each file in the directory is a key, its content the value (fits Kubernetes secret mounts).
- `EnvVarConfigProvider`: environment variables of the worker process; placeholder `${env:<ENV_NAME>}`.

## External secret stores
Custom providers implement the `org.apache.kafka.common.config.provider.ConfigProvider` interface, packaged as a JAR on the classpath and referenced by class name in `config.providers.<alias>.class`; their settings go in `config.providers.<alias>.param.*`.

## Rotation
Values are resolved when the connector/task (re)starts. A provider that returns a TTL with its data makes the worker schedule a reload; the connector option `config.reload.action` (default `restart`) decides what that does. Otherwise: rotate the secret, then `POST /connectors/x/restart?includeTasks=true`.

## Gotchas
- Connector configurations (including any inlined secrets) are stored in `config.storage.topic`: protect that topic and the offsets and status topics with ACLs as you would any sensitive topic.
- Every worker needs the same provider settings and the same files, since tasks can run on any worker.

## Verify
- [ ] Connector JSON in version control contains only placeholders, never passwords.
- [ ] Connector starts on every worker (move a task by restarting one worker).

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: `config.providers` and `config.providers.<alias>.class`/`.param.` syntax, the three built-in providers and their placeholder syntax (`${alias:path:key}`, `${alias:ENV_NAME}`), `allowed.paths` (unset means all paths allowed) and the EnvVarConfigProvider `allowlist.pattern`, TTL-driven scheduled reload in the worker (WorkerConfigTransformer source) with `config.reload.action` default restart, and the statement that configs including inlined secrets live in the internal topics (security model). Removed: the Kafka 3.5 and 3.x version labels, the Vault, AWS, Azure, Lenses and Strimzi provider list and the Strimzi source link, the `vault.param.ttl` example, the claims about resolved values in task configs and the validation endpoint, and the `grep` check.

Method: documentation only; no commands were run.
