---
id: computing-software.web-development.nestjs.config-env-validation
name: config-env-validation
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, configuration, validation, zod, class-validator]
level: practitioner
status: docs-checked
description: "Fail fast at NestJS startup on bad environment variables using a Standard Schema validationSchema such as Zod or a custom synchronous validate function."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/application/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Option 1, a Standard Schema library (Zod, Valibot, ArkType) through `validationSchema`:

```typescript
ConfigModule.forRoot({
  validationSchema: z.object({
    NODE_ENV: z.enum(['development', 'production', 'test', 'provision']).default('development'),
    PORT: z.coerce.number().default(3000),
  }),
}),
```

Leave a variable without a default to require it; bootstrap throws if it is missing. Env vars are always strings, hence `z.coerce.number()`. `ConfigService` serves the schema's output, so coercions apply. Unknown variables (`PATH`, `HOME`) do not fail validation, and every failing variable is reported, formatted `PATH: message` and joined by newlines. Library settings go under `validationOptions: { libraryOptions: {...} }`.

Joi still works but needs Joi v18+; `@nestjs/config` keeps `allowUnknown: true` and `abortEarly: false` for Joi.

Option 2, a synchronous `validate` function with class-validator:

```typescript
export function validate(config: Record<string, unknown>) {
  const validatedConfig = plainToInstance(EnvironmentVariables, config, { enableImplicitConversion: true });
  const errors = validateSync(validatedConfig, { skipMissingProperties: false });
  if (errors.length > 0) throw new Error(errors.toString());
  return validatedConfig;
}
// ConfigModule.forRoot({ validate })
```

Set `validatePredefined: false` to skip variables that were set before the module loaded (for example `PORT=3000 node main.js`).

Gotchas:
- `validate` must be synchronous.
- Because Node's native `--env-file` variables count as predefined, they are only validated while `validatePredefined` stays `true`.
- If a schema converts `AUTH_ENABLED` to a boolean, `get()` returns the converted value, so do not compare it with `'true'`; use `get<boolean>('AUTH_ENABLED')`.

## Checked

2026-11-04. Read the whole configuration page (`content/application/configuration.md` in nestjs/docs.nestjs.com). Confirmed `validationSchema` with Zod, required-without-default, string coercion, schema output served by `ConfigService`, unknown variables, the `PATH: message` error format, `validationOptions.libraryOptions`, the Joi v18 hint and its defaults, `validatePredefined`, the synchronous `validate` function example, and the native `--env-file` note. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
