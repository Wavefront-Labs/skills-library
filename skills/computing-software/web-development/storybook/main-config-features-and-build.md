---
id: computing-software.web-development.storybook.main-config-features-and-build
name: main-config-features-and-build
category: computing-software
field: web-development
product: storybook
tags: [features-flags, build-test, disabledaddons, production-build, feature-toggles]
level: advanced
status: docs-checked
description: "Toggle built-in features in main config and slim down production builds used for tests."
sources:
  - https://storybook.js.org/docs/api/main-config/main-config-features
  - https://storybook.js.org/docs/api/main-config/main-config-build
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# features and build.test

Goal: disable unneeded features and trim test builds.

`features` booleans include `actions`, `backgrounds`, `controls`, `highlight`, `interactions`, `measure`, `outline`, `toolbars`, `viewport` (these are enabled by default), plus `componentsManifest`, `developmentModeForBuild`, `docgenServer`, `sidebarOnboardingChecklist` and `menuOnboardingChecklist`. Some flags depend on the renderer, and React also lists `experimentalCodeExamples` and `experimentalTestSyntax` (both experimental). `babelRemoveBugfixes` applies to the Webpack builder only.

```ts
features: { measure: false, outline: false },
```

`build.test` is enabled automatically by `storybook build --test`; the docs advise overriding it only to disable a specific feature or debug a build issue:

```ts
build: {
  test: {
    disableBlocks: true,
    disabledAddons: ['@storybook/addon-a11y'],
    disableMDXEntries: true,
    disableAutoDocs: true,
    disableDocgen: true,
    disableSourcemaps: true,
    disableTreeShaking: true,
  },
},
```
- `disableBlocks`: exclude the `@storybook/addon-docs/blocks` module
- `disabledAddons`: addons disabled in the build output
- `disableMDXEntries`: remove user-written MDX docs entries
- `disableAutoDocs`: leave out autodocs pages
- `disableDocgen`: disable automatic argType and property inference
- `disableSourcemaps`: override the default source map generation
- `disableTreeShaking`: disable tree shaking

Verify: the built Storybook lacks the disabled parts.

## Checked
Date: 2026-11-04. Read the features and build main-config pages (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: feature flag names and defaults, Webpack-only `babelRemoveBugfixes`, every `build.test` option and its effect, `--test` behavior.
Removed: the claim that a test build is smaller than a normal build; the pages do not state it.
Method: documentation only; no commands were run.
