---
id: computing-software.web-development.strapi.testing-jest-supertest
name: testing-jest-supertest
category: computing-software
field: web-development
product: strapi
tags: [strapi, testing, jest, supertest, sqlite, unit-tests]
level: practitioner
status: docs-checked
description: "Set up Jest and Supertest for a Strapi app: dev dependencies, test script, jest config, and the Windows SQLite caveat."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Testing with Jest and Supertest

Install:

```bash
yarn add jest supertest --dev
```

`package.json` script:

```json
"test": "jest --forceExit --detectOpenHandles"
```

Jest config:

```js
{
  testPathIgnorePatterns: ["/node_modules/", ".tmp", ".cache"],
  testEnvironment: "node",
}
```

## Notes
- Integration tests start a real Strapi instance with an in-memory SQLite database, then call endpoints through Supertest.
- Unit tests for plugin code can mock the `strapi` object instead.
- The guide does not work on Windows with SQLite because of how Windows locks the SQLite file.

## Checked

Checked 2026-11-04 against the Strapi Testing page (introduction, Windows note, install, `package.json` script, Jest config). Removed the WSL or CI suggestion and the explanation of `--forceExit` and `--detectOpenHandles`, which the page does not state.

Method: documentation only; no commands were run.
