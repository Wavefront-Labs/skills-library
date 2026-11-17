---
id: computing-software.messaging-and-integration.redpanda.sasl-scram-users-and-client-connections
name: sasl-scram-users-and-client-connections
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [sasl, scram, users, sasl-mechanisms, rpk-security-user, schema-registry, http-proxy]
level: practitioner
status: docs-checked
description: "Check SCRAM is enabled via sasl_mechanisms, create SCRAM users, grant them ACLs as a superuser, connect rpk as that user, and configure HTTP Proxy credentials from 25.2."
sources:
  - https://docs.redpanda.com/streaming/current/manage/security/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SCRAM is a challenge-response mechanism, so passwords are never sent, even encrypted. It is enabled by default.

```bash
rpk cluster config get sasl_mechanisms
rpk cluster config set sasl_mechanisms '["SCRAM"]'
```
The first should show `SCRAM`. If it is missing, the page says to enable it by appending `SCRAM` to the list; the `set` command replaces the whole list, so include any other mechanisms you still need. Different listeners can use different mechanisms through `sasl_mechanisms_overrides`, for example SCRAM internally and OAUTHBEARER externally.

**Create a user.** Supported mechanisms are `SCRAM-SHA-256` and `SCRAM-SHA-512`. New users have no permissions; only a superuser can grant them via ACLs:

```bash
rpk security user create <my-user> -p '<password>' --mechanism SCRAM-SHA-256
rpk security acl create --allow-principal User:myuser \
  --operation create,describe --cluster \
  -X user=<superuser-name> \
  -X pass='<superuser-password>' \
  -X sasl.mechanism=<superuser-authentication-mechanism>
```
That grants `create` and `describe` on the cluster. Cluster `describe` does not imply topic `describe`, so grant topic permissions separately, for example `--operation describe --topic myfirsttopic`.

**Connect as the user** by passing credentials to rpk, for example:

```bash
rpk topic create myfirsttopic -X sasl.mechanism=SCRAM-SHA-256
rpk topic describe myfirsttopic -X sasl.mechanism=SCRAM-SHA-256
```
with `user` and `pass` supplied via a profile, environment variables or `-X`.

**Schema Registry and HTTP Proxy** support only SASL/SCRAM. Breaking change in 25.2: HTTP Proxy no longer uses ephemeral credentials. If its listeners use `authentication_method: none`, configure explicit `scram_username`, `scram_password` and `sasl_mechanism` for its Kafka client, and give that user the permissions it needs.

## Checked

The commands, supported mechanisms, default permissions, override property and the 25.2 HTTP Proxy change were confirmed on the SASL/SCRAM section of the Authentication page.

Method: docs-checked 2026-11-09 against the Redpanda Authentication page (SASL/SCRAM and Enable authentication sections); no commands were run.
