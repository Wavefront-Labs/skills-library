---
id: creative-arts.design-for-form-and-experience.design-systems.building-tokens-with-style-dictionary
name: building-tokens-with-style-dictionary
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [style-dictionary-build, style-dictionary, token-transforms, design-token-build, token-platforms, amazon-style-dictionary]
level: practitioner
status: docs-checked
description: "Build platform outputs from tokens with Style Dictionary: source files, platforms, transforms and formats, a config example, custom transforms and checks."
sources:
  - https://styledictionary.com/reference/config/
  - https://styledictionary.com/reference/hooks/formats/predefined/
  - https://styledictionary.com/reference/hooks/transform-groups/predefined/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Building tokens with Style Dictionary

Style Dictionary reads token JSON, applies transforms, and writes files for each platform you configure (for example CSS variables and JavaScript modules).

## Minimal config (v4, ES module `config.mjs`)
```js
export default {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'build/css/',
      files: [{ destination: 'variables.css', format: 'css/variables' }]
    },
    js: {
      transformGroup: 'js',
      buildPath: 'build/js/',
      files: [{ destination: 'tokens.js', format: 'javascript/es6' }]
    }
  }
};
```
Run with `npx style-dictionary build --config config.mjs` (`--config` points at a non-default file; the default is `config.json` or `config.js` in the package root). JS config files are ES modules with a default export. The `usesDtcg` option marks DTCG-format tokens, though the docs say it is usually detected automatically. Check the docs for your installed major version.

## Concepts
- **Transforms** change a token's value or name per platform (the `css` group includes `name/kebab` and `size/rem`; the `js` group includes `name/pascal` and `color/hex`). **Transform groups** bundle them.
- **Formats** decide the file output (`css/variables` writes custom properties; `javascript/es6` writes named exports).
- A file entry can take a `filter`; a platform can take `actions`.

## Practice
1. Keep tiers in separate files (primitives, semantic, themes) (see `...design-systems.tokens-tiers-primitive-semantic-component`).
2. Build one output per theme (see `...design-systems.theming-multi-brand-and-multi-mode-tokens`).
3. Run the build in CI and commit or publish outputs; diff outputs in PRs.
4. For Figma sources use the sync pipeline (see `...design-systems.building-a-token-sync-pipeline`).

## Verify
- [ ] An unresolved alias is caught (test it; the docs read did not state the behaviour).
- [ ] CSS output names match the naming convention.
- [ ] CI builds the tokens on each change.

## Checked
2026-11-01. Confirmed on the Style Dictionary config reference, predefined formats and predefined transform groups pages: config keys (`source`, `platforms`, `transformGroup`, `buildPath`, `files`, `destination`, `format`, `filter`, `actions`, `usesDtcg`), CLI `build` and `--config`, ES-module config, the `css` and `js` groups' listed transforms, and the two formats. Removed: the v3/v4 async claim, Android and iOS outputs, alias-failure claim, hex-to-rgba example.
Method: documentation only; no commands were run.
