---
id: computing-software.devops-ci-cd.verdaccio.install-and-start-verdaccio
name: install-and-start-verdaccio
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [install, npm-install, first-run, verdaccio, private-registry, npmjs]
level: intro
status: docs-checked
description: "Install Verdaccio globally with npm, start it on port 4873, and point npm at it; Node.js version rules and the Docker and Helm alternatives."
sources:
  - https://verdaccio.org/docs/installation/
  - https://verdaccio.org/docs/docker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: the Node.js release must match the Verdaccio line. 6.x needs Node.js 22 or newer, 7.x needs Node.js 24 or newer. npm 10 or newer is recommended.

```
npm install -g verdaccio
verdaccio
```
The server listens on `http://localhost:4873/`. At startup it logs the htpasswd file path and the http address. On first run it writes a default `config.yaml`.

Point a client at it (any one of):
- `npm set registry http://localhost:4873/`
- `npm install --registry http://localhost:4873` for a single command
- `registry=http://localhost:4873` in `.npmrc`
- `publishConfig.registry` in `package.json`

Alternatives: `docker run -it --rm --name verdaccio -p 4873:4873 verdaccio/verdaccio`, or `helm repo add verdaccio https://charts.verdaccio.org` then `helm install registry --set image.tag=7 verdaccio/verdaccio`. Try the 7 prerelease with `npx --yes verdaccio@next-7`.

Read the best practices page before production use.

## Checked

2026-11-04. Confirmed against the Verdaccio Installation, Docker and Command Line Tool pages (Node.js 22 and 24 minimums, npm 10, default port and startup log, client setup options, Docker and Helm commands, next-7). Removed: the stated goal line, the claim that startup prints storage paths, and the log-watching verify tip.
Method: documentation only; no commands were run.
