---
id: computing-software.web-development.vitepress.css-preprocessors-and-vscode-intellisense
name: css-preprocessors-and-vscode-intellisense
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, sass, scss, less, stylus, css-preprocessors, vue-official, volar, tsconfig, intellisense]
level: practitioner
status: docs-checked
description: "Use Sass/Less/Stylus in Markdown and theme files, and enable Vue IntelliSense for .md files via tsconfig and VS Code settings."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/using-vue.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vue - Official provides IntelliSense for Vue files out of the box, but `.md` files need configuration adjustments.

**CSS preprocessors.** VitePress supports `.scss`, `.sass`, `.less`, `.styl` and `.stylus` files out of the box (via Vite) with no Vite plugins, but the preprocessor itself must be installed:

```sh
npm install -D sass      # .scss and .sass
npm install -D less
npm install -D stylus
```

Then use them in Markdown and theme components:

```vue
<style lang="sass">
.title
  font-size: 20px
</style>
```

**IntelliSense in `.md` files.** The Vue - Official VS Code plugin needs two adjustments to provide IntelliSense in `.md` files:

1. In `tsconfig.json` or `jsconfig.json`, include Markdown and declare the extension:

```json
{
  "include": ["docs/**/*.ts", "docs/**/*.vue", "docs/**/*.md"],
  "vueCompilerOptions": {
    "vitePressExtensions": [".md"]
  }
}
```

2. In `.vscode/settings.json`:

```json
{
  "vue.server.includeLanguages": ["vue", "markdown"]
}
```

## Checked

2026-11-04. Confirmed against the VitePress using-vue guide (Using CSS Pre-processors, VS Code IntelliSense Support: tsconfig/jsconfig include and vueCompilerOptions.vitePressExtensions, vue.server.includeLanguages). Removed: the unsupported 'Effect' sentence and the Verify step.

Method: documentation only; no commands were run.
