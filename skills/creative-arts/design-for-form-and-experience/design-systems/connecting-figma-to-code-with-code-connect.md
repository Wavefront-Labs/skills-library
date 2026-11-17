---
id: creative-arts.design-for-form-and-experience.design-systems.connecting-figma-to-code-with-code-connect
name: connecting-figma-to-code-with-code-connect
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [code-connect, design-to-code, figma-code-connect, dev-mode, component-mapping, design-code-sync, handoff]
level: practitioner
status: docs-checked
description: "Connect Figma components to code with Code Connect: template files, property mappings, publishing and unpublishing, and what shows in Dev Mode."
sources:
  - "https://developers.figma.com/docs/code-connect/"
  - "https://developers.figma.com/docs/code-connect/quickstart-guide/"
  - "https://developers.figma.com/docs/code-connect/react/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Figma Code Connect

**Goal:** when a developer inspects an instance in Dev Mode, they see the real production code for the component, mapped from its Figma properties, instead of generated CSS.

## Requirements
- A Dev or Full seat on the Professional, Organization or Enterprise plan. Professional plans can have one active library and one active framework; Organization and Enterprise plans can have several active frameworks.
- A personal access token with the Code Connect scope set to Write and the File content scope set to Read.

## Setup
1. Install the command line tool with npm: `npm install --global @figma/code-connect@latest`.
2. Add `figma.config.json` at the project root with a `codeConnect` block holding `include` globs, a `label` (for example React) and a `language`; label and language control how snippets are labelled in Figma.
3. For TypeScript, add `@figma/code-connect/figma-types` to `types` in `tsconfig.json`.
4. Write a template file next to the component, named like it (`Button.figma.ts`): a `// url=` comment pointing at the Figma component (right-click it and choose Copy link to selection), property reads such as `getString`, `getBoolean`, `getEnum` and `getInstanceSwap` on the selected instance, and an `export default` with the code example, its imports and a unique id.
5. Publish from the repository root: `npx figma connect publish --token=PERSONAL_ACCESS_TOKEN`; the `FIGMA_ACCESS_TOKEN` environment variable can replace `--token`.
6. Open the component in Figma, switch to Dev Mode, and check the snippet in the Inspect panel.

An AI agent with the Figma MCP server and the figma-code-connect skill can write template files for you; review the result before publishing.

## Older parser-based files
Figma now says template files are the only actively maintained approach; the framework parsers get no more updates. Existing React files use `figma.connect(Component, url, { props, example })` with helpers `figma.string`, `figma.boolean`, `figma.enum`, `figma.instance` and `figma.nestedProps`, each taking the Figma property name. Code Connect files are not executed: snippets are treated as strings, so conditionals appear verbatim and `figma.connect` cannot be built in a loop.

## Unpublish
`npx figma connect unpublish --node=NODE_URL --label=LABEL` removes one node's mapping for a label. Without a node URL it unpublishes all components defined in the Code Connect files directory, so always pass `--node`.

## Gotchas
- Code Connect UI (in Figma) and the CLI can be used together; CLI-created connections show in the UI but can only be edited in the CLI.
- Keep Figma property names and the names read in template files in step; re-publish after renames.

## Verify
- [ ] Each library component has a template file and Dev Mode shows production code.
- [ ] Token scopes and seat type match the requirements above.

## Checked
2026-11-01. Confirmed on the Code Connect overview, quickstart and React pages: seats and plans, token scopes, install command, `figma.config.json`, template file contents, publish and unpublish commands and the unpublish-all warning, parser deprecation, helper names, not-executed behaviour, UI and CLI interplay. Removed as unconfirmed or wrong: `--save-dev` install, `figma connect create` and wizard, "Organization or Enterprise only" seat claim (corrected), CI publish advice, and main-component versus instance node advice.
Method: documentation only; no commands were run.
