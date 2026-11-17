---
id: computing-software.software-engineering.deno.test-sanitizers
name: test-sanitizers
category: computing-software
field: software-engineering
product: deno
tags: [test, sanitizers, sanitize-ops, sanitize-resources, sanitize-exit, resource-leaks]
level: advanced
status: docs-checked
description: "Catch leaked resources, unawaited async ops and Deno.exit in tests; defaults since Deno 2.8 and the five scopes for enabling sanitizers."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/sanitizers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three sanitizers catch misbehaviour assertions miss.

- Resource sanitizer: all I/O resources created in a test must be closed (`Deno.FsFile`, connections, `fetch` bodies, timers). Off by default as of Deno 2.8; opt in with `sanitizeResources: true`.
- Async op sanitizer: all async operations must complete before the test ends. Off by default as of Deno 2.8; opt in with `sanitizeOps: true`.
- Exit sanitizer: fails tests calling `Deno.exit()`. On by default; disable with `sanitizeExit: false`.

Close things when done:

```ts
const file = await Deno.open("hello.txt");
file.close();

const response = await fetch("https://example.com");
await response.body?.cancel(); // if not consumed otherwise
```

Re-enable resource and op sanitizers (pre-2.8 behaviour) at five scopes, highest precedence first:

1. Per test: `Deno.test({ name: "strict", sanitizeOps: true, sanitizeResources: true, fn() {} })`
2. Per module: `Deno.test.sanitizer({ ops: true, resources: true });`
3. CLI: `--sanitize-ops` and `--sanitize-resources`
4. Env: `DENO_TEST_SANITIZE_OPS=1` and `DENO_TEST_SANITIZE_RESOURCES=1`
5. deno.json:

```jsonc
{
  "test": {
    "sanitizeOps": true,
    "sanitizeResources": true
  }
}
```

An unsanitized `Deno.exit(0)` in a test ends the process, so later tests never run.

## Checked

2026-11-04. Confirmed against docs runtime/test/sanitizers.md: resource, op and exit sanitizers, Deno 2.8 defaults, five enabling scopes, flags, env vars and deno.json keys.

Method: documentation only; no commands were run.
