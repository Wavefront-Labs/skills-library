---
id: computing-software.web-development.node-express.env-file-and-config-validation
name: env-file-and-config-validation
category: computing-software
field: web-development
product: node-express
tags: [node, env-file, config-validation, dotenv, zod, twelve-factor, process-env, web-development]
level: practitioner
status: verified
description: "Configuring Node apps: --env-file and process.loadEnvFile, typed validation of process.env with zod at startup, defaults, secrets handling and per-environment files."
sources:
  - https://nodejs.org/api/cli.html#--env-fileconfig
  - https://nodejs.org/api/process.html#processloadenvfilepath
  - https://12factor.net/config
  - https://zod.dev/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration with --env-file and validated process.env

**Goal:** one typed config object, validated once at startup, failing fast with a clear message.

## 1. Loading .env without dotenv
```bash
node --env-file=.env server.js                    # Node 20.6+
node --env-file=.env --env-file=.env.local app.js # later files override earlier
node --env-file-if-exists=.env.local app.js       # added in Node 22.9 (also present in 20.20 and 22.17; 22.6 rejects it); no error if missing
```
```js
process.loadEnvFile(".env");                      // programmatic, Node 20.12 / 21.7+
```
Existing environment variables win over file values (`PORT=1111 node --env-file=.env` kept 1111). `--env-file` and `process.loadEnvFile` stopped being experimental in Node 24.10 / 22.21. In production, don't ship `.env` files - inject env from the platform/secret manager.

## 2. Validate and type once
```js
// config.js
import { z } from "zod";
const Env = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  PORT: z.coerce.number().int().positive().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  CORS_ORIGINS: z.string().default("").transform((s) => s.split(",").map((x) => x.trim()).filter(Boolean)),   // default BEFORE transform
  FEATURE_X: z.enum(["true", "false"]).default("false").transform((v) => v === "true"),
});
const parsed = Env.safeParse(process.env);
if (!parsed.success) {
  console.error("Invalid configuration:", parsed.error.flatten().fieldErrors);
  process.exit(1);
}
export const config = Object.freeze(parsed.data);
```
Import `config` everywhere; never read `process.env` deep in the code. Order matters in zod 4: with `.transform(...).default("false")` the default is returned as the output untransformed, so `FEATURE_X` came out as the truthy string `"false"` and `CORS_ORIGINS` as `""` (observed on zod 4.6.7); `.default(...)` before `.transform(...)` gives `false` and `[]`.

## 3. Gotchas
- Every env value is a string: `"false"` is truthy; `Number("")` is 0. Coerce explicitly.
- Don't log the config object (secrets). Log which keys are set if needed.
- `NODE_ENV` affects libraries (Express view cache, React builds); don't invent `NODE_ENV=staging` - use a separate `APP_ENV`.
- Secrets in env are visible to child processes and crash dumps; for high-value secrets prefer mounted files or a secret manager SDK.

## 4. Files
Commit `.env.example` with every key and dummy values; gitignore `.env*` except the example. Tests: `node --env-file=.env.test --test`.

## Verify
- [ ] Starting with a missing required var exits non-zero with the key name.
- [ ] `grep -rn "process.env" src | grep -v config.js` returns nothing.
- [ ] `.env` files are not in git (`git ls-files | grep .env`).
