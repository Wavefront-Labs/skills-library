---
id: computing-software.devops-ci-cd.renovate.constraints
name: constraints
category: computing-software
field: devops-ci-cd
product: renovate
tags: [constraints, tool-versions, language-constraints, renovate]
level: advanced
status: docs-checked
description: "How Renovate detects tool and language constraints for artifact updates, how to override them, and datasource filtering."
sources:
  - https://docs.renovatebot.com/configuration-options/#constraints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Constraints tell Renovate which versions of third-party tools to use when it updates artifacts such as lock files and checksum files. Renovate typically detects them automatically from files within the repository, so you rarely need to set them. Constraints do not take effect when `binarySource=global`.

Constraints also restrict which datasource versions can be upgraded to, based on language support. For now this works for `python`:

```json
{
  "constraints": {
    "python": "2.7"
  }
}
```

To override what Renovate detects, wrap the constraints in the `force` object of the global self-hosted configuration (not repository config):

```js
module.exports = {
  force: {
    constraints: {
      node: '< 15.0.0',
    },
  },
};
```

Related options:

- `constraintsFiltering` is `none` (all releases allowed) or `strict`, which includes a release only if its constraints match the package file constraints. It needs a `constraints` object or detected constraints, and a datasource that returns constraint data per release.

Enabling `constraintsFiltering=strict` with `binarySource=global` can make Renovate suggest updates it cannot then apply, because the right tool versions are not installed. The default for `constraintsFiltering` is `none`.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page: `constraints` (automatic detection, python datasource restriction, `force` in global config), `constraintsFiltering` (`none`/`strict`, default, requirements) and the `binarySource=global` warnings. Removed: `engines` and tool-version file examples, the `binarySource=install` claim, and the artifact-error troubleshooting advice. The `force` example now follows the docs (global config, JS).

Method: documentation only; no commands were run.
