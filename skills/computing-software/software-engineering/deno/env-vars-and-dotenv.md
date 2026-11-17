---
id: computing-software.software-engineering.deno.env-vars-and-dotenv
name: env-vars-and-dotenv
category: computing-software
field: software-engineering
product: deno
tags: [environment-variables, deno-env, env-file, dotenv, precedence]
level: intro
status: docs-checked
description: "Read and set environment variables in Deno with Deno.env, --env-file (multiple files, precedence), @std/dotenv and inline VAR=value in tasks."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/env_variables.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
Deno.env.set("FIREBASE_API_KEY", "examplekey123");
console.log(Deno.env.get("FIREBASE_API_KEY"));
console.log(Deno.env.has("FIREBASE_AUTH_DOMAIN"));
```

`.env` files: `deno run --env-file main.ts` reads `.env` from the cwd or the first parent that has one. Name another file as the flag value; repeat the flag for several.

```sh
deno run --env-file=.env.one --env-file=.env.two --allow-env <script>
```

Precedence: within one file the first declaration of a variable wins; across files the last `--env-file` wins. Quote values containing spaces: `MY_VAR="my value with spaces"`.

`@std/dotenv`:

```ts
import { load } from "jsr:@std/dotenv";
const env = await load({ envPath: ".env.local", export: true });
```

`export: true` also puts values in the process environment so `Deno.env` can read them. Run with `--allow-read --allow-env`.

Inline for one command, handy in tasks:

```jsonc
{ "tasks": { "build:light": { "command": "BUILD_TYPE=LIGHT deno run main.ts" } } }
```

## Checked

2026-11-04. Confirmed against docs runtime/reference/env_variables.md: Deno.env get/set/has, --env-file lookup and repetition, precedence note, @std/dotenv load options, permissions, inline VAR=value in tasks, quoting.

Method: documentation only; no commands were run.
