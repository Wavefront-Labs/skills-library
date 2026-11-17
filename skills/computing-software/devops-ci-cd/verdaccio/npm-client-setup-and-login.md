---
id: computing-software.devops-ci-cd.verdaccio.npm-client-setup-and-login
name: npm-client-setup-and-login
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [npm, npmrc, npm-login, npm-registry, npm-login-legacy, strict-ssl, lockfile-registry]
level: practitioner
status: docs-checked
description: "Point npm at Verdaccio globally, per project, per scope or per command; npm login versus adduser in npm 9+ and 12; SSL and mixed-registry lockfile fixes."
sources:
  - https://verdaccio.org/docs/setup-npm/
  - https://verdaccio.org/docs/cli-registry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Minimum npm is 10.
```
npm set registry http://localhost:4873/                    # user-wide
npm set registry http://localhost:4873/ --location project # .npmrc in project
npm config set @my-scope:registry http://localhost:4873
npm install lodash --registry http://localhost:4873       # one command
```
Project `.npmrc` for a private scope alongside npmjs:
```
registry=https://registry.npmjs.org/
@my-company:registry=http://localhost:4873/
```
Login (npm 9+): `login` authenticates an existing user and `adduser` creates one without logging in. Web login is not supported for Verdaccio, so add `--auth-type=legacy`:
```
npm login --registry http://localhost:4873 --auth-type=legacy
npm adduser --registry http://localhost:4873 --auth-type=legacy
```
npm 12 removed `adduser`; create users in your auth backend, or stay on npm 11.

Troubleshooting:
- `SELF_SIGNED_CERT_IN_CHAIN` with an invalid certificate: `npm config set ca ""` and `npm config set strict-ssl false`.
- npm 7+ lockfileVersion 2 breaks when `resolved` URLs mix npmjs and Verdaccio; installing with another registry fails.
- npm stage needs npm 11.17.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Setup npm and Using a private registry. Confirmed: minimum npm 10, the set registry commands, the scope and per-command forms, login versus adduser from npm 9, the removal of adduser in npm 12, the SSL fix, the lockfile warning and npm stage needing 11.17. Removed or corrected: the verify line (npm whoami is not on the pages).

Method: documentation only; no commands were run.
