---
id: computing-software.devops-ci-cd.backstage.plugin-create-and-test
name: plugin-create-and-test
category: computing-software
field: devops-ci-cd
product: backstage
tags: [create-plugin, backstage-cli-new, plugin-testing, backstage]
level: practitioner
status: docs-checked
description: "Create a Backstage frontend plugin with yarn new and run it in isolation."
sources:
  - https://backstage.io/docs/plugins/create-a-plugin
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Create a plugin from the repository root:

```bash
yarn new
```

Then select `frontend-plugin`. `yarn new` is a shortcut for `backstage-cli new --select plugin`. The plugin is built and added to the Backstage app automatically, and with the app running (`yarn start`) its default page appears at `/my-plugin` for a plugin id of `my-plugin`.

You can also serve the plugin in isolation by running `yarn start` in the plugin directory, or with `yarn workspace`:

```bash
yarn workspace @backstage/plugin-my-plugin start
```

Serving in isolation gives quicker iteration, a faster startup and hot reloads. It is only meant for local development, and its setup is in the plugin's `dev/` directory.

`yarn new` also offers other plugin library package types. This page is marked legacy for the old frontend system; the docs point to separate pages for the new frontend system and for backend plugins and modules.

## Checked

2026-11-03. Confirmed on the Create a Backstage Plugin page: `yarn new`, the `backstage-cli new --select plugin` shortcut, selecting `frontend-plugin`, automatic build and addition to the app, serving in isolation with `yarn start` or `yarn workspace`, the `dev/` directory, other package types, and the legacy notice. Removed: the testing guidance section (test file names, black-box principle, mocking, `yarn test`), the generated folder layout and the list of plugin types, none of which this page states. The description was narrowed to match.

Method: documentation only; no commands were run.
