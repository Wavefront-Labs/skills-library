---
id: computing-software.web-development.storybook.storybook-composition
name: storybook-composition
category: computing-software
field: web-development
product: storybook
tags: [composition, refs, composed-storybooks, iframe-security, multi-storybook]
level: advanced
status: docs-checked
description: "Combine multiple Storybooks with the refs config and per-environment refs, plus composition troubleshooting."
sources:
  - https://storybook.js.org/docs/sharing/storybook-composition
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Storybook composition

Goal: browse other Storybooks inside yours.

Add `refs` to `main.ts`:

```ts
refs: {
  'design-system': { title: 'Design System', url: 'https://design.example.com' },
  angular: { title: 'Angular', url: 'http://localhost:4400' },
},
```
Published (statically built) or locally running Storybooks work, with any view layer; their stories appear in your sidebar. Addons in composed Storybooks do not work as they do natively.

Per environment, make `refs` a function receiving `config` and a second argument with `configType`:

```ts
refs: (config, { configType }) =>
  configType === 'DEVELOPMENT'
    ? { x: { title: 'X', url: 'http://localhost:7007' } }
    : { x: { title: 'X', url: 'https://x.example.com' } },
```

Troubleshooting from the page:
- Outdated Storybook versions can generate `index.json` at deploy time with a specific CLI version's `extract` command (not available in Storybook 8.0 or higher); see the older docs.
- In development, Storybook blocks iframe embedding from non-localhost origins and only exchanges messages with a composing Storybook on a local host. For a LAN IP, build the composed Storybook and compose its build output, or enable `security.insecureRemoteIframeEmbed` and `security.insecureIframeMessaging` in the composed Storybook's config, noting this lets any website you visit embed your local Storybook and exchange messages with it.

## Checked

Method: 2026-11-08 read docs/sharing/storybook-composition.mdx and the refs-with-function snippet from the Storybook repo. Removed the package.json / Chromatic package-composition section (not on this page), corrected the `refs` function signature and the iframe troubleshooting (flags belong in the composed Storybook; building is the first option), and removed a Verify step. The first refs example was not compared with the page snippet.
