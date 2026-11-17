---
id: computing-software.cloud-infrastructure-engineering.openbao.seal-stanza-health-checks
name: seal-stanza-health-checks
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, seal-stanza, health-check, auto-unseal, plugin]
level: practitioner
status: docs-checked
description: "The OpenBao seal stanza: naming, health-check settings and defaults, env var precedence, plugin shadowing and v2.7.0 plugin-only seals."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/configuration/seal/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The seal stanza

Optional. It enables Auto Unseal (HSM or cloud KMS encrypts the root key) instead of the default Shamir seal. Syntax: `seal [NAME] { ... }`, for example `seal "pkcs11"`.

## Health checks

Auto seals periodically encrypt and decrypt a small random payload; failures log warnings so you can fix a broken seal before you need it.

- `health_check_enabled` default true
- `health_check_timeout` default `"1m"`
- `health_check_interval` default `"10m"`
- `health_check_interval_unhealthy` default `"1m"`

## Rules

- Where an option has an environment variable, the variable overrides the config file.
- For plugin seals, the name in the `seal` stanza must match the name in the `plugin` stanza (the plugin name is arbitrary).
- If a KMS provider is both built in and installed as a plugin, the plugin shadows the builtin.

## Deprecation

In OpenBao v2.7.0 many previously built-in mechanisms no longer ship in the standalone binary and are plugin-only. See the deprecation notice linked from the seal stanza page for which mechanisms are affected. External KMS plugins are supported from v2.6.0 and are registered with `plugin "kms" [NAME]` alongside `seal [NAME]`.

Provider pages: transit-seal, static-key-seal.

## Checked

2026-11-04. Read the OpenBao seal stanza overview page in full. Confirmed: optional stanza replacing the default Shamir seal, syntax, environment variable precedence, the health check description and the four options with defaults, plugin name matching, plugin shadowing of builtins and the v2.7.0 plugin-only warning. Removed: a generic upgrade-check instruction and a pointer to an awskms-seal page that is not part of this skill set.
Method: documentation only; no commands were run.
