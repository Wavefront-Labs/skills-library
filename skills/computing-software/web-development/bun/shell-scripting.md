---
id: computing-software.web-development.bun.shell-scripting
name: shell-scripting
category: computing-software
field: web-development
product: bun
tags: [bun-shell, shell-nothrow, shell-injection, shell-redirects]
level: practitioner
status: docs-checked
description: "Script with Bun Shell ($): output methods, quiet and nothrow, cwd and env, injection-safe interpolation, redirects to JS objects, builtins and pitfalls."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/shell.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```js
import { $ } from "bun";
await $`echo "Hello World!"`;                        // resolves { stdout, stderr, exitCode }
const text = await $`echo hi`.text();                // also .json(), .lines(), .blob()
const { exitCode, stdout } = await $`ls`.cwd("/tmp").quiet().nothrow();
await $`echo $NAME`.env({ ...process.env, NAME: "Bun" });
await $`cat < ${new Response("some body")} | wc -w`.text();
await $`echo "Hello" > ${Buffer.alloc(100)}`;
```

- A non-zero exit throws `ShellError` (`exitCode`, `stdout`, `stderr`); `.nothrow()` or `$.nothrow()` disables it.
- Global defaults: `$.cwd()`, `$.env()`, `$.throws(bool)`.
- It is not `/bin/sh`: a reimplementation inside the Bun process. Builtins include `cd`, `ls`, `rm`, `echo`, `pwd`, `cat`, `touch`, `mkdir`, `which`, `mv`, `seq`, `basename`.
- Redirects: `<`, `>`, `2>`, `&>`, `>>`, `2>&1`, `1>&2`.

Security: interpolated strings are escaped into one argument. `` $`bash -c "echo ${input}"` `` is unsafe because the inner shell re-parses it, and `{ raw: ... }` skips escaping. Bun cannot stop an external program treating a value as its own flag, so validate input.

Gotchas: backticks do not substitute (use `$(...)`); commands run concurrently, unlike bash; a bare `await` prints output, so add `.quiet()` or `.text()`.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/shell: text/json/lines/blob readers, quiet, nothrow and ShellError fields, global $.nothrow/$.throws/$.cwd/$.env, per-command cwd and env, redirect operators and JS-object redirects, builtin list, backtick substitution not working, concurrent operation, interpolation escaping, the bash -c and argument-injection warnings, and the { raw } escape bypass. Nothing removed.
Method: documentation only; no commands were run.
