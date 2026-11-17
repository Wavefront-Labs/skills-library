---
id: computing-software.web-development.directus.flow-condition-script-operations
name: flow-condition-script-operations
category: computing-software
field: web-development
product: directus
tags: [flow-condition, run-script, flow-operations, sandbox-limits]
level: practitioner
status: docs-checked
description: "Use the Directus flow Condition and Run Script operations: filter-rule branching, missing-field behaviour, sandbox limits and throwing errors."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/06.flows/4.operations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Condition**: validates data against filter rules and takes the resolve or reject path. It appends `null` under its key whether or not it matched; a misconfigured rule appends an array with debug information.

Gotcha: every field in the rules must exist in the data. A field that is absent (not explicitly `null`) sends the flow down reject regardless of operator. For possibly-missing fields use the inverse operator such as `_nnull` and put logic on the reject path.

Warning: in a blocking event-hook flow, ending on a reject path cancels the database transaction.

**Run Script**: vanilla JavaScript or TypeScript in an isolated sandbox. No file system, no network requests, no node modules (build a custom operation extension for libraries).

```js
module.exports = function (data) {
  return { timesTwo: data.previousOperation.value * 2 };
};
```

The return value (must be valid JSON) is appended under the operation key. Throwing an error breaks the chain and stops subsequent flows; with a blocking event hook it cancels the transaction.

## Checked

2026-11-04: confirmed against the Directus docs Operations page (Condition and Run Script sections): null payload and debug array, missing-field callout, blocking hook transaction warning, sandbox limits, node modules callout, JSON return, throwing errors. Removed the unsupported verify line.

Method: documentation only; no commands were run.
