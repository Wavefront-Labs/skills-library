---
id: computing-software.devops-ci-cd.verdaccio.config-builder-api
name: config-builder-api
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [config-builder, programmatic-config, configbuilder, generate-yaml, verdaccio-config-package]
level: advanced
status: docs-checked
description: "Generate Verdaccio configuration in code with ConfigBuilder from @verdaccio/config, output JSON or YAML, and use it to run a typed test registry."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/e2e/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```js
import { ConfigBuilder } from '@verdaccio/config';
const config = ConfigBuilder.build();
config
  .addUplink('upstream', { url: 'https://registry.upstream.local' })
  .addPackageAccess('upstream/*', { access: 'public', publish: 'foo, bar', unpublish: 'foo, bar', proxy: 'some' })
  .addLogger({ level: 'info', type: 'stdout', format: 'json' })
  .addStorage('/tmp/verdaccio')
  .addSecurity({ api: { legacy: true } });
config.getConfig();   // JSON object
config.getAsYaml();   // YAML string
```
Other methods used on the e2e page: `.addAuth({ htpasswd: { file } })`. Typed keys mean a misspelled setting is a compile error instead of silently ignored.

Programmatic start (e2e page): `const server = (await runServer(config)).listen(4873);` then `server.close()`.

Gotchas:
- Always call `addAuth`; with no auth section the server starts, answers `/-/ping`, and a publish hangs.
- On 6.x an inline config object needs `config.configPath = config.self_path = process.cwd()` or `runServer` throws `configPath property is required`. 7.x does not.

Verify: print `getAsYaml()` once to see what the registry is really given.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Configuration (Config Builder API) and End to End testing. Confirmed: the ConfigBuilder chain, getConfig and getAsYaml, addAuth with htpasswd, runServer(config).listen, the missing-auth publish hang and the 6.x configPath fix. Removed or corrected: nothing.

Method: documentation only; no commands were run.
