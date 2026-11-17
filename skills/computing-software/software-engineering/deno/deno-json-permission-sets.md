---
id: computing-software.software-engineering.deno.deno-json-permission-sets
name: deno-json-permission-sets
category: computing-software
field: software-engineering
product: deno
tags: [deno-json, permissions, permission-set, default-permission, allow-deny-ignore, test-permissions]
level: advanced
status: docs-checked
description: "Named permission sets in deno.json (Deno 2.5+), the -P flag, default set, object form with allow/deny/ignore, test/bench/compile permissions, and the risk."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/deno_json.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deno 2.5+ stores permission sets under `permissions`. Keys are permission names (`read`, `write`, `net`, `env`, `sys`, `run`, `ffi`, `import`); values are a boolean, a string array, or an object with `allow`/`deny`/`ignore`.

```jsonc
{
  "permissions": {
    "read-data": { "read": "./data" },
    "read-and-write": { "read": true, "write": ["./data"] }
  }
}
```

Use with `deno run -P=read-data main.ts`. A set named `"default"` is used with bare `-P`.

Object form: `read` and `env` support `allow`, `deny` and `ignore` (silently ignore); `write`, `net`, `run`, `ffi`, `sys`, `import` support `allow` and `deny` only.

```jsonc
{
  "permissions": {
    "default": {
      "env": { "allow": true, "ignore": ["API_KEY", "SECRET_TOKEN"] },
      "run": { "allow": true, "deny": ["rm", "sudo"] }
    }
  }
}
```

`test`, `bench` and `compile` may carry `permissions` (inline or a set name). Then `deno test` alone errors ("Did you mean to run with `-P`?"); run with `-P`, a permission flag, or `-A`. In a workspace the closest deno.json supplies test/bench permissions.

Risk: a script could edit deno.json to elevate permissions, like `deno task`, hence the explicit `-P` opt-in.

## Checked

2026-11-04. Confirmed against the Deno configuration file (deno.json) reference: Deno 2.5+, permission names and value forms, `-P=name` and the default set, which permissions support `ignore`, test/bench/compile permissions and the `-P` error, workspace closest deno.json, security risk. Nothing removed.

Method: documentation only; no commands were run.
