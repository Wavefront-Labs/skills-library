---
id: computing-software.devops-ci-cd.verdaccio.multiple-uplinks-and-offline
name: multiple-uplinks-and-offline
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [multiple-uplinks, failover, offline-registry, proxy-failover, second-registry, air-gapped]
level: practitioner
status: docs-checked
description: "Proxy a package through several uplinks in order (proxy: server1 server2), or build a fully offline registry by removing uplinks and all proxy fields."
sources:
  - https://verdaccio.org/docs/linking-remote-registry/
  - https://verdaccio.org/docs/packages/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Several uplinks per pattern; the first in the list answers, and if it fails the next is tried:

```yaml
uplinks:
  server1:
    url: https://server1.registry.net/npm
  server2:
    url: https://server2.registry.net/npm
packages:
  'webpack':
    access: $all
    publish: $authenticated
    proxy: server1 server2
```
Default `**` can use `proxy: npmjs uplink2` the same way.

Fully offline registry: empty `uplinks`, no `proxy` field anywhere:
```yaml
uplinks:
packages:
  '@my-company/*':
    access: $all
    publish: none
  '**':
    access: $all
    publish: $authenticated
```
Everything you install must then be published locally first.

Alternative from the docs: `.npmrc` scope routing (`@mycompany:registry=http://localhost:4873`) has limits: scopes only, exact match, one registry per scope, tokens in the repo. Pointing clients at Verdaccio only and using uplinks is usually better.

Verify: stop the first uplink and confirm installs still resolve through the second.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Linking a Remote Registry and Package Access. Confirmed: proxy: server1 server2 with first-then-next order, the npmjs uplink2 example, the offline config, and the four scope-routing limits. Removed or corrected: nothing.

Method: documentation only; no commands were run.
