---
id: computing-software.software-engineering.typescript.node-configuration-env-file-and-parseargs
name: node-configuration-env-file-and-parseargs
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, env-file, parseargs, process-env, configuration, dotenv, nodejs]
level: practitioner
status: verified
description: "Configure Node apps without extra deps: process.env typing and validation, --env-file / process.loadEnvFile, util.parseArgs for CLIs, and failing fast on bad config."
sources: ["https://nodejs.org/api/cli.html#--env-fileconfig", "https://nodejs.org/api/util.html#utilparseargsconfig", "https://nodejs.org/api/process.html#processloadenvfilepath", "https://12factor.net/config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node configuration: env files and parseArgs

**Goal:** typed, validated configuration from environment variables and CLI flags,
loaded once at startup.

## .env files (`--env-file` added Node 20.6; `--env-file-if-exists` added 22.9)
```bash
node --env-file=.env --env-file-if-exists=.env.local dist/server.js
```
```ts
process.loadEnvFile(".env");            // programmatic (Node 21.7+ and 20.12+)
```
Existing environment variables win over file values (checked: `KEEP=env node --env-file=...` kept `env`); with several `--env-file` flags later files override earlier ones; a missing `--env-file-if-exists` file prints "not found. Continuing without it." Commit `.env.example`, never `.env`
with secrets. In containers/Kubernetes inject real env vars and skip the file.

## Parse and validate once
```ts
import { z } from "zod";
const Env = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  PORT: z.coerce.number().int().min(1).max(65535).default(8080),
  DATABASE_URL: z.string().url(),
  FEATURE_SEARCH: z.stringbool().default(false),     // zod 4 (checked with zod 4.6.7); or z.enum(["true","false"]).transform(v => v === "true")
});
export const config = Env.parse(process.env);       // throws a ZodError whose `issues` list every invalid key
```
Everything in `process.env` is a string (or undefined): `"false"` is truthy, `Number("")` is 0.
Never read `process.env.X` deep in business code - import `config`.

## CLI flags with util.parseArgs
```ts
import { parseArgs } from "node:util";
const { values, positionals } = parseArgs({
  args: process.argv.slice(2),
  allowPositionals: true,
  options: {
    out: { type: "string", short: "o", default: "dist" },
    verbose: { type: "boolean", short: "v", multiple: true },
    help: { type: "boolean", short: "h" },
  },
  strict: true,                         // unknown flags throw
});
if (values.help) { printUsage(); process.exit(0); }
```
For subcommands, completion and generated help, use `commander` or `yargs`.

## Precedence
Defaults < config file < environment < CLI flags. Log the effective config at startup with
secrets redacted.

## Exit codes
Exit non-zero on invalid config (`process.exitCode = 1` then return, or throw at top level) so
orchestrators mark the deploy failed instead of crash-looping later.

## Verify
- [ ] Starting with a missing required variable prints which key is missing and exits 1.
- [ ] No direct `process.env` reads outside the config module (lint rule `n/no-process-env`).
