---
id: computing-software.cybersecurity-defensive.zitadel.configuration-files-and-environment
name: configuration-files-and-environment
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, configuration, defaults-yaml, steps-yaml, environment-variables, firstinstance]
level: practitioner
status: docs-checked
description: "Configure ZITADEL with the runtime config, the steps file and environment variables, and merge secret files separately."
sources:
  - https://zitadel.com/docs/self-hosting/manage/configure/configure
  - https://zitadel.com/docs/self-hosting/manage/tls_modes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL has two configuration files.

- Runtime configuration: pass with `--config`. Every setting in `defaults.yaml` can also be set by an environment variable, such as `ZITADEL_DATABASE_POSTGRES_DSN`.
- Database initialization file (`steps.yaml`): pass with `--steps`. Its settings also have environment variables.

To change defaults for the first instance created by `zitadel setup`, use the `FirstInstance` section in the steps file; it overrides `DefaultInstance` from the runtime configuration for that first instance.

The documented example passes several `--config` files (a config file and a separate secrets file) together with `--steps`. Use that to keep ordinary configuration, such as the database host, apart from secret configuration, such as passwords.

The masterkey must be 32 bytes. Pass it by value with `--masterkey`, from the `ZITADEL_MASTERKEY` environment variable with `--masterkeyFromEnv`, or from a file with `--masterkeyFile`:

```bash
zitadel start-from-init --masterkey "MasterkeyNeedsToHave32Characters" --tlsMode external
```

Never commit it. Keep it in a secrets manager or inject it as a file or secret at deploy time.

## Checked
2026-11-08. Confirmed against the ZITADEL configure page and TLS modes page: --config, --steps, defaults.yaml environment variables, FirstInstance overriding DefaultInstance, masterkey of 32 bytes with --masterkey, --masterkeyFromEnv and --masterkeyFile, separate secrets config file. Removed: the ExistingDatabase init claim and the ZITADEL_SERVICEPING_ENABLED example, which the page text did not confirm. Fixed the source URL list.
Method: documentation only; no commands were run.
