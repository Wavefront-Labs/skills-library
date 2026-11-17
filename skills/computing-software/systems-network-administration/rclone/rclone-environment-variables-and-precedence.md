---
id: computing-software.systems-network-administration.rclone.rclone-environment-variables-and-precedence
name: rclone-environment-variables-and-precedence
category: computing-software
field: systems-network-administration
product: rclone
tags: [environment-variables, precedence, rclone-config-env, no-config-file]
level: practitioner
status: docs-checked
description: "Configure rclone entirely from environment variables and know the precedence between connection strings, flags, env vars and the config file."
sources: ["https://rclone.org/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every option has an environment variable: take the long flag, strip `--`, change `-` to `_`, upper-case it and prefix `RCLONE_`. `--stats 5s` becomes `RCLONE_STATS=5s`, `--drive-use-trash` becomes `RCLONE_DRIVE_USE_TRASH=true`. Verbosity is special: `RCLONE_VERBOSE=1` for `-v`, `2` for `-vv`. Run `rclone version -vv` to see which options were set from the environment.

## Defining a remote from the environment

Use `RCLONE_CONFIG_` + upper-case remote name + `_` + option. You must set the `_TYPE` variable.

```console
export RCLONE_CONFIG_MYS3_TYPE=s3
export RCLONE_CONFIG_MYS3_ACCESS_KEY_ID=XXX
export RCLONE_CONFIG_MYS3_SECRET_ACCESS_KEY=XXX
rclone lsd mys3:
```

The remote name is only upper-cased, so `my-remote` needs `RCLONE_CONFIG_MY-REMOTE_TYPE`, which many shells cannot export. Use only letters, digits and `_` in names you plan to configure this way. Names defined by environment are case insensitive, unlike config-file remotes. Only the immediate backend is affected: `RCLONE_CONFIG_MYS3CRYPT_ACCESS_KEY_ID` does nothing for a crypt over S3, whereas `RCLONE_S3_ACCESS_KEY_ID` sets the key for every s3 remote including the one under the crypt. Connection strings are usually simpler: `rclone lsd :s3,access_key_id=XXX,secret_access_key=XXX:`.

## Precedence for backend options

First match wins:

1. connection string parameters
2. command-line flags
3. remote-specific env vars (`RCLONE_CONFIG_MYREMOTE_SKIP_LINKS`)
4. backend-specific env vars (`RCLONE_LOCAL_SKIP_LINKS`)
5. backend-generic env vars (`RCLONE_SKIP_LINKS`)
6. config file
7. defaults

For non-backend options the order is flag, environment, default. Other variables: `RCLONE_CONFIG_PASS` (config password), `RCLONE_PASSWORD_COMMAND`, and `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` (HTTPS wins for https requests).

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
