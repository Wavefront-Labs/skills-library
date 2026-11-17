---
id: computing-software.devops-ci-cd.concourse-ci.dynamic-vars-and-var-sources
name: dynamic-vars-and-var-sources
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [vars, dynamic-vars, var-sources, vault, ssm, secretsmanager, dummy, idtoken, experimental]
level: advanced
status: docs-checked
description: "Understand dynamic vars read at step start and var_sources of type vault, dummy, ssm, secretsmanager and idtoken, with vault_config and which fields can be parameterised."
sources:
  - https://concourse-ci.org/docs/vars/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dynamic vars are read from a credential manager or var source at runtime, so values are not stored in the database. They are fetched as late as possible, when a step using them is about to execute, which allows short-lived credentials and rapid rotation, and they may be cached. Parameterisable attributes: `resource.source`, `resource_type.source`, `resource.webhook_token`, task step `params`, and entire task configs (from `file`, `config` or `fly execute`). Inside `across`, `set_pipeline` identifier and `file`, and the task step identifier, `input_mapping` and `output_mapping` are also interpolated.

**Var sources** are defined in `pipeline.var_sources` and referenced by name: `((my-vault:test-user.username))`. The feature is marked experimental (introduced in v5.8.0). Types: `vault`, `dummy`, `ssm`, `secretsmanager` (v7.7.0+), and `idtoken` (v7.14.0+). The page contradicts itself on one spelling: its type list says `secretmanager`, but the schema section says `secretsmanager`; this skill uses the schema spelling.

- `vault` config: `url`, `ca_cert`, `path_prefix` (default `/concourse`), `lookup_templates` (default `/{{.Team}}/{{.Pipeline}}/{{.Secret}}` and `/{{.Team}}/{{.Secret}}`), `shared_path`, `namespace`, `client_cert`, `client_key`, `server_name`, `client_token`, `auth_backend`, `auth_params`, `auth_max_ttl`, `auth_retry_max`, `auth_retry_initial`, `enable_kv_mount_cache`, and `insecure_skip_verify`, which the page tells you not to use.
- `dummy` config has `vars`, a static map. It is only useful when you have no credential manager but want values redacted from build output.
- `ssm` and `secretsmanager` each take a single `region`.

Since var sources are per pipeline, different pipelines can use different Vault servers or paths.

## Checked

2026-11-04. Dynamic var rules and the var_source schema confirmed on the Vars page, Dynamic vars and Var sources sections. The Vars page spells the Secrets Manager type two ways (`secretmanager` in the list, `secretsmanager` in the schema).

Method: documentation only; no commands were run.
