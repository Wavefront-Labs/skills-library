---
id: computing-software.software-engineering.deno.task-shell-syntax
name: task-shell-syntax
category: computing-software
field: software-engineering
product: deno
tags: [task, shell, boolean-lists, pipelines, redirects, env-vars, shebang]
level: practitioner
status: docs-checked
description: "The cross-platform sh/bash subset in deno task: && || ; &, env vs shell variables, pipes, command substitution, negation, redirects and shebang scripts."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/cli/task.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`deno task` executes in a cross-platform shell that is a subset of sh/bash.

- `a && b` runs b on success; `a || b` on failure; `a ; b` regardless.
- `a & b` runs async. The first failing async command fails the rest; opt out with `|| true`.
- `export VAR=value` exports to spawned processes. `VAR=value` alone is a shell variable, not exported (`Deno.env.get` gives `undefined`). Per-command env: `VAR=hello VAR2=bye deno run main.ts`.
- `$?` holds the last exit code: `deno eval 'Deno.exit(10)' || echo $?`.
- Pipes: `echo Hello | deno run main.ts`; stdout and stderr with `|&`.
- Command substitution: `deno run main.ts $(git rev-parse HEAD)`.
- Negate: `! deno eval 'Deno.exit(1);'`.
- Redirects: `>`, `2>`, `&>`, `>>`, `/dev/null` (works on Windows), `>&2`, `2>&1`, and input `gzip < file.txt`. Multiple redirects are not supported.

Cross-platform shebang (Deno 1.42+): scripts starting `#!/usr/bin/env -S` run the same on all platforms.

```ts title="script.ts"
#!/usr/bin/env -S deno run
console.log("Hello there!");
```

```json title="deno.json"
{ "tasks": { "hi": "./script.ts" } }
```

In JSON config, escape double quotes with backslashes.

## Checked

2026-11-04. Confirmed against docs runtime/reference/cli/task.md (deno task): boolean/sequential/async lists, env vs shell variables, $?, pipes, substitution, negation, redirects, Deno 1.42 shebang.

Method: documentation only; no commands were run.
