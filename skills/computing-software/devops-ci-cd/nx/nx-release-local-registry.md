---
id: computing-software.devops-ci-cd.nx.nx-release-local-registry
name: nx-release-local-registry
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, local-registry, verdaccio, e2e, releaseversion, releasepublish]
level: advanced
status: docs-checked
description: "Update tools/start-local-registry.ts to publish packages to a local registry for e2e tests with releaseVersion and releasePublish from nx/release."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/update-local-registry-setup.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replace the old per-project `publish` targets in the e2e local registry script with Nx Release so newly generated libraries are published too.

Nx creates `tools/start-local-registry.ts`, meant to be called from jest's `globalSetup`. The legacy version is recognisable by this call after starting the registry:

```typescript
execFileSync(nx, ['run-many', '--targets', 'publish', '--ver', '0.0.0-e2e', '--tag', 'e2e'], { env: process.env, stdio: 'inherit' });
```

Replace it with the `nx/release` functions:

```typescript
import { startLocalRegistry } from '@nx/js/plugins/jest/local-registry';
import { releasePublish, releaseVersion } from 'nx/release';

export default async () => {
  const localRegistryTarget = '@demo-plugin-1800/source:local-registry';
  const storage = './tmp/local-registry/storage';
  global.stopLocalRegistry = await startLocalRegistry({ localRegistryTarget, storage, verbose: false });

  await releaseVersion({
    specifier: '0.0.0-e2e',
    stageChanges: false,
    gitCommit: false,
    gitTag: false,
    firstRelease: true,
    versionActionsOptionsOverrides: { skipLockFileUpdate: true },
  });
  await releasePublish({ tag: 'e2e', firstRelease: true });
};
```

Options used by the page: `specifier: '0.0.0-e2e'`, `stageChanges`, `gitCommit` and `gitTag` set to false, `firstRelease: true`, `versionActionsOptionsOverrides: { skipLockFileUpdate: true }` for `releaseVersion`, and `tag: 'e2e'` with `firstRelease: true` for `releasePublish`. The `localRegistryTarget` in the page (`@demo-plugin-1800/source:local-registry`) is its example workspace; use your own.

Related: nx-release-custom-registries (points releases at a registry).

## Checked

2026-11-07. Confirmed against Update Your Local Registry Setup to use Nx Release: the generated tools/start-local-registry.ts and its jest globalSetup purpose, the legacy run-many publish call, and the updated script with releaseVersion and releasePublish from nx/release and every option value shown. Removed: the page does not explain why each option is set, so the rationale for specifier, git flags, firstRelease, skipLockFileUpdate and the e2e tag is gone; also the invented e2e Verify step.

Method: documentation only; no commands were run.
