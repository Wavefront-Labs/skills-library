---
id: computing-software.devops-ci-cd.verdaccio.private-vs-public-routing
name: private-vs-public-routing
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [proxy-routing, private-packages, dependency-confusion, publish-conflict, proxy-removal, fork]
level: advanced
status: docs-checked
description: "Keep private packages from leaking to npmjs lookups by removing proxy on private patterns, and override a public package with a fork or a temporary prerelease."
sources:
  - https://verdaccio.org/docs/best/
  - https://verdaccio.org/docs/packages/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default every pattern proxies to npmjs, so even a locally published `@my-company/auth` is looked up publicly. Remove `proxy` on private patterns and keep it on the rest:

```yaml
packages:
  '@my-company/*':
    access: $authenticated
    publish: $authenticated
    unpublish: $authenticated
  '@*/*':
    access: $authenticated
    publish: $authenticated
    proxy: npmjs
  '**':
    access: $authenticated
    publish: $authenticated
    proxy: npmjs
```
This also avoids needless metadata merges and tarball downloads, and the best practices page files it under security. Use a prefix such as `local-*` or a scope; order matters.

Override a public package:
- Permanent fork: add a separate entry with no `proxy` and publish a version higher than the cached public one.
- Temporary patch: publish a prerelease of the next patch version so the original wins once it catches up.
```
npm version 0.1.3-my-temp-fix
npm publish --tag fix --registry http://localhost:4873
```
Example: a public 0.1.2 pairs with 0.1.3-my-temp-fix.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Best Practices and Package Access. Confirmed: the default proxy to npmjs, the example with proxy removed on the private scope, ordering, the fork and temporary prerelease options, and the 0.1.2 and 0.1.3-my-temp-fix example. Removed or corrected: the verify line, and the unsupported dependency-confusion wording.

Method: documentation only; no commands were run.
