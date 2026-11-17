---
id: computing-software.web-development.biome.well-known-json-files-comments-and-trailing-commas
name: well-known-json-files-comments-and-trailing-commas
category: computing-software
field: web-development
product: biome
tags: [biome, well-known-files, tsconfig, json-comments, trailing-commas, allowcomments, allowtrailingcommas, turbo-json, jsonc]
level: advanced
status: docs-checked
description: "Which JSON-like files Biome parses with comments and trailing commas by file name, such as tsconfig.json, .eslintrc.json and turbo.json."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/configuration/configure-biome.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Biome treats some JSON-like files specially by file name, not extension. The list currently covers JSON-like files only and may grow with new parsers.

**Strict JSON** (`json.parser.allowComments` and `allowTrailingCommas` both false): `.all-contributorsrc`, `.arcconfig`, `.auto-changelog`, `.bowerrc`, `.c8rc`, `.htmlhintrc`, `.imgbotconfig`, `.jslintrc`, `.nycrc`, `.tern-config`, `.tern-project`, `.vuerc`, `.watchmanconfig`, `mcmod.info`.

**Comments allowed, trailing commas not** (the consuming tools can only strip comments): `.ember-cli`, `.eslintrc.json`, `.jscsrc`, `.jshintrc`, `tslint.json`, `turbo.json`.

**Comments and trailing commas both allowed:** `.babelrc`, `.babelrc.json`, `.devcontainer.json`, `.hintrc`, `.hintrc.json`, `.oxlintrc.json`, `.swcrc`, `api-documenter.json`, `api-extractor.json`, `babel.config.json`, `deno.json`, `devcontainer.json`, `dprint.json`, `jsconfig.json`, `jsr.json`, `language-configuration.json`, `nx.json`, `project.json`, `tsconfig.json`, `typedoc.json`, `typescript.json`, and all `.json` files under project `.vscode/`, `.zed/` and `.cursor/` folders and under the corresponding user settings folders.

Practical effect: Biome will not report parse errors for a commented `tsconfig.json`, but will for a trailing comma in `turbo.json`. For other JSON files with comments set the parser options in an override.

Verify: add a comment to `tsconfig.json` and run `biome check` with no parse error.

## Checked

2026-11-08. Read the Configure Biome guide in full. Confirmed the three well-known-file lists and the VS Code, Zed and Cursor folder rules. Removed a suggestion about the .jsonc extension that the page does not make.

Method: documentation only; no commands were run.
