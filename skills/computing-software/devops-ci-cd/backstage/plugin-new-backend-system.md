---
id: computing-software.devops-ci-cd.backstage.plugin-new-backend-system
name: plugin-new-backend-system
category: computing-software
field: devops-ci-cd
product: backstage
tags: [new-backend-system, create-backend, backend-add, backstage]
level: practitioner
status: docs-checked
description: "Compose a Backstage backend with createBackend and backend.add, using features and dependency injection."
sources:
  - https://backstage.io/docs/plugins/new-backend-system
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The new backend system is released and ready for production, and the docs recommend migrating plugins and deployments to it. Its goal was to reduce setup code and make updates easier, using a dependency injection system similar to the frontend's.

```ts
import { createBackend } from '@backstage/backend-defaults';

const backend = createBackend();

backend.add(import('@backstage/plugin-catalog-backend'));

backend.start();
```

Concepts:

- A feature is a plugin or a module, and `backend.add` installs it. The docs example installs the catalog this way.
- Modules extend a single plugin through its extension points (for example an entity provider for the catalog or actions for the scaffolder) and must be deployed with that plugin.
- Services such as logging, database access and configuration are injected rather than constructed by hand.
- Extension points are registered by plugins and let modules customise a plugin's behaviour.

The canonical backend system documentation lives in its own section; this plugin page is marked legacy, so use it for orientation and the backend system docs for details.

## Checked

2026-11-03. Confirmed on the New Backend System page: released and ready for production use with migration recommended, `createBackend` from `@backstage/backend-defaults`, `backend.add`, `backend.start`, dependency injection similar to the frontend, plugins, modules (one plugin, deployed together), services (logging, database access, configuration), extension points, and the legacy notice pointing to the Backend System docs. Removed: the auth, scaffolder and search `backend.add` lines, the lazy-loading claim, the named service list including scheduler, `auth` and `httpAuth`, and the installation order and removal paragraph, none of which this page states.

Method: documentation only; no commands were run.
