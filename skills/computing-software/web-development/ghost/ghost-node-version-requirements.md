---
id: computing-software.web-development.ghost.ghost-node-version-requirements
name: ghost-node-version-requirements
category: computing-software
field: web-development
product: ghost
tags: [ghost, nodejs, node-versions, nvm, upgrade, compatibility]
level: practitioner
status: docs-checked
description: "Ghost Node.js support: only the current LTS is supported, and Node upgrades require reinstalling dependencies."
sources:
  - https://github.com/TryGhost/docs/blob/main/faq/node-versions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run Ghost on a supported Node.js version.

Support table in the docs: Node 20.x (Iron LTS) and 21.x unsupported, Node 22.x (Jod LTS) required, 23.x and above unsupported. The page also says the required Node version is v22 LTS. Ghost uses the recommended Node.js version in production on Ghost(Pro). Running the latest Node is not guaranteed to work and Ghost cannot offer support for issues.

Upgrade procedure from the page:
1. Install the new Node version with the NodeSource apt flow: import the GPG key, create the deb repository with `NODE_MAJOR` set to a supported version (the page uses 22), then `sudo apt-get update` and `sudo apt-get install nodejs -y`.
2. Run `ghost version` to get the current Ghost version, then `ghost update [version] --force` to force Ghost to reinstall your current version, which re-installs dependencies. Ghost has several binary dependencies compiled for a specific Node version, so skipping this makes Ghost fail to start with strange error messages.

Do not update Node and Ghost at the same time; reinstalling the current Ghost version first ensures Node is updated correctly.

Errors: installing Ghost on an unsupported Node may give `ERROR: Unsupported version of Node` and/or `Exit status 231`; install a compatible Node.js. Multiple Node versions can be installed with nave or nvm.

Compatibility matrix (last rows): Ghost 5.110.0 (2025/02/21) added Node 22 and bumped Ghost-CLI to ^1.27.0; Ghost 6.0.0 (2025/08/04) supports `^22.13.1` only, removing Node 18 and Node 20.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 100 lines, no imported snippets; the "learn more" link on the script deprecation warning was not followed): faq/node-versions.mdx. Removed as unconfirmed: the `ghost backup` step, the "restart Ghost and run `ghost doctor`" step, the advice to check the matrix before upgrading Ghost, CLI and Node together (the page advises against updating Node and Ghost at once), the claim that a production service must use the supported version, and the Verify step.
Method: documentation only; no commands were run.
