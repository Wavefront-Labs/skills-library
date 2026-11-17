---
id: computing-software.web-development.vite.rolldown-options-chunking
name: rolldown-options-chunking
category: computing-software
field: web-development
product: vite
tags: [rolldown-options, code-splitting, manual-chunks, custom-build]
level: advanced
status: docs-checked
description: "Customize the build through build.rolldownOptions and control chunk splitting with output.codeSplitting, including multiple outputs for build-only plugins."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/build.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Beyond the build options, adjust the underlying Rolldown options directly via `build.rolldownOptions`:

```js
export default defineConfig({
  build: {
    rolldownOptions: {
      // https://rolldown.rs/reference/
    },
  },
})
```

For example, specify multiple Rolldown outputs with plugins applied only during build.

Chunking strategy: configure how chunks split with `build.rolldownOptions.output.codeSplitting` (see Rolldown's manual code splitting docs). If you use a framework, follow its documentation for chunk splitting.

Rolldown-level settings such as `input`, `external` and `output.globals` live in this same object, as the multi-page and library examples show.

## Checked

2026-11-07. Re-read the Building for Production guide (docs/guide/build.md) in full. Confirmed build.rolldownOptions, the multiple-outputs-with-build-only-plugins example, build.rolldownOptions.output.codeSplitting with the framework note, and that input, external and output.globals sit in rolldownOptions (Multi-Page App text and Library Mode example). The linked Rolldown reference page was not used as a source. Nothing removed.

Method: documentation only; no commands were run.
