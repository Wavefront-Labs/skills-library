---
id: computing-software.software-engineering.deno.permissions-env-and-sys
name: permissions-env-and-sys
category: computing-software
field: software-engineering
product: deno
tags: [permissions, allow-env, ignore-env, allow-sys, os-info, wildcard]
level: practitioner
status: docs-checked
description: "Granting scoped access to environment variables (suffix wildcards, --ignore-env) and to system information with --allow-sys interface names, including node:os."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/permissions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Environment: `--allow-env[=<VARIABLE_NAME>...]` (`-E`). Since Deno v2.1 suffix wildcards give scoped access.

```sh
deno run --allow-env=HOME,FOO script.ts
deno run --allow-env="AWS_*" script.ts
deno run --allow-env --deny-env=AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY script.ts
```

`--ignore-env[=<VARIABLE_NAME>...]` does not throw: reads silently return `undefined`, treating variables as unset.

```sh
deno run --ignore-env=PORT,HOME script.ts
```

On Windows, names match case-insensitively. The value of `NO_COLOR` is visible to all code regardless of permission.

System info: `--allow-sys[=<API_NAME>...]` (`-S`) gates OS information such as hostname, osRelease, osUptime, loadavg, networkInterfaces, systemMemoryInfo, uid, gid, username, cpus and homedir.

```sh
deno run --allow-sys="systemMemoryInfo,osRelease" script.ts
deno run --allow-sys --deny-sys="networkInterfaces" script.ts
```

The same flag gates Node APIs in `node:os` and `node:process`: `os.cpus()` needs `--allow-sys=cpus`; `os.networkInterfaces()` needs `--allow-sys=networkInterfaces`.

## Checked

2026-11-04. Confirmed against docs runtime/reference/permissions.md: --allow-env/-E, v2.1 suffix wildcards, --ignore-env, Windows case-insensitivity, NO_COLOR, --allow-sys/-S names, node:os mapping.

Method: documentation only; no commands were run.
