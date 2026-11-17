---
id: computing-software.web-development.astro.astro-env-type-safe-schema
name: astro-env-type-safe-schema
category: computing-software
field: web-development
product: astro
tags: [astro-env, envfield, env-schema, secrets, getsecret]
level: advanced
status: docs-checked
description: "Declare a type-safe env schema with envField in astro.config, choose client or server context and public or secret access, and import from astro:env."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/environment-variables.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add an `env.schema` in config. Each variable needs a `context` (`"client"` or `"server"`) and `access` (`"secret"` or `"public"`), plus options like `optional` or `default`.

```js title="astro.config.mjs"
import { defineConfig, envField } from "astro/config";

export default defineConfig({
  env: {
    schema: {
      API_URL: envField.string({ context: "client", access: "public", optional: true }),
      PORT: envField.number({ context: "server", access: "public", default: 4321 }),
      API_SECRET: envField.string({ context: "server", access: "secret" }),
    }
  }
})
```

Types generate on `astro dev` or `astro build`; run `astro sync` to generate only types. Import from `astro:env/client` or `astro:env/server`:

```astro
---
import { API_URL } from "astro:env/client";
import { API_SECRET } from "astro:env/server";
---
```

Variable kinds: public client (in client and server bundles), public server (server bundle), secret server (not in the bundle). Secret client variables are unsupported: `context: "client"` with `access: "secret"` is not possible. Secrets are validated whenever anything is imported from `astro:env/server`, so you may need dummy values during build, or set `validateSecrets: true` to validate on start.

Types: `envField.string`, `.number`, `.boolean`, `.enum({ values: ["foo", "bar", "baz"], default: "baz" })`.

`getSecret("FOO")` from `astro:env/server` returns `string | undefined` for secrets not in the schema. `astro:env` is a virtual module: it does not work in `astro.config.mjs` or scripts; use `process.env`.

## Checked

2026-11-04. Confirmed against the Astro environment variables guide: env.schema, envField types, context and access combinations, validateSecrets, getSecret and the virtual module limits. Made the import match the declared API_SECRET variable.

Method: documentation only; no commands were run.
