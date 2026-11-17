---
id: computing-software.devops-ci-cd.backstage.auth-guest-provider
name: auth-guest-provider
category: computing-software
field: devops-ci-cd
product: backstage
tags: [guest-provider, development-auth, sign-in-page-providers, backstage]
level: intro
status: docs-checked
description: "Use the guest authentication provider for local development only, and wire it into the sign-in page."
sources:
  - https://backstage.io/docs/auth/guest/provider
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The guest provider emits tokens for a guest user, which suits local development. It differs from the old guest sign-in that only stored identity in the browser.

The docs warn that this provider should only ever be enabled for `development`; the package is explicitly disabled for non-development environments to prevent unauthorised access.

Backend:

```bash
yarn --cwd packages/backend add @backstage/plugin-auth-backend-module-guest-provider
```

```ts
const backend = createBackend();
backend.add(import('@backstage/plugin-auth-backend'));
backend.add(import('@backstage/plugin-auth-backend-module-guest-provider'));
await backend.start();
```

Frontend: add the guest entry to the `SignInPage` providers list, alongside any real providers you want available.

Guidance:

Config: the provider must also be enabled in config, for example in `app-config.local.yaml`:

```yaml
auth:
  providers:
    guest: {}
```

Optional keys are `userEntityRef`, `ownershipEntityRefs` (used for ownership when the user is not found in the catalog) and `dangerouslyAllowOutsideDevelopment`, which allows guest sign-in outside development (for example in production) and should stay off.

The docs say the main reason to use this provider is to exercise permissioned plugins.

## Checked

2026-11-03. Confirmed against the Backstage Guest Authentication Provider page: purpose, development-only warning, package name, backend and frontend snippets, config keys. Removed: the unsupported claims about gating the module by build and about example catalog data.

Method: documentation only; no commands were run.
