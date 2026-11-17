---
id: computing-software.web-development.vitepress.import-code-snippets
name: import-code-snippets
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, import-code-snippets, snippet-regions, vscode-region, code-from-file, markdown-snippet]
level: practitioner
status: docs-checked
description: "Import code from real files with <<< @/path, line highlights, #region selection, relative paths and explicit language in braces."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/markdown.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pull code from files that your tests and builds already use, so docs never drift:

```md
<<< @/snippets/snippet.js
<<< @/snippets/snippet.js{2}          <!-- with line highlight -->
<<< ../snippets/snippet.js            <!-- relative path -->
```

`@` is the **source root**: the project root unless `srcDir` is set.

**Regions.** Use a VS Code region and select it with `#name` after the path:

```md
<<< @/snippets/snippet-with-region.js#snippet{1}
```

If a file has several regions with the same name they are all imported and concatenated, including different comment styles (an HTML `<!-- #region -->` in a Vue template and `// #region` in its script). The marker comments are removed from the output; `markdown.snippet.stripRegionMarkers: 'all'` also strips other nested markers, `false` keeps them all. Region names may contain letters, digits, `_`, `-` and `.`. A file name containing `#` needs an explicit region, e.g. `<<< ./my#file.js#region`.

**Language in braces** when it cannot be inferred from the extension (only alphanumeric extensions are inferred, so `main.c++` needs it):

```md
<<< @/snippets/snippet.cs{c#}
<<< @/snippets/snippet.cs{1,2,4-6 c#}
<<< @/snippets/snippet.cs{1,2,4-6 c#:line-numbers}
```

Extra text in the braces is passed on as attributes, such as `{ts twoslash}` when `@shikijs/vitepress-twoslash` is configured; attributes cannot contain square brackets.

**Missing file or region = build error.** Set `markdown.snippet.silent: true` to log a warning and render nothing.

Verify: rename the region and see the build fail loudly.

## Checked

Read the Import Code Snippets section of the markdown guide. Confirmed `<<< @/path`, line highlights, the `@` source root and `srcDir`, relative paths, region selection and concatenation, `markdown.snippet.stripRegionMarkers` and `silent`, region name characters, the `#` file-name rule, language and attributes in braces, and the square-bracket limit. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
