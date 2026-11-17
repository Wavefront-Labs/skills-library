---
id: computing-software.messaging-and-integration.redpanda.rpk-x-options-env-vars-and-precedence
name: rpk-x-options-env-vars-and-precedence
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [rpk, x-options, environment-variables, precedence, tls, sasl, durations]
level: practitioner
status: docs-checked
description: "How rpk resolves settings: -X options, RPK_ environment variables, profiles, then redpanda.yaml, plus the key-to-variable mapping rule, defaults and Go duration format."
sources:
  - https://docs.redpanda.com/streaming/current/reference/rpk/rpk-x-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every rpk setting is a `key=value` after `-X`, for example `rpk -X tls.enabled=true`. Older common flags such as `--brokers` and `--tls-enabled` are deprecated but still supported as `-X` options. `rpk -X list` lists the options and `rpk -X help` gives details.

**Priority** (higher overrides lower):
1. Command-line flags including `-X` (current command only)
2. `RPK_*` environment variables (shell session)
3. rpk profile in `rpk.yaml` (persistent, recommended)
4. `rpk` section of `redpanda.yaml` (system-wide defaults)

**Environment variable rule.** Prefix with `RPK_` and replace dots with underscores: `tls.enabled` becomes `RPK_TLS_ENABLED`, `admin.hosts` becomes `RPK_ADMIN_HOSTS`. Available keys include `brokers`, `tls.enabled`, `tls.ca`, `tls.cert`, `tls.key`, `tls.insecure_skip_verify`, `sasl.mechanism`, `user`, `pass`, the same TLS set under `admin.` and `registry.`, `registry.hosts`, and `globals.*` such as `command_timeout`, `dial_timeout`, `retry_timeout` and `fetch_max_wait`.

Defaults called out: `brokers` is `localhost:9092`; `tls.enabled` and `tls.insecure_skip_verify` are `false`. Giving mTLS certificate file paths automatically opts into `tls.enabled`.

**Durations** use Go format: units `ns`, `us`, `ms`, `s`, `m`, `h`, combinable, such as `30s`, `1m30s`, `2h45m30s`.

**Scripts and automation:**

```bash
export RPK_BROKERS="<broker1:port>,<broker2:port>"
export RPK_USER="<username>"
export RPK_PASS="<password>"
export RPK_SASL_MECHANISM="<mechanism>"
export RPK_TLS_ENABLED="true"
```

## Checked

2026-11-04. Priority order, the variable mapping table, defaults, duration format and the scripting example were confirmed on the rpk -X options page.

Method: documentation only; no commands were run.
