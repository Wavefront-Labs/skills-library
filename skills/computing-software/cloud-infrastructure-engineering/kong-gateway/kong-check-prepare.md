---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.kong-check-prepare
name: kong-check-prepare
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, kong-check, kong-prepare, effective-config, validation, cli]
level: practitioner
status: docs-checked
description: "Validate kong.conf with kong check, print the effective configuration with kong prepare --vv, and prepare the prefix directory for starting Nginx directly."
sources:
  - https://developer.konghq.com/gateway/manage-kong-conf/
  - https://developer.konghq.com/gateway/cli/reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kong check and kong prepare

## Validate

```bash
kong check /etc/kong/kong.conf
```

It evaluates the parameters in the file, including those set by environment variables. A valid file returns:

```
configuration at /etc/kong/kong.conf is valid
```

The positional `<conf>` argument defaults to `/etc/kong/kong.conf`.

## Show the effective configuration

```bash
kong prepare --conf /etc/kong/kong.conf --vv
```

`--vv` (debug) prints the full effective configuration, including values from environment variables.

`kong prepare` itself prepares the prefix directory so Nginx can be started directly without `kong start`. Flags: `-c, --conf`, `-p, --prefix`, `--nginx-conf`.

## Health

`kong health -p <prefix>` checks whether the services this node needs are running.

Global flags for every command: `--help`, `--v` (verbose), `--vv` (debug).

## Checked

2026-11-04. Confirmed against the Managing Kong Gateway configuration page (`kong check`, valid-file message, `kong prepare --conf ... --vv` output of all properties including environment variables) and the CLI reference (`kong check` default path, `kong prepare` description and flags, `kong health -p`, global flags). Removed an unsupported advice sentence.
Method: documentation only; no commands were run.
