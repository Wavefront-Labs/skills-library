---
id: computing-software.devops-ci-cd.earthly.earthly-config-global-settings
name: earthly-config-global-settings
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, cache-size-mb, cache-size-pct, buildkit-additional-args, buildkit-additional-config, buildkit-max-parallelism, container-frontend, secret-provider]
level: advanced
status: docs-checked
description: "Tune the global section of the earthly config: cache size, BuildKit parallelism, extra BuildKit args and config, session timeout, CA certs, MTU, ip_tables, frontend."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthly-config/earthly-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthly global config settings

Goal: tune BuildKit and earthly behaviour in the `global:` section of `~/.earthly/config.yml`.

- `cache_size_mb`: total BuildKit cache size in MB, used for automatic garbage collection. 0 or omitted uses the BuildKit internal default of 10% of the root filesystem.
- `cache_size_pct`: cache size as a percentage (0-100) of the filesystem; combined with `cache_size_mb` the lesser value wins; ignored when 0.
- `buildkit_max_parallelism`: max parallelism of BuildKit workers, default 20; lower it on resource-constrained machines.
- `conversion_parallelism`: concurrent converters for targets using blocking commands like `IF`, `WITH DOCKER --load`, `FROM DOCKERFILE`.
- `disable_analytics`, `disable_log_sharing` (logged-in users only): set true to disable.
- `git_image`: image for internal git commands (`GIT CLONE`, `IMPORT`); default `alpine/git:v2.30.1`.
- `org`: default organization; ignored when `--org` or `EARTHLY_ORG` is set.
- `cni_mtu` (between 64 and 65,536) and `ip_tables` (`iptables-legacy` or `iptables-nft`) override automatic detection.
- `no_loop_device` is obsolete and ignored.

## buildkit_additional_args / buildkit_additional_config
Changing either restarts BuildKit on the next run.
```yaml
global:
  buildkit_additional_args: ["--userns", "host"]
```
Session timeout (default 24 hours; `0` disables the feature):
```yaml
global:
  buildkit_additional_args: ["-e", "BUILDKIT_SESSION_TIMEOUT=72h"]
```
Extra CA certificate (needs both keys):
```yaml
global:
  buildkit_additional_args: ["-v", "<absolute-path-to-ca-file>:/etc/config/add.ca"]
  buildkit_additional_config: |
    [registry."<registry-hostname>"]
      ca=["/etc/config/add.ca"]
```

## container_frontend
Auto-discovered in the order Docker, Podman, None. Set `docker-shell` or `podman-shell` explicitly:
```yaml
global:
  container_frontend: podman-shell
```

## secret_provider (experimental)
A program on PATH that receives the secret id as first argument and prints the value on stdout. Exit status 2 means "not found, keep searching under `.secret`"; any other non-zero code makes earthly exit.
```sh
#!/bin/sh
set -e
if [ "$1" = "mysecret" ]; then
    echo -n "open sesame"
    exit 0
fi
exit 2
```

## Gotcha
All stdout is the secret value, including whitespace and newlines, so use `echo -n`. Anything on stderr is shown on the earthly console without affecting the secret.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthly-config/earthly-config.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
