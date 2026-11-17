---
id: computing-software.web-development.nestjs.config-module-env-files
name: config-module-env-files
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, configuration, env, dotenv, configservice]
level: intro
status: docs-checked
description: "Load .env files in NestJS with ConfigModule.forRoot, pick file paths, make it global, cache it, and read values through ConfigService get and getOrThrow."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/application/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install `npm i --save @nestjs/config` (uses dotenv internally; needs TypeScript 4.1+).

```typescript
@Module({
  imports: [ConfigModule.forRoot({ isGlobal: true })],
})
export class AppModule {}
```

`forRoot()` parses `.env` from the process working directory, merges it with `process.env`, and registers `ConfigService`. If a key exists in both, the runtime environment wins; set `override: true` to let the file win.

Options:
- `envFilePath: '.development.env'` or an array `['.env.development.local', '.env.development']`; with several files the first one wins.
- `ignoreEnvFile: true` reads only runtime variables.
- `isGlobal: true` avoids importing `ConfigModule` in every module.
- `cache: true` speeds up `ConfigService#get` for `process.env` values.
- `skipProcessEnv: true` makes `get` ignore `process.env`.
- `expandVariables: true` enables `SUPPORT_EMAIL=support@${APP_URL}`.

Reading values:

```typescript
constructor(private configService: ConfigService) {}
const dbUser = this.configService.get<string>('DATABASE_USER');
const dbHost = this.configService.get<string>('database.host', 'localhost');
const must = this.configService.getOrThrow<string>('DATABASE_USER');
```

`getOrThrow()` throws when the value is `undefined` and its return type excludes `undefined`. In `main.ts` use `app.get(ConfigService)`. For variables needed before bootstrap use `nest start --env-file .env`, or run `node --env-file=.env dist/main.js` with `ignoreEnvFile: true`.

Gotchas:
- With `process.loadEnvFile()`, call it in a file imported before `AppModule`; a call in the `main.ts` body is too late because `forRoot()` reads `process.env` while `app.module` is evaluated.
- `ConfigService<Env>` with `get('PORT', { infer: true })` types the result from the interface.

## Checked

2026-11-04. Read the whole configuration page (`content/application/configuration.md` in nestjs/docs.nestjs.com). Confirmed the install line and TypeScript 4.1 note, `forRoot()` behaviour and runtime-wins precedence with `override`, `envFilePath` (first file wins), `ignoreEnvFile`, `isGlobal`, `cache`, `skipProcessEnv`, `expandVariables`, `get`/`getOrThrow`, `app.get(ConfigService)`, `nest start --env-file`, the native `--env-file` and `process.loadEnvFile()` notes, and `ConfigService<Env>` with `infer`. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
